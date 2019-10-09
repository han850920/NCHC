from app import app
from app.models import ImgObject
from flask import render_template, url_for, json,request,redirect
from jinja2 import Template
from .utils import Reporter
import os
import glob
import sqlite3
import time

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
    
    conn = sqlite3.connect('NCHC-submit.db')
    cursor = conn.cursor()
    list_of_files = glob.glob('/tmp/*-FOOD.json') # * means all if need specific format then *.csv
    data_list=[]    
    # parse the latest json-FOOD file
    if list_of_files!=[]:
        latest_file = max(list_of_files, key=os.path.getctime)
        
        data_list = refresh_data(latest_file)
    else:
        return render_template('index.html', data_list = [], submit_page = True)


    if request.method == "POST":
        img_obj = request.json
        if img_obj is not None:
            table_name = get_latest_table_name(cursor)
            cursor.execute('UPDATE {} SET state = 1 WHERE name=?'.format(table_name),(img_obj['name'],))
            conn.commit()
            # print("call line bot")
            cmd = "python script/post_linebot_arg.py \'" + img_obj['ID'] + "\' \'" +img_obj['road'] + "\' \'" + img_obj['time'] + "\' \'" + img_obj['name'] + "\' \'" + img_obj['path'] + "\'"
            os.system(cmd)
            # print(cmd)
            return redirect(url_for('index'))
        else:
            print("refresh")
            # create new table and insert the new data
            table_name = "`" + data_list[0].time +"`"
            if table_name != get_latest_table_name(cursor):
                # drop old table
                cursor.execute('select name from sqlite_master where type = "table"')
                table = cursor.fetchall()
                for t in table:
                    cursor.execute('DROP TABLE IF EXISTS {}'.format("`" + t[0] + "`"))    
                cursor.execute('CREATE TABLE {}(id TEXT, road TEXT, time TEXT, name TEXT, path TEXT,state BOOLEAN)'.format(table_name))
                cursor.executemany("INSERT INTO {} VALUES(?,?,?,?,?,?)".format(table_name),((img.ID,img.road,img.time,img.name,img.path,0,) for img in data_list))
                conn.commit()
                time.sleep(1)
            return redirect(url_for('index'))
    else:
        #select the latest data
        table_name = get_latest_table_name(cursor)
        print(table_name)
        if table_name == "`" + data_list[0].time + "`":
            row = cursor.execute('SELECT * FROM {}'.format(table_name))
            data_list=[]
            for r in row:
                img_object = ImgObject()
                img_object.ID = r[0]
                img_object.road = r[1]
                img_object.time = r[2]
                img_object.name = r[3]
                img_object.path = r[4]
                img_object.state = r[5]
                data_list.append(img_object)
         
        return render_template('index.html', data_list = data_list, submit_page = True)

    
    

@app.route('/records',methods=['GET', 'POST'])
def records():

    
    data_list=[]
    conn = sqlite3.connect('NCHC-submit.db')
    cursor = conn.cursor()
    if request.method =='POST':
        
        reporter = Reporter(1) # 0 => 小圖置下 ; 1 ＝> 小圖置右
        report_path = reporter.make_report()
        print("save report")
        

            

    table_name = get_latest_table_name(cursor)
    row = cursor.execute("SELECT * FROM {} WHERE state = 1".format(table_name))
    for r in row:
        img_object = ImgObject()
        img_object.ID = r[0]
        img_object.road = r[1]
        img_object.time = r[2]
        img_object.name = r[3]
        img_object.path = r[4]
        img_object.state = r[5]
        data_list.append(img_object)
    return render_template('records.html', data_list = data_list,submit_page = False)

def refresh_data(json_file_name):
    # json_url = os.path.join(SITE_ROOT,json_file_name)
    data = json.load(open(json_file_name))
    data_list=[]
    
    for d in data:
        img_object = ImgObject()
        key_idx = 0
        data_str=""
        flag=0
        for i in d:
            if i == "\'":  
                flag = (flag+1) % 2
                if flag==0:
                    img_object.set_(data_str, key_idx)
                    key_idx = (key_idx+1) % 6
                    data_str=""
                continue
            if flag==1:
                data_str += i
        img_object.state = False
        data_list.append(img_object)
    # clean all old img
    cmd="rm -rf ./app/static/img/*"
    os.system(cmd)

    if len(data_list)>=0:
        # add new image
        for d in data_list:
            cmd="cp %s ./app/static/img/"%(d.path)
            os.system(cmd)
    return data_list

def get_latest_table_name(cursor):
    cursor.execute('select name from sqlite_master where type = "table"')
    table = cursor.fetchall()
    if len(table)>0:
        table_name = "`"+table[-1][0]+"`" # because there are punctuation name
        return table_name
    else:
        return None