# -*- encoding:utf-8 -*-
from flask import Flask,jsonify,render_template,request
from py2neo import Graph
from package import SimRd,GetInfor
import time
import MySQLdb
import json
app = Flask(__name__)
# 数据库连接
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')

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

@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
