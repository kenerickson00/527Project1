from flask import Flask, request, render_template
from connection import connect_rds, connect_redshift

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
    query = request.args.get('query')
    connection = connect_rds()
    fields, items, time = connection.perform_query(query)
    result = {'fields': fields, 'items': items, 'time': time}
    connection.close()
    return result

@app.route('/')
def index():
    return render_template('index.html')
