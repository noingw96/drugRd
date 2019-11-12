# -*- encoding:utf-8 -*-
from flask import Flask,jsonify,render_template,request
from py2neo import Graph
from package import SimRd,GetInfor,ProvinceDict
import time
import MySQLdb
import json
app = Flask(__name__)
# 数据库连接
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')

#一、页面方法
#请求药材资讯的推荐内容
@app.route('/inforRd',methods=['POST','GET'])
def inforRd():
    request_data = request.args.get("content")
    try:
        cursor = db.cursor()
        sql = 'select * FROM erwei'
        cursor.execute(sql)
        results = cursor.fetchall()  # 数据库中找到满足条件的结果
        myresult = SimRd.search(results, request_data)  # 比较矩阵中相似度，返回前10个结果
        str = ''  # 查询的字符串
        for line in myresult:
            str += '"' + line['name'] + '",'
        sql2 = 'select * FROM information where keyName in (' + str[:-1] + ')'
        cursor.execute(sql2)
        inforListResult = cursor.fetchall()
        inforList = []
        inforList = GetInfor.get(inforListResult)  # 获取推荐的资讯列表
        return jsonify(elements=inforList, rank=myresult)
    except:
        errMessage ={
            "errCode":"1001",
            "Message":"暂无此数据"
        }
        return jsonify(elements=errMessage)

#请求药材的分类
@app.route('/requestClass',methods=['POST','GET'])
def requestClass():
    request_id = request.args.get("drugId")
    request_name = request.args.get("drugName")
    try:
        cursor = db.cursor()
        sql = 'select * FROM drugBasedetail where drugClassId ='+request_id
        cursor.execute(sql)
        results = cursor.fetchall()
        #封装返回数据
        responseData = {
            'category': request_name,
            'categorgId': request_id,
            'content': []
        }
        for line in results:
            responseData['content'].append({
                 'drugId': line[0],
                 'drugName': line[1],
                 'drugClass': line[2],
                 'drugClassId': line[3],
                 'otherName': line[4],
                 'newTime': line[5],
                 'productionArea': line[6],
                 'characteristic': line[7],
                 'img': line[8],
            })
        return jsonify(elements=responseData)
    except:
        errMessage ={
            "errCode":"1002",
            "Message":"暂无此类别"
        }
        return jsonify(elements=errMessage)

#请求省份常见药材，显示地图点击页面上
@app.route('/requestProvinceFloat', methods=['POST', 'GET'])
def requestProvinceFloat():
    try:
        cursor = db.cursor()
        sql = 'select * FROM drugposition'
        cursor.execute(sql)
        results = cursor.fetchall()
        backData = ProvinceDict.getProvinceFloat(results)
        return jsonify(elements=backData)
    except:
        errMessage ={
            "errCode":"1003",
            "Message":"省份数据仍在更新，请稍后"
        }
        return jsonify(elements=errMessage)

@app.route('/ProvinceClassNum', methods=['POST', 'GET'])
def requestProvinceClassNum():
    keyword = request.args.get("province")
    try:
        cursor = db.cursor()
        sql = 'select * FROM drugposition where position like "' + keyword + '"'
        cursor.execute(sql)
        results = cursor.fetchall()
        sql2 = 'select * FROM drugbasedetail'
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        classRate = ProvinceDict.getProvinceClassNum(results, results2, keyword, 8)
        return jsonify(elements=classRate)
    except:
        errMessage = {
            "errCode": "1004",
            "Message": "有关于省市的药材分类数据仍在更新"
        }
        return jsonify(elements=errMessage)



#二、页面内容
#首页
@app.route('/')
def index():
    return render_template('index.html')

#分类页
@app.route('/class')
def Drugclass():
    return render_template('class.html')

#分布页
@app.route('/dist')
def Drugdist():
    return render_template('dist.html')

@app.route('/login')
def login():
    return render_template('login.html')



#三、inc中，页面的公共部分
@app.route('/inc/leftMenu')
def leftMenu():
    return render_template('inc/leftMenu.html')

@app.route('/inc/bgChange')
def bgChange():
    return render_template('inc/bgChange.html')

@app.route('/inc/header')
def headerMenu():
    return render_template('inc/header.html')

if __name__=='__main__':
    app.run(debug=True)
