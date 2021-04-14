import pymysql
import psycopg2
from pymongo import MongoClient
from pydrill.client import PyDrill
from drillpy import connect
import pandas
import time


class connect_redshift():
    def __init__(self):
        #self.con = psycopg2.connect(dbname= 'dev', host='redshift-cluster-1.c9hlirpegyjx.us-east-2.redshift.amazonaws.com', port= '5439',
        #                    user= 'admin101', password= 'Window12')
        self.con = psycopg2.connect(dbname= 'dev', host='redshift-cluster-1.cxhpbk96dqyo.us-east-1.redshift.amazonaws.com', port= '5439',
                            user= 'awsuser', password= 'CS527Group5')
        self.cur = self.con.cursor()
        return

    def close(self):
        self.con.commit()
        self.cur.close()
        self.con.close()
        return

    def perform_query(self, query):
        start = int(time.time() * 1000)
        self.cur.execute(query)
        data = self.cur.description
        try:
            items  = self.cur.fetchmany(1000)
        except:
            items = []
        total = int(time.time() * 1000) - start
        if len(items) == 1000:
            total = -total
        fields = []
        if data is not None:
            for i in range(len(data)):
                fields.append(data[i][0])
        return fields, items, total

class connect_rds():
    def __init__(self):
        self.db = pymysql.connect(host='database-2.csgrmq8cjzjf.us-east-1.rds.amazonaws.com',  user='admin',
                           password='CS527Group5', db= 'CS527' )
        self.db.autocommit(True)
        self.cursor = self.db.cursor()
        return

    def close(self):
        self.db.close()
        return

    def perform_query(self, query):
        start = int(time.time() * 1000)
        self.cursor.execute(query)
        data = self.cursor.description
        items  = self.cursor.fetchmany(1000)
        total = int(time.time() * 1000) - start
        if len(items) == 1000:
            total = -total
        fields = []
        if data is not None:
            for i in range(len(data)):
                fields.append(data[i][0])
        return fields, items, total

class connect_mongo():
    def __init__(self):
        self.client = MongoClient(host='') #, port=''
        self.db = self.client['instacart']
        return

    def close(self):
        self.client.close()
        return

    def perform_query(self, query): #query in mysql format

        return

    def convert_query(self, query):
        lower = query.lower()
        if not lower.find("select") == -1:
            ind = lower.find("select")
            if not ind == 0: #special case
                return #do something here
            else: #normal select query, select {cols} from {table} {condtions}
                #db.{table}.find({conditions})
                q = query[7:] #remove "select "
                f = lower.find("from") #remember spaces before and after from
                columns = q[:f-1] #leave off space
                if columns is "*":
                    columns = ""
                rest = query[f+5:] #table + conditions
                table = rest #will get changed if any conditions exist
                temp = rest.lower()
                conditions = None
                if not temp.find("where") == -1:
                    return
                if not temp.find("limit") == -1:
                    return
                if not temp.find("skip") == -1:
                    return
                #perform query
                collection = self.db[table]
                if conditions is None:
                    return collection.find()
                else:
                    return collection.find(conditions)

class connect_drill():
    def __init__(self):
        self.conn = connect(host='52.54.173.197',db='mongo.CS527', port=8047)# connect(host='3.141.153.121',db='mongo.data', port=8047)
        self.curs = self.conn.cursor()
        return

    def close(self):
        self.conn.commit()
        self.curs.close()
        self.conn.close()
        return

    def perform_query(self, query):
        start = int(time.time() * 1000)
        #return "test"
        curs = self.curs.execute(query)
        #data = self.curs.description
        items = curs.fetchmany(1000) #items is a pandas dataframe
        total = int(time.time() * 1000) - start
        if len(items.index) == 1000:
            total = -total
        fields = []
        if not items.empty:
            for i in items.columns:
                fields.append(i)
        vals = items.values.tolist()
        return fields, vals, total
