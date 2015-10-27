import MySQLdb
import json
from bs4 import BeautifulSoup
import jieba
import jieba.analyse

# yi18 database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

# filter database & its cursor, encoding: utf8
db_filter = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='filter')
cur_filter = db_filter.cursor()
db_filter.set_character_set('utf8')

# database tables
table_name = [
    'ask', 'book', 'checks', 'disease', 'drug',
    'food', 'lore', 'news', 'surgery', 'symptom'
]

SQL = 'SELECT * FROM ask'
cursor.execute(SQL)
results = cursor.fetchall()

dct_value = {}


# parse json format function, key-value
def json_value(d):
    for k in d.keys():
        if isinstance(d[k], dict):
            json_value(d[k])
        elif isinstance(d[k], list):
            for it in d[k]:
                json_value(it)
        else:
            dct_value[k] = d[k]
    return


for record in results:

    json_value(json.loads(record[3]))
    content = ''
    for key in dct_value.keys():
        if isinstance(dct_value[key], unicode):
            content += dct_value[key]

    soup = BeautifulSoup(content)
    content = soup.getText().replace('\n', '')
    tags = jieba.analyse.extract_tags(content, 5, True)
    keywords = weight = ''
    for word, w in tags:
        keywords += (word+',')
        weight += (str(w)+',')

    SQL = 'INSERT INTO ask(id, title, classname, keywords, weight) VALUES(%s, %s, %s, %s, %s)'
    cur_filter.execute(SQL, (record[0], record[1], record[2], keywords, weight))
    db_filter.commit()

    SQL = 'INSERT INTO ask_cache(id, content) VALUES(%s, %s)'
    cur_filter.execute(SQL, (record[0], content))
    db_filter.commit()

    print 'Finish %d.' % record[0]
