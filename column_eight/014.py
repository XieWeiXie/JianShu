# -*- coding:utf-8 -*-
# To: learn MySQLdb
# Date: 2016.05.02
# Author: wuxiaoshen

import MySQLdb
connector = MySQLdb.connect(
    user="root",
    host="localhost",
    port=3306,
    passwd="123456",
    db="exercise",
    charset="utf8")
cur = connector.cursor()
sql = 'select * from persons WHERE id =1'
sql2 = "UPDATE persons SET FirstName = 'xiexiaolu' WHERE id = 1"
sql3 ="INSERT INTO persons(Id, LastName,FirstName,Address,City)VALUES (4, 'xiaolu', 'xie','zhabei','shanghai')"
cur.execute(sql3)
sql4 = 'select * from persons'
cur.execute(sql4)
A = cur.fetchall()
for one in A:
    print(one)

