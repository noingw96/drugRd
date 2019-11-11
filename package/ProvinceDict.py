# -*- encoding:utf-8 -*-
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