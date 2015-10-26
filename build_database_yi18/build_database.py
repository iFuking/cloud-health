import MySQLdb
import logging
import json

db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

home_path = '/home/dick/yi18'
logging.basicConfig(level=logging.INFO)

