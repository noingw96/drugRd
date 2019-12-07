# -*- encoding:utf-8 -*-
import numpy as np
from py2neo import Graph
import time
import MySQLdb
from package import SimRd,GetInfor
import json
from package import PlantRd
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')
if __name__=='__main__':
    start = time.clock()
    cursor = db.cursor()
    keyword = "灵芝孢子粉"
    sql = 'select * from drugposition where name ="'+keyword+'"'#获取药材种植区域
    cursor.execute(sql)
    results = cursor.fetchall()
    sql2 = 'select * from money where drugName ="' + keyword + '"'#获取药材市场价格
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    plantData=[]
    sql_str='' #查找省份待拼接字符串
    citylist = []
    for i in results:
        plantData.append({
            "position":i[2],
            "rate":i[3]
        })
    plantNeedData = sorted(plantData, key=lambda e: e.__getitem__('rate'), reverse=True)
    for i in plantNeedData[0:4]:
        sql_str += '"'+i['position']+'",'
        citylist.append(i['position'])
    sql_geo = 'select areaName,center FROM t_area where areaName in ('+sql_str[:-1]+')' #获取相应城市的坐标
    cursor.execute(sql_geo)
    results_geo = cursor.fetchall()

    backData = PlantRd.getFlyOption(results2,results_geo,citylist,keyword,plantNeedData)
    print(backData)





    print("程序执行时间：",(time.clock()-start))