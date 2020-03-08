# -*- encoding:utf-8 -*-
import numpy as np
from py2neo import Graph
import time
import MySQLdb
import json
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['STZhongsong']    # 指定默认字体：解决plot不能显示中文问题
plt.rcParams['axes.unicode_minus'] = False
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')
province=[ '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '北京', '天津', '上海', '重庆', '台湾省']
similarYao = []
def clearUser(list):
    new_user=[]
    for i in list:
        new_user.append(float(i))
    return new_user
#利用余弦相似度进行推荐:平均时间0.35658413195658817
def search(main,database,is_sort,the_max=1,the_min=-0.1):
    index = province.index(main)+1
    aim = 'p'+ str(index)
    cursor = db.cursor()
    searchResult=[]
    allData = []
    origin = {}#目标地区向量
    for i in range(1,33):
        column = 'p'+ str(i)
        sql = 'select '+ column +' FROM '+ database
        cursor.execute(sql)
        results = cursor.fetchall()
        cur = {
            "name": province[i - 1],
            "position": []
        }
        for row in results:
            cur['position'].append(row[0])
        allData.append(cur)
        if aim == column:
            origin = cur
    similarResult=[]


    for row in allData:
        theSimilar = cos_sim(clearUser(origin['position']),clearUser(row['position']),the_max,the_min)
        similarResult.append({
            "name":row["name"],
            "similar":theSimilar
        })
    if is_sort:
        sort = sorted(similarResult, key=lambda e: e.__getitem__('similar'), reverse=True)
    else:
        sort = similarResult
    return sort
    # return sort[0:10]
def cos_sim(vector_a, vector_b,the_max,the_min):

    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    # add method 阈值
    # the_min = -0.1
    # the_max = 0.6

    j=0
    for i in range(len(vector_a)):
        if vector_a[j] <= the_min or vector_b[j] <= the_min or vector_a[j] >= the_max or vector_b[j] >= the_max:
            vector_a.pop(j)
            vector_b.pop(j)
        else:
            j+=1
    yu = 10
    if len(vector_a)<=yu or len(vector_b)<=yu:
        return 0
    #add method
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim
def MAE(a,b):
    N = 32
    the_abs = 0
    for i in a:
        cur_name = i['name']
        for j in b:
            if cur_name == j['name']:
                the_abs += abs(i['similar']-j['similar'])
    return the_abs/N*10
def format(train):
    train_data = []
    for i in train:
        train_data.append(i['similar'])
    return train_data

def getYaocai(erwei_train,the_min,the_max,key):
    shuju = erwei_train[1:5]
    all_data=[]
    cursor = db.cursor()
    origin_index = province.index(key)+1
    origin = 'p' + str(origin_index)
    for i in shuju:
        name = i['name']
        index = province.index(name)+1
        column = 'p' + str(index)
        sql = 'select name,' + column +','+origin+ ' FROM erwei_train'
        cursor.execute(sql)
        results = cursor.fetchall()
        similar_yaocai = []
        origin_yaocai=[]
        for j in results:
            if float(j[1]) >= the_min and float(j[1]) <= the_max and float(j[2]) >= the_min and float(j[2]) <= the_max:
                similar_yaocai.append({
                    "yaocai_name": j[0],
                    'rate': j[1]
                })
                origin_yaocai.append({
                    "yaocai_name": j[0],
                    'rate': j[2]
                })
        # sort = sorted(similar_yaocai, key=lambda e: e.__getitem__('rate'), reverse=True)[0:10]
        all_data.append({
            "similar_position":name,
            "similar":similar_yaocai,
            'position':key,
            'origin':origin_yaocai
        })
    return all_data

#main方法帮助找出key地区相似的前几个地区，以及具体的药材比率
def main(key):
    the_min = 0.01
    the_max = 0.4
    erwei_train = search(key, "erwei_train", True, the_max, the_min)
    data = getYaocai(erwei_train,0.1,1,key)
    # for i in data:
    #     print(i)
    return data

def doublePosition(p1,p2):
    the_min = 0.05
    the_max = 1
    cursor = db.cursor()
    index1 = province.index(p1) + 1
    index2 = province.index(p2) + 1
    column1 = 'p' + str(index1)
    column2 = 'p' + str(index2)
    sql = 'select name,' + column1 + ',' + column2 + ' FROM erwei'
    cursor.execute(sql)
    results = cursor.fetchall()
    similar_yaocai = []
    origin_yaocai = []
    for j in results:
        if float(j[1]) >= the_min and float(j[1]) <= the_max and float(j[2]) >= the_min and float(j[2]) <= the_max:
            similar_yaocai.append({
                "yaocai_name": j[0],
                'rate': j[1]
            })
            origin_yaocai.append({
                "yaocai_name": j[0],
                'rate': j[2]
            })
    return [similar_yaocai,origin_yaocai]
# main('辽宁')
# doublePosition('辽宁','吉林')