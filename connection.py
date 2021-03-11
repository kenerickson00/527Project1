import pymysql
import psycopg2
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
