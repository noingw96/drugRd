# -*- encoding:utf-8 -*-
from flask import Flask,jsonify,render_template,request
from py2neo import Graph
import time
import MySQLdb
import json
app = Flask(__name__)
# 数据库连接
# grapy = Graph(
#     "http://localhost:7474",
#     username="neo4j",
#     password="161616"
# )
db = MySQLdb.connect("127.0.0.1", "root", "root", "wzw", charset='utf8')
def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.properties)
    return {"data": data}
def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id),
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}
    return {"data": data}

@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
