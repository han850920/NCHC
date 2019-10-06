from PIL import Image,ImageDraw,ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import math
import time 
class Reporter():
    def __init__(self):
        self.img_width = 320
        self.img_height = 240
        self.report_width = self.img_width * 3
        self.repot_height = 0
        self.url='http://140.110.17.128/aimap/stoca/color_lamp/nowred.aspx'

    def get_Web(self,url,name):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
        browser=webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
        browser.get(url)
        try:
            WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.ID, 'map'))
            )
        except Exception as e:
            print(e)
        time.sleep(1)
        img_path = './app/static/reports/'+name+'.png'
        browser.save_screenshot(img_path)

        browser.quit()
        return_img = Image.open(img_path)
        return_img = return_img.resize((self.report_width, int(self.report_width/return_img.size[0] * return_img.size[1])),Image.ANTIALIAS)


        return return_img

    def draw_idx_circle(self,id,image):
        x=30
        y=30
        r=30    
        draw = ImageDraw.Draw(image)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,0))

        if id<10:
            fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 70)
            draw.text((x-3*r/4,y-6*r/5), str(id), font=fnt, fill=(255,255,255),align="left",)
        elif 9<id and id<100:
            fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 45)
            draw.text((x-4*r/5,y-4*r/5), str(id), font=fnt, fill=(255,255,255),align="left",)
        else:
            fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
            draw.text((x-r,y-4*r/5), str(id), font=fnt, fill=(255,255,255),align="left",)
        
        return image

    def make_report(self, data):
        report_name = os.path.splitext(data[0]['mseg']['im_name'].split('_')[-1])[0]
        x_offset = 0
        y_offset = 0
        self.report_height = math.ceil(len(data)/3)* self.img_height
        new_im = Image.new('RGB', (self.report_width, self.report_height))

        
        for k,v in enumerate(data):
            img_path = os.path.join('/tmp', report_name, v['mseg']['im_name'])
            img = Image.open(img_path)
            img = img.resize((self.img_width,self.img_height),Image.ANTIALIAS)
            igm = self.draw_idx_circle(v['data']['index'],img)
            new_im.paste(img, (x_offset, y_offset))
            x_offset += self.img_width
            if (k+1) % 3 == 0:
                x_offset=0
                y_offset+=self.img_height

        web_img = self.get_Web(self.url,report_name)

        report_im = Image.new('RGB', (self.report_width, self.report_height+web_img.size[1]))

        report_im.paste(web_img, (0, 0))
        
        report_im.paste(new_im, (0, web_img.size[1]))
        report_path = os.path.join('/tmp',report_name+'_confmapflag.jpg')
        report_im.save(report_path)
        return report_path
        



        
