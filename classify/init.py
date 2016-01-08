import MySQLdb
import time

db = MySQLdb.connect(host='localhost', user='web', passwd='web', db='filter')
cursor = db.cursor()
db.set_character_set('utf8')

table_name = [
    'ask', 'book', 'checks', 'disease', 'drug',
    'food', 'lore', 'news', 'surgery', 'symptom'
]

# for table in table_name:
#    sql = 'DELETE FROM %s' % table
#    cursor.execute(sql)
#    db.commit()
#    print time.strftime('%Y/%m/%d %H:%M:%S--') + 'Delete DATABASE `filter`, TABLE `%s` finished.' % table

#    sql = 'DELETE FROM %s_cache' % table
#    cursor.execute(sql)
#    db.commit()
#    print time.strftime('%Y/%m/%d %H:%M:%S--') + 'Delete DATABASE `filter`, TABLE `%s_cache` finished.' % table

cursor.execute('DROP DATABASE IF EXISTS filter')
cursor.execute('CREATE DATABASE IF NOT EXISTS filter')
