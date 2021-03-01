import pymysql
import psycopg2
from time import time


class connect_redshift():
    def __init__(self, host="", database='database', user='', password='', port=5439):
        self.con = psycopg2.connect(host=host, dbname=database, port=port, password=password, user=user)
        self.cur = self.con.cursor()
        return

    def close(self):
        self.cur.close()
        self.con.close()
        return

    def perform_query(self, query_statement):
        start = int(time() * 1000)
        self.cur.execute(query_statement)
        data = self.cur.description
        items = self.cur.fetchall()
        time = int(time() * 1000) - start
        fields = []
        for i in range(len(data)):
            fields.append(data[i][0])
        return fields, items, time

class connect_rds():
    def __init__(self, host="", user="", password="", db=""):
        self.db = pymysql.connect(host, user, password, db)
        self.cursor = self.db.cursor()
        return

    def close(self):
        self.db.close()
        return

    def perform_query(self, query_statement):
        start = int(time() * 1000)
        self.cursor.execute(query_statement)
        data = self.cursor.description
        items = self.cursor.fetchall()
        time = int(time() * 1000) - start
        fields = []
        for i in range(len(data)):
            fields.append(data[i][0])
        return fields, items, time
