import MySQLdb
from bs4 import BeautifulSoup
import jieba
import jieba.analyse

db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

SQL = 'SELECT * FROM ask'
cursor.execute(SQL)
results = cursor.fetchall()

db_filter = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='filter')
cur_filter = db_filter.cursor()
db_filter.set_character_set('utf8')

for record in results:
    soup = BeautifulSoup(record[3])
    content = soup.getText().encode('utf8')
    tags = jieba.analyse.extract_tags(content, 5, True)
    keywords = weight = ''
    for word, w in tags:
        keywords += (word+',')
        weight += (str(w)+',')

    keywords = keywords.encode('utf8')
    SQL = "INSERT INTO ask(id, title, classname, keywords, weight) VALUES(%s, %s, %s, %s, %s)"
    cur_filter.execute(SQL, (record[0], record[1], record[2], keywords, weight))
    db_filter.commit()

    print 'Finish %d.' % record[0]
