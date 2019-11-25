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
    sql = 'select * FROM loginuser where loginid = "' + username + '"'
    cursor.execute(sql)
    results = cursor.fetchall()[0]
    print(results[0])



    print("程序执行时间：",(time.clock()-start))