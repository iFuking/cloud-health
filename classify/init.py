import MySQLdb

db = MySQLdb.connect(host='localhost', user='web', passwd='web')
cursor = db.cursor()
db.set_character_set('utf8')

cursor.execute('DROP DATABASE IF EXISTS filter')
cursor.execute('CREATE DATABASE IF NOT EXISTS filter')
db.commit()