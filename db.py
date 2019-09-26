import sqlite3
conn = sqlite3.connect('NCHC-submit.db')
cursor = conn.cursor()
table_name = "test8"
# cursor.execute('DROP TABLE IF EXISTS submit')
# cursor.execute('CREATE TABLE IF NOT EXISTS {}(id TEXT, road TEXT, time TEXT, name TEXT, path TEXT,state BOOLEAN)'.format(table_name))
# road='myRo ad'
# cursor.execute('INSERT INTO "{}" VALUES("myID",?,"myTime","myName","myPath",1)'.format(db_name,road))

cursor.execute('select name from sqlite_master where type = "table"')
table = cursor.fetchall()
# for t in table:
#     print(t)
print(table)
# for t in table:
#     table_name = "`"+t[0] + "`"
#     print(table_name)
#     row = cursor.execute('select * from {}'.format(table_name))
#     for r in row:
#         print(r)