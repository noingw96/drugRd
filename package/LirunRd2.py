# -*- encoding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model import db
from math import sqrt


# pip install --upgrade -i https://mirrors.tencent.com/pypi/simple numpy

def gitAllPirce(key):
    ret_time =[]
    ret_price =[]
    switch = {
        '金银花':'jinyinhua',
        '连翘':'lianqiao'
    }
    result = db.sql_helper("select time,"+switch[key]+" from drug_price")
    for i in result:
        ret_time.append(i[0])
        ret_price.append(i[1])
    ret = {
        'time':ret_time,
        'price':ret_price
    }
    return ret

def cal_sum(list,k,mark):
    if mark==0:
        n = 0
        for i in list:
            n += i
        return float(n / k)
    else:
        n = list[0]*mark  # mark为指数α，依次递减
        cur_mark = mark
        for i in list[1:]:
            cur_mark = cur_mark * (1 - mark)
            n += i * cur_mark
        return n

def move(list,a,b,mark):
    pre = list.copy()
    length = len(list)
    for i in range(a,length):
        pre[i] = cal_sum(pre[i-b:i],b,mark)
    return pre
def MAE(a,b):
    N = 12
    the_abs = 0
    for i in range(len(a)):
        the_abs += abs(a[i] - b[i])
    return the_abs/N
def price_pre(train_range,slider,mark=0):
    result = db.sql_helper("select * from sheet3")
    # result = db.sql_helper("select * from test_data")
    data = []
    for i in result:
        data.append(float(i[3]))
    train_data = data[0:train_range]
    test_data = data.copy()
    predict = data.copy()
    ret = move(predict,train_range,slider,mark)
    # print(data)
    # print(ret)

    # plt.ylabel("价格")
    # plt.xlabel("时间")
    #
    #
    #
    # plt.plot(test_data, label='Trust')
    # plt.plot(ret, label='predict')
    # plt.plot(train_data, label='Train')
    # plt.legend(loc='best')
    rms = MAE(data,ret)
    # print(rms)
    # plt.show()
    return ret


#第一参数5-8可以，其中8最好
# price_pre(48,8,0.9)#人参

# a=price_pre(48,10,0.4)#白芍
# print(a[-1])


