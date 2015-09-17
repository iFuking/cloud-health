__author__ = 'dick'
import MySQLdb
import json

db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

MIN_RESP_CONTENT_LENGTH = 81
EMPTY_RESP_NUM = 100

api_item = [
    'disease', 'symptom', 'check', 'surgery',
    'lore', 'ask', 'book',
    'drug', 'food', 'cook',
    'news'
]
names = [
    'name', 'name', 'name', 'name',
    'title', 'title', 'name',
    'name', 'name', 'name',
    'title'
]

for i in range(0, len(api_item)):
    req_id = 0
    empty_resp = 0

    while True:
        if empty_resp > EMPTY_RESP_NUM:
            break
        req_id += 1
        try:
            file_name = '/home/dick/tmp/%s/%d.txt' % (api_item[i], req_id)
            read_file = open(file_name)
            content = read_file.read()

            empty_resp = 0
            print file_name
            item = json.loads(content)
            req_id = item['yi18']['id']
            name = item['yi18'][names[i]]
            content = content.decode('utf8')

            SQL = "insert into yi18_" + api_item[i] + "(id, " + names[i] + ", content) values(%s, %s, %s)"
            cursor.execute(SQL, (req_id, name, content))
            db.commit()

        except IOError as e:
            print type(e)
            empty_resp += 1
            SQL = "insert into yi18_exception(item, id, info) values(%s, %s, %s)"
            cursor.execute(SQL, (api_item[i], req_id, e))
            db.commit()
            continue
        except ValueError as e:
            print type(e)
            SQL = "insert into yi18_exception(item, id, info) values('%s', %d, '%s')" % (api_item[i], req_id, e)
            cursor.execute(SQL)
            db.commit()
            continue

        finally:
            read_file.close()

    SQL = "delete from yi18_exception where item='%s' and id>%d" % (api_item[i], req_id-EMPTY_RESP_NUM-1)
    cursor.execute(SQL)
    db.commit()
