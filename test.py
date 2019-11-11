# -*- encoding:utf-8 -*-
import numpy as np
from py2neo import Graph
import time
import MySQLdb
from package import SimRd,GetInfor
import json
from package import ProvinceDict
db = MySQLdb.connect("127.0.0.1", "root", "root", "wzw", charset='utf8')
if __name__=='__main__':
    start = time.clock()
    cursor = db.cursor()
    sql = 'select * FROM positiondetail'
    cursor.execute(sql)
    results = cursor.fetchall()
    className = '加工类'
    backData=ProvinceDict.getProvinceFloat(results)
    for i in backData:
        print(i)
    print("程序执行时间：",(time.clock()-start))