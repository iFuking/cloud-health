# encoding: utf-8
import MySQLdb
from pymongo import MongoClient
import json

mysql_db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='filter')
cursor = mysql_db.cursor()
mysql_db.set_character_set('utf8')

client = MongoClient()
mongo_db = client.test


def mysql2mongo():
    sql = 'SHOW TABLES'
    cursor.execute(sql)
    table_name = cursor.fetchall()

    for table in table_name:
        collection = mongo_db['f_'+table[0]+'2s']

        sql = 'SHOW COLUMNS FROM %s' % table[0]
        cursor.execute(sql)
        columns = cursor.fetchall()

        sql = 'SELECT * FROM %s' % table[0]
        cursor.execute(sql)
        records = cursor.fetchall()
        for r in records:
            dct = {}
            for i in range(0, len(columns)):
                dct[columns[i][0]] = r[i]
            collection.insert_one(dct)
    return


def main():
    mysql2mongo()
    return


if __name__ == '__main__':
    main()
