import MySQLdb

db = MySQLdb.connect(host='localhost', user='root', passwd='123456')
cursor = db.cursor()
db.set_character_set('utf8')

cursor.execute('DROP DATABASE IF EXISTS classify')
cursor.execute('CREATE DATABASE IF NOT EXISTS classify')
db.commit()
