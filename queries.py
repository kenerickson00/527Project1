from flask import Flask, request, render_template
from connection import connect_rds, connect_redshift, connect_drill, connect_mongo2

import pymysql

app = Flask(__name__)

@app.route('/redshift')
def query_redshift():
    query = request.args.get('query')
    connection = connect_redshift()
    fields, items, time = connection.perform_query(query)
    result = {'fields': fields, 'items': items, 'time': time}
    connection.close()
    return result

@app.route('/rds')
def query_rds():
    '''db = pymysql.connect(host='database-2.csgrmq8cjzjf.us-east-1.rds.amazonaws.com', user='admin', password='CS527Group5', db= 'CS527' )
    cursor = db.cursor()
    data = cursor.execute('select sum(ID) from trial')
    data = cursor.description
    fields = []
    if data is not None:
        for i in range(len(data)):
            fields.append(data[i][0])
    return "query worked"
    items=cursor.fetchall()
    result = {'fields': fields, 'items': items, 'time': 0}
    return result'''
    query = request.args.get('query')
    connection = connect_rds()
    #return connection.perform_query(query)
    fields, items, time = connection.perform_query(query)
    result = {'fields': fields, 'items': items, 'time': time}
    connection.close()
    return result

@app.route('/mongodb')
def query_mongodb():
    query = request.args.get('query')
    connection = connect_drill()
    #connection = connect_mongo2()
    #return connection.perform_query(query)
    fields, items, time = connection.perform_query(query)
    result = {'fields': fields, 'items': items, 'time': time}
    connection.close()
    return result

@app.route('/')
def index():
    return render_template('index.html')
