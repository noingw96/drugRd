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
    # keyword = "灵芝孢子粉"
    keyword = "白芍"
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
            "name":i[2],
            "value":i[3]
        })
    plantNeedData = sorted(plantData, key=lambda e: e.__getitem__('value'), reverse=True)
    for i in plantNeedData[0:4]:
        sql_str += '"'+i['name']+'",'
        citylist.append(i['name'])
    sql_geo = 'select areaName,center FROM t_area where areaName in ('+sql_str[:-1]+')' #获取相应城市的坐标
    cursor.execute(sql_geo)
    results_geo = cursor.fetchall()
    arguments = {
        'keyword': keyword,
        'position': "",
        'number':2000,
        'trans': 500,
    }
    backData = PlantRd.getFlyOption(results2,results_geo,citylist,arguments,plantNeedData)


    # flyGeo = {
    #     '荷花池': [104.084339, 30.697028],
    #     '玉林': [110.190178, 22.658497],
    #     '亳州': [115.763194, 33.842247],
    #     '安国': [115.275916, 38.465295]
    # }
    # print(flyGeo)
    # a=flyGeo
    # print(a)
    # a['荷花池']=1
    # print(a)
    # print(flyGeo)





    print("程序执行时间：",(time.clock()-start))