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
    sql = 'select * FROM drugposition where position like "'+ keyword+'"'
    cursor.execute(sql)
    results = cursor.fetchall()
    sql2 = 'select * FROM drugbasedetail'
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    classRate = ProvinceDict.getProvinceClassNum(results,results2,keyword,12)
    print(classRate)




    print("程序执行时间：",(time.clock()-start))