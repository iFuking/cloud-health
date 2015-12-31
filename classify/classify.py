# encoding: utf-8
import MySQLdb

# filter database & its cursor, encoding: utf8
db_filter = MySQLdb.connect(host='localhost', user='web', passwd='web', db='filter')
cur_filter = db_filter.cursor()
db_filter.set_character_set('utf8')

# classify database & its cursor, encoding: utf8
db_classify = MySQLdb.connect(host='localhost', user='web', passwd='web', db='classify')
cur_classify = db_classify.cursor()
db_classify.set_character_set('utf8')

# disease list
DISEASE_NAME = [
    '血压', '肥胖',
    '中风', '心脏病', '血管瘤', '肾衰竭',
    '糖尿病', '冠心病', '血脂',
    '肠炎', '肺结核', '肿瘤',
    '甲状腺'
]

# database tables | disease_info table's column
TABLE_NAME = [
    'ask', 'book', 'checks', 'disease', 'drug',
    'food', 'lore', 'news', 'surgery', 'symptom'
]

# query item
KEY_WORDS = [
    'keywords', 'keywords', 'menu', 'keywords', 'category',
    'keywords', 'keywords', 'keywords', 'keywords', 'keywords'
]


def main():
    # execute only once
    for name in DISEASE_NAME:
        try:
            sql = 'INSERT INTO disease_info(name) VALUES(%s)'
            cur_classify.execute(sql, name)
            db_classify.commit()
        except MySQLdb.IntegrityError as e:
            continue

    for name in DISEASE_NAME:
        i = -1
        print 'Disease ' + name
        for table in TABLE_NAME:
            i += 1
            # fetch disease_name-like keywords
            sql = 'SELECT %s_id FROM %s WHERE %s ' % (table, table, KEY_WORDS[i]) \
                  + 'LIKE %s'
            cur_filter.execute(sql, '%'+name+'%')
            results = cur_filter.fetchall()

            col = ''
            for res in results:
                col += str(res[0])+','
            # update column according to disease name
            sql = 'UPDATE disease_info SET %s=' % table + '%s WHERE name=%s'
            cur_classify.execute(sql, (col, name))
            db_classify.commit()

            print 'Table ' + table


if __name__ == '__main__':
    main()
