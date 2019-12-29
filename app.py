# -*- encoding:utf-8 -*-
from flask import Flask,jsonify,render_template,request
from py2neo import Graph
from package import SimRd,GetInfor,ProvinceDict,PlantRd
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

#获取省份药材分类数据
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
        classRate = ProvinceDict.getProvinceClassNum(results, results2, keyword, 12)
        return jsonify(elements=classRate)
    except:
        errMessage = {
            "errCode": "1004",
            "Message": "有关于省市的药材分类数据仍在更新"
        }
        return jsonify(elements=errMessage)

#登录判断
@app.route('/LoginCheck', methods=['POST', 'GET'])
def loginCheck():
    #接受post请求
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    username = json_data.get("username")
    password = json_data.get("password")
    flag = json_data.get("flag")
    print(username,password,flag)
    try:
        cursor = db.cursor()
        sql = 'select * FROM loginuser where loginid = "' + username + '"'
        cursor.execute(sql)
        results = cursor.fetchall()[0]
        if results[1] == password:
            sql2 = 'select * FROM userinfo where loginid = "' + username + '"'
            cursor.execute(sql2)
            info = cursor.fetchall()[-1]
            backMessage={
                "successCode": "2001",
                "message": "登录成功",
                "username":results[0],
                "nickname":results[2],
                "tel":results[3],
                "address":results[4],
                "createname":results[5],
                "userinfo":info[3]
            }
        else:
            backMessage={
                "errCode": "1005",
                "message": "用户不存在或密码错误"
            }
        return jsonify(elements=backMessage)
    except:
        errMessage = {
            "errCode": "1006",
            "message": "用户不存在或密码错误"
        }
        return jsonify(elements=errMessage)

#注册信息
@app.route('/RegisterMsg', methods=['POST', 'GET'])
def registerMsg():
    # 接受post请求
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    username = json_data.get("username")
    password = json_data.get("password")
    nickname = json_data.get("nickname")
    tel = json_data.get("tel")
    address = json_data.get("address")
    createtime = json_data.get("createtime")
    operdrug=''
    print(username,password,nickname,tel,address,createtime)
    try:
        cursor = db.cursor()
        sql = 'insert into loginuser (loginid,password,nickname,tel,useraddress,createtime) values("' + str(
            username) + '","' + str(password) + '","' + str(nickname) + '","' + str(tel) + '","' + str(
            address) + '","' + str(createtime) + '") '
        cursor.execute(sql)
        sql2 = 'insert into userinfo (loginid,time,operdrug) values("' + str(username) + '","' + str(
            createtime) + '","' + str(operdrug) + '") '
        cursor.execute(sql2)
        backMessage = {
            "code": "2002",
            "message": "注册成功"
        }
        return jsonify(elements=backMessage)
    except:
        errMessage = {
            "code": "1007",
            "message": "账号已存在，请修改账号重新注册"
        }
        return jsonify(elements=errMessage)

#用户日志更新
@app.route('/UpdateInfo', methods=['POST', 'GET'])
def updateInfo():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    userid = json_data.get("userid")
    operdrug = json_data.get("userinfo")
    time = json_data.get("time")
    try:
        cursor = db.cursor()
        sql = "insert into userinfo (loginid,time,operdrug) values('" + userid + "','" + time + "','" + operdrug + "') "
        cursor.execute(sql)
        backMessage = {
            "code": "2003",
            "message": "更新日志成功"
        }
        return jsonify(elements=backMessage)
    except:
        errMessage = {
            "code": "1008",
            "message": "服务器忙，暂时无法更新日志"
        }
        return jsonify(elements=errMessage)

#获取种植推荐页可视化配置
@app.route('/getFlyOption', methods=['POST', 'GET'])
def getFlyOption():
    arguments = {
        'keyword':request.args.get("drugname"),
        'position':request.args.get("position"),
        'number':request.args.get("number"),
        'trans':request.args.get("trans"),
    }
    cursor = db.cursor()
    sql = 'select * from drugposition where name ="' + arguments['keyword'] + '"'  # 获取药材种植区域
    cursor.execute(sql)
    results = cursor.fetchall()
    sql2 = 'select * from money where drugName ="' + arguments['keyword'] + '"'  # 获取药材市场价格
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    plantData = []
    sql_str = ''  # 查找省份待拼接字符串
    citylist = []
    for i in results:
        plantData.append({
            "name": i[2],
            "value": i[3]
        })
    plantNeedData = sorted(plantData, key=lambda e: e.__getitem__('value'), reverse=True)
    for i in plantNeedData[0:4]:
        sql_str += '"' + i['name'] + '",'
        citylist.append(i['name'])
    sql_geo = 'select areaName,center FROM t_area where areaName in (' + sql_str[:-1] + ')'  # 获取相应城市的坐标
    cursor.execute(sql_geo)
    results_geo = cursor.fetchall()
    backData = PlantRd.getFlyOption(results2, results_geo, citylist, arguments, plantNeedData)  # 获取配置主方法
    return jsonify(elements=backData)
    # try:
    #
    # except:
    #     errMessage = {
    #         "code": "1009",
    #         "message": "服务器忙，暂时无法更新推荐内容"
    #     }
    #     return jsonify(elements=errMessage)

# 请求种植推荐页饼图列表2数据
@app.route('/DrugSim', methods=['POST', 'GET'])
def DrugSim():
    request_data = request.args.get("drugname")
    try:
        cursor = db.cursor()
        sql = 'select * FROM erwei'
        cursor.execute(sql)
        results = cursor.fetchall()
        myresult = SimRd.search(results, request_data)  # 比较矩阵中相似度，返回前10个结果
        return jsonify(myresult)
    except:
        errMessage = {
            "errCode": "1010",
            "Message": "暂无此数据"
        }
        return jsonify(elements=errMessage)

#二、页面路由
#首页-资讯页
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

#种植推荐页
@app.route('/plant')
def plant():
    return render_template('plant.html')


#登录页
@app.route('/login')
def login():
    return render_template('login.html')

#注册页
@app.route('/register')
def register():
    return render_template('register.html')



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
