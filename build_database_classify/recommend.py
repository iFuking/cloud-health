import MySQLdb
import urllib2
import socket
import json

# cloudtest database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='cloudtest')
cursor = db.cursor()
db.set_character_set('utf8')

# fetch all (id, open_id) pair from user table
SQL = 'SELECT id, open_id FROM user ORDER BY id ASC'
cursor.execute(SQL)
results = cursor.fetchall()

# classify database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='classify')
cursor = db.cursor()
db.set_character_set('utf8')

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
host = '172.18.9.7'

for record in results:
    uuid = record[0]     # user id
    open_id = record[1]  # wechat id

    # open api, fetch all reports using open_id
    url = 'http://%s/api/history?openId=%s&diagnose=true' % (host, open_id)
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request, timeout=1)
        # response, json format content
        content = response.read()

    # catch exception, not found host or connection timeout
    except (urllib2.URLError, socket.timeout) as e:
        continue

    dct = json.loads(content)
    bp = bmi = 'NORMAL'
    if 'data' in dct:
        for item in dct['data']:
            if 'bp' in item['result'] and item['result']['bp']['result'] != 'NORMAL':
                bp = item['result']['bp']['result']
                break

        for item in dct['data']:
            if 'bmi' in item['result'] and item['result']['bmi']['result'] != 'NORMAL':
                bmi = item['result']['bmi']['result']
                break

    disease_id = ''
    if bp != 'NORMAL':
        disease_id += '1,'
    if bmi != 'NORMAL':
        disease_id += '2,'
    if disease_id == '':
        continue

    try:
        SQL = 'INSERT INTO user_info(id, disease_id) VALUES(%s, %s)'
        cursor.execute(SQL, (uuid, disease_id))
        db.commit()
    except MySQLdb.IntegrityError as e:
        continue
