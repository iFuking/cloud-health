import MySQLdb
import json
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import logging
import time

# yi18 database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='web', passwd='web', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

# filter database & its cursor, encoding: utf8
db_filter = MySQLdb.connect(host='localhost', user='web', passwd='web', db='filter')
cur_filter = db_filter.cursor()
db_filter.set_character_set('utf8')

logging.basicConfig(level=logging.INFO)

# database tables
table_name = [
    'ask', 'book', 'checks', 'disease', 'drug',
    'food', 'lore', 'news', 'surgery', 'symptom'
]
# table_name = ['book']

# in different tables, column name differ
name = [
    'title', 'name', 'name', 'name', 'name',
    'name', 'title', 'title', 'name', 'name'
]
class_name = [
    'classname', 'bookclass', 'menu', 'department', 'category',
    'menu', 'classname', 'tag', 'department', 'place'
]
# name = ['name']
# class_name = ['bookclass']
dct_value = {}


# parse json format function, key-value
def json_value(dct):
    for key in dct.keys():
        if ignore_tag(key):
            # type(d[k]) is also dict, call function recursively
            if isinstance(dct[key], dict):
                json_value(dct[key])
            # type(d[k]) is list, parse each node
            elif isinstance(dct[key], list):
                for it in dct[key]:
                    json_value(it)
            # until key-value structure, save it
            else:
                dct_value[key] = dct[key]
    return


ignore_key = [
    'img', 'from', 'author', 'count',
    'image', 'ANumber', 'PType', 'factory',
    'time', 'list'
]


# ignore some specify keys
def ignore_tag(tag):
    for k in ignore_key:
        if k == tag:
            return False
    return True


def chr_replace(content):
    content_tmp = ''
    for i in range(0, len(content)):
        if ord(content[i]) == 12288:
            continue
        elif i > 0 and ord(content[i]) == ord('\n') and ord(content[i]) == ord(content[i-1]):
            continue
        content_tmp += content[i]
    content = content_tmp.replace('\r', '').replace('\t', '').replace(' ', '')
    return content


def main():
    i = -1
    start_time = time.time()  # timestamp start time
    # main function & algorithm logic, build table one by one
    for table in table_name:
        i += 1
        # fetch a table's records
        sql = 'SELECT * FROM %s' % table
        cursor.execute(sql)
        results = cursor.fetchall()

        for record in results:
            # call json_value() function, parse json(content) & save pair<key, value>
            # filter the first time
            dct_value.clear()
            json_value(json.loads(record[3]))

            content = ''
            for key in dct_value.keys():
                # only unicode(string) included, int/long/bool.. ignored
                # filter the second time
                if isinstance(dct_value[key], unicode):
                    content += dct_value[key]

            # print content
            soup = BeautifulSoup(content)
            # beautiful soup get text (tag filter) & newline filter
            # filter the third time
            content_text = chr_replace(soup.getText())

            # jieba extract tags, return top5 key words & its weight
            tags = jieba.analyse.extract_tags(content_text, 5, True)
            keywords = weight = ''
            # words and weight separated by ','
            for word, w in tags:
                keywords += (word+',')
                weight += (str(w)+',')

            try:
                # sql = 'INSERT INTO %s_cache(id, content) ' % table + 'VALUES(%s, %s)'
                # cur_filter.execute(sql, (record[0], content))
                # db_filter.commit()

                sql = 'INSERT INTO %s(%s_id, %s, %s, keywords, weight, content) ' % (table, table, name[i], class_name[i]) + \
                      'VALUES(%s, %s, %s, %s, %s, %s)'
                cur_filter.execute(sql, (record[0], record[1], record[2], keywords, weight, content))
                db_filter.commit()

                logging.info(time.strftime('%Y/%m/%d %H:%M:%S--') +
                             'Building DATABASE `filter`, TABLE `%s` with id=%s finished.' %
                             (table, record[0]))

            except MySQLdb.IntegrityError as e:
                logging.error(time.strftime('%Y/%m/%d %H:%M:%S--') +
                              'In DATABASE `filter`, TABLE `%s` with id=%s, %s.' %
                              (table, record[0], e))
                continue

        time_now = time.time()
        logging.info('Total time cost: %ss.' % (time_now-start_time))


if __name__ == '__main__':
    main()
