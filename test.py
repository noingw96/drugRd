# -*- encoding:utf-8 -*-
import numpy as np
from py2neo import Graph
import time
import MySQLdb
from package import SimRd,GetInfor
import json
from package import ProvinceDict
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')
if __name__=='__main__':
    start = time.clock()
    cursor = db.cursor()
    keyword = "安徽"
    username = '7180289'
    address = '长沙'
    sql = 'select * from userinfo where loginid ="7180289"'
    cursor.execute(sql)
    results = cursor.fetchall()




    print("程序执行时间：",(time.clock()-start))