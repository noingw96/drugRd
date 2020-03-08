# -*- encoding:utf-8 -*-
import MySQLdb
db = MySQLdb.connect("127.0.0.1", "root", "root", "bishe", charset='utf8')
def sql_helper(sql):
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()  # 数据库中找到满足条件的结果
    return results