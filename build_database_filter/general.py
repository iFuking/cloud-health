import MySQLdb
import json
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import logging

# yi18 database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

# filter database & its cursor, encoding: utf8
db_filter = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='filter')
cur_filter = db_filter.cursor()
db_filter.set_character_set('utf8')

logging.basicConfig(level=logging.INFO)

# database tables
table_name = [
    'ask', 'book', 'checks', 'disease', 'drug',
    'food', 'lore', 'news', 'surgery', 'symptom'
]

# in different tables, column name differ
name = [
    'title', 'name', 'name', 'name', 'name',
    'name', 'title', 'title', 'name', 'name'
]
class_name = [
    'classname', 'bookclass', 'menu', 'department', 'category',
    'menu', 'classname', 'tag', 'department', 'place'
]


# parse json format function, key-value
def json_value(d):
    for k in d.keys():
        # type(d[k]) is also dict, call function recursively
        if isinstance(d[k], dict):
            json_value(d[k])
        # type(d[k]) is list, parse each node
        elif isinstance(d[k], list):
            for it in d[k]:
                json_value(it)
        # until key-value structure, save it
        else:
            dct_value[k] = d[k]
    return


ignore_key = ['img', 'author', 'time']


# ignore some specify keys
def ignore_tag(tag):
    for k in ignore_key:
        if k == tag:
            return False
    return True


# main function & algorithm logic, build table one by one
i = -1
for table in table_name:
    i += 1
    # fetch a table's records
    SQL = 'SELECT * FROM %s' % table
    cursor.execute(SQL)
    results = cursor.fetchall()

    for record in results:
        dct_value = {}
        # call json_value() function, parse json(content) & save pair<key, value>
        # filter the first time
        json_value(json.loads(record[3]))
        content = ''
        for key in dct_value.keys():
            # only unicode(string) included, int/long/bool.. ignored
            # filter the second time
            if ignore_tag(key) and isinstance(dct_value[key], unicode):
                content += dct_value[key]

        soup = BeautifulSoup(content)
        # beautiful soup get text (tag filter) & newline filter
        # filter the third time
        content = soup.getText().replace('\n', '')

        # jieba extract tags, return top5 key words & its weight
        tags = jieba.analyse.extract_tags(content, 5, True)
        keywords = weight = ''
        # words and weight separated by ','
        for word, w in tags:
            keywords += (word+',')
            weight += (str(w)+',')

        try:
            SQL = 'INSERT INTO %s(id, %s, %s, keywords, weight) ' % (table, name[i], class_name[i]) + \
                  'VALUES(%s, %s, %s, %s, %s)'
            cur_filter.execute(SQL, (record[0], record[1], record[2], keywords, weight))
            db_filter.commit()

            SQL = 'INSERT INTO %s_cache(id, content) ' % table + 'VALUES(%s, %s)'
            cur_filter.execute(SQL, (record[0], content))
            db_filter.commit()

            logging.info("Table %s with id=%s finished." % (table, record[0]))

        except MySQLdb.IntegrityError as e:
            logging.error('In table `%s` with id=%s, %s.' % (table, record[0], e))
            continue
