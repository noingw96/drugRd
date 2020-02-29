# -*- encoding:utf-8 -*-
import random
#获取资讯列表，格式化
def get(informations):
    all = []
    newInforList=[]
    for infor in informations:
        cur = {
            'key': infor[0],
            'title': infor[1],
            'intro': infor[2],
            'author': infor[3],
            'time': infor[4],
            'url': infor[5]
        }
        all.append(cur)
    newInforList = RandomInfor(all)
    return newInforList[1:20]
def RandomInfor(inforList):
    #将资讯列表乱序
    randomList = []
    while len(inforList)>0:
        rand = random.randint(0, len(inforList) - 1)
        popElement = inforList.pop(rand)
        randomList.append(popElement)
    return randomList

def getSearch(informations):
    all = []
    for infor in informations:
        cur = {
            'key': infor[0],
            'title': infor[1],
            'intro': infor[2],
            'author': infor[3],
            'time': infor[4],
            'url': infor[5]
        }
        all.append(cur)
    return all[1:20]

