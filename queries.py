from flask import Flask, request, render_template
from connection import connect_rds, connect_redshift

app = Flask(__name__)

@app.route('/redshift', methods=['GET'])
def query_redshift():
    query = request.args.get('query', 'show tables;')
    connection = connect_redshift(host='redshift-cluster-1.c9hlirpegyjx.us-east-2.redshift.amazonaws.com', port= '5439', user='admin101', password='Window12')
    fields, items, time = connection.perform_query(query)
    result = {'fields': fields, 'items': items, 'time': time}
    connection.close()
    return result

@app.route('/rds', methods=['GET'])
def query_rds():
    query = request.args.get('query', 'show tables;')
    connection = connect_rds(host='dev.cwhftiwcf2zq.us-east-2.rds.amazonaws.com', user='admin101',
                               password='Window12', db= 'database')
    fields, items, time = connection.perform_query(query)
    result = {'fields': fields, 'items': items, 'time': time}
    connection.close()
    return result

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
