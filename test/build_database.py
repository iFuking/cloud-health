__author__ = 'dick'
import MySQLdb
import urllib2
import socket
import json

db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

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
        url = 'http://api.yi18.net/%s/show?id=%d' % (api_item[i], req_id)
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request, timeout=1)
            content = response.read()
            if len(content) < MIN_RESP_CONTENT_LENGTH:
                empty_resp += 1
                continue

            empty_resp = 0
            print url
            item = json.loads(content)
            req_id = item['yi18']['id']
            name = item['yi18'][names[i]]
            content = content.decode('utf8')

            SQL = "insert into yi18_" + api_item[i] + "(id, " + names[i] + ", content) values(%s, %s, %s)"
            cursor.execute(SQL, (req_id, name, content))
            db.commit()

        except urllib2.URLError as e:
            SQL = "insert into yi18_exception(item, id, info) values('%s', %d, '%s')" % (api_item[i], req_id, e)
            cursor.execute(SQL)
            db.commit()
            print type(e)
            continue
        except socket.timeout as e:
            SQL = "insert into yi18_exception(item, id, info) values('%s', %d, '%s')" % (api_item[i], req_id, e)
            cursor.execute(SQL)
            db.commit()
            print type(e)
            continue
        except ValueError as e:
            SQL = "insert into yi18_exception(item, id, info) values('%s', %d, '%s')" % (api_item[i], req_id, e)
            cursor.execute(SQL)
            db.commit()
            print type(e)
            continue
