# -*- encoding:utf-8 -*-
import numpy as np
from py2neo import Graph
import time
import MySQLdb
from package import SimRd,GetInfor
import json
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')
if __name__=='__main__':
    start = time.clock()
    cursor = db.cursor()
    sql = 'select * FROM erwei'
    cursor.execute(sql)
    results = cursor.fetchall()
    myresult=SimRd.search(results,"人参")
    str=''
    for line in myresult:
        str+='"'+line['name']+'",'
    sql2 = 'select * FROM information where keyName in ('+str[:-1]+')'
    cursor.execute(sql2)
    results1 = cursor.fetchall()
    all=[]
    all=GetInfor.get(results1)
    for i in all:
        print(i)
    print("程序执行时间：",(time.clock()-start))