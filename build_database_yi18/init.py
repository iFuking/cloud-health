import MySQLdb

db = MySQLdb.connect(host='localhost', user='root', passwd='123456')
cursor = db.cursor()
db.set_character_set('utf8')

cursor.execute('DROP DATABASE IF EXISTS yi18')
cursor.execute('CREATE DATABASE IF NOT EXISTS yi18')
db.commit()

