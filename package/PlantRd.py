# -*- encoding:utf-8 -*-
#获取飞行配置函数接受如下参数
# 1 药材在市场上价格
# 2 种植地区经纬度
# 3 种植地区列表
# 4 查找药材名称
# 5 种植区域分布比例列表
def getFlyOption(results2,results_geo,citylist,keyword,plantNeedData):
    marketData = {}
    flyGeo = {
        '荷花池': [104.084339, 30.697028],
        '玉林': [110.190178, 22.658497],
        '亳州': [115.763194, 33.842247],
        '安国': [115.275916, 38.465295]
    }  # 飞行地点坐标
    flyVal = []  # 飞行数据
    # marketlist = ['荷花池', '玉林', '亳州', '安国']
    marketlist =[]
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
        "flyGeo": flyGeo
    }
    return backData
