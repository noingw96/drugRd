# -*- encoding:utf-8 -*-
import numpy as np
from py2neo import Graph
import time
import MySQLdb
import json
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')
def clearUser(list):
    new_user=[]
    for i in list:
        new_user.append(float(i))
    return new_user
#利用余弦相似度进行推荐:平均时间0.10868
def search(main):
    cursor = db.cursor()
    searchResult=[]
    sql = 'select * FROM erwei'
    cursor.execute(sql)
    allData=[]
    aim={}
    similarResult=[]
    results = cursor.fetchall()
    for row in results:
        cur = {
            "name":row[0],
            "position":row[1:]
         }
        allData.append(cur)
        if row[0]==main:
            aim=cur
    for row in allData:
        theSimilar = cos_sim(clearUser(aim['position']),clearUser(row['position']))
        similarResult.append({
            "name":row["name"],
            "similar":theSimilar
        })
    sort = sorted(similarResult, key=lambda e: e.__getitem__('similar'), reverse=True)
    return sort[0:10]
def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim
if __name__=='__main__':
    start = time.clock()
    myresult=search("人参")
    for i in myresult:
        print(i)
    print("程序执行时间：",(time.clock()-start))