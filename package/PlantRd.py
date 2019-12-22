# -*- encoding:utf-8 -*-
from math import radians, cos, sin, asin, sqrt
#获取飞行配置函数接受如下参数
# 1 药材在市场上价格
# 2 种植地区经纬度
# 3 种植地区列表
# 4 查找药材名称
# 5 种植区域分布比例列表
def getFlyOption(results2,results_geo,citylist,arguments,plantNeedData):
    keyword =arguments['keyword']
    marketData = {}
    flyGeo = {
        '荷花池': [104.084339, 30.697028],
        '玉林': [110.190178, 22.658497],
        '亳州': [115.763194, 33.842247],
        '安国': [115.275916, 38.465295]
    }  # 飞行地点坐标
    flyVal = []  # 飞行数据
    # marketlist = ['荷花池', '玉林', '亳州', '安国']
    marketlist =[]#真正收购的市
    marketGeo = getMarketGeo(flyGeo,results2)#获取药材市场经纬度
    plantGeo = getPlantGeo(results_geo)#获取种植区域经纬度
    PMdistance = getPMD(marketGeo,plantGeo)
    PMPrice = getPMP(PMdistance,arguments,results2)
    print(results2)
    for i in results2:
        marketlist.append(i[1])
    # 获得经纬度
    for i in results_geo:
        temp_geo = i[1].split(',')
        temp_geo[0] = float(temp_geo[0])
        temp_geo[1] = float(temp_geo[1])
        flyGeo[i[0]] = temp_geo
    # 获得市场价格
    for i in results2:
        marketData[i[1]] = {
            "name": i[1],
            "value": float(i[3])
        }
        # 获得飞行路线
    for market in marketlist:
        try:
            flyVal.append([
                {'name': market},
                {'name': market, 'value': 100}
                # marketData[market]
            ])
        except:
            err=8000
    for market in marketlist:
        try:
            for city in citylist:
                flyVal.append([
                    {'name': market},
                    {'name': city, 'value': 40}
                ])
        except:
            err=8000
    backData = {
        "drugname": keyword,
        "plantData": plantNeedData[0:4],
        "flyVal": flyVal,
        "flyGeo": flyGeo,
        "PMD":PMdistance
    }
    return backData

def getPMD(marketGeo,plantGeo):
    geodistance(120.12802999999997, 30.28708, 115.86572000000001, 28.7427)
    PMDistanceList = []
    for plant in plantGeo:
        for market in marketGeo:
            PMDistanceList.append({
                "start":plant['name'],
                "end":market['name'],
                "distance":geodistance(plant['geo'][0],plant['geo'][1],market['geo'][0],market['geo'][1]),
                "price":market['price']
            })
    # for i in PMDistanceList:
    #     print(i)
    return PMDistanceList

def geodistance(lng1,lat1,lng2,lat2):
    # lng1, lat1, lng2, lat2 = (120.12802999999997, 30.28708, 115.86572000000001, 28.7427)
    lng1,lat1,lng2,lat2 = map(radians,[float(lng1),float(lat1),float(lng2),float(lat2)])# 经纬度转换成弧度
    dlon = lng2 - lng1
    dlat = lat2 -lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance=round(distance/1000,3)
    return distance

def getMarketGeo(flyGeo,real):
    marketGeo = []
    realMarket = []
    priceObj = getPrice(real)
    for realMarket_item in real:
        realMarket.append(realMarket_item[1])
    for market_item in flyGeo:
        if market_item in realMarket:
            marketGeo.append({
                'name': market_item,
                'geo': flyGeo[market_item],
                'price':priceObj[market_item]
            })
    return  marketGeo

def getPlantGeo(results_geo):
    plantGeo = []
    for plant_item in results_geo:
        temp_geo = plant_item[1].split(',')
        temp_geo[0] = float(temp_geo[0])
        temp_geo[1] = float(temp_geo[1])
        plantGeo.append({
            'name': plant_item[0],
            'geo': temp_geo
        })
    return plantGeo

def getPrice(rows):
    Price={}
    for row in rows:
        Price[row[1]] = row[3]
    return Price

#获得种植推荐，计算价格
def getPMP(PMdistance,arguments,marketPrice):
    number = arguments['number']
    trans = arguments['trans']
    lirunList = []
    for i in range(len(PMdistance)):
        lirun = float(PMdistance[i]['price'])*number - float(PMdistance[i]['distance'])*trans
        PMdistance[i]['lirun'] = lirun
    for i in PMdistance:
        print(i)


