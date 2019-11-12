# -*- encoding:utf-8 -*-
#求药材分布页，左下角数据接口，显示当前省份的常见药材,传入参数药材与省市对应集合
def getProvinceFloat(results):
    allData = {}
    backData = {}
    for line in results:
        name = line[1]
        position = line[2]
        if position in allData.keys():
            if len(allData[position]['drugList']) <= 10:
                allData[position]['drugList'].append({
                    'name': name,
                    'value': line[3]
                })
                if line[3] < allData[position]['minValue']:
                    allData[position]['minValue'] = line[3]
            else:
                if line[3] > allData[position]['minValue']:
                    sort = sorted(allData[position]['drugList'], key=lambda e: e.__getitem__('value'), reverse=True)
                    allData[position]['drugList'] = sort[0:10]
                    allData[position]['minValue'] = allData[position]['drugList'][9]['value']
        else:
            allData[position] = {
                'minValue': 0,
                'drugList': []
            }
            allData[position]['minValue'] = line[3]
            allData[position]['drugList'].append({
                'name': name,
                'value': line[3]
            })
    for i in allData:
        temp = ''
        for j in allData[i]['drugList']:
            temp += j['name'] + ';'
        # backData.append({
        #     'province': i,
        #     'list': temp
        # })
        backData[i] = temp
    return backData

#获取省份药材各分类的数量，传入参数，results该省市的药材列表，results2药材与分类对于的字典，keyword省份,limit返回内容的长度
#执行时间0.014769951987886247
def getProvinceClassNum(results,results2,keyword,limit):
    if limit >=12:
        limit = 12
    data = {
        keyword: []
    }
    classObj = {}  # 药材-类字典
    classRate = {} #种类-数量字典
    for line in results:
        data[keyword].append(line[1])
    for line in results2:
        classObj[line[1]] = line[2]
    for i in data[keyword]:
        className = classObj[i]
        if className in classRate.keys():
            classRate[className] += 1
        else:
            classRate[className] = 1
    while len(classRate) > limit:
        minKey = ''
        minNum = 10000
        for i in classRate:
            if classRate[i] < minNum:
                minKey = i
                minNum = classRate[i]
        del classRate[minKey]
    realBack = {
        'province':keyword,
        'content':classRate
    }
    return realBack