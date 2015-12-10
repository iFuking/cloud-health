import MySQLdb
import urllib2
import socket
import json

# cloudtest database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='web', passwd='web', db='cloudtest')
cursor = db.cursor()
db.set_character_set('utf8')

# fetch all (id, open_id) pair from user table
SQL = 'SELECT id, open_id FROM user ORDER BY id ASC'
cursor.execute(SQL)
results = cursor.fetchall()

# classify database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='web', passwd='web', db='classify')
cursor = db.cursor()
db.set_character_set('utf8')

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
host = '172.18.9.7'

cursor.execute('DELETE FROM user_info')
db.commit()


def get_diseases(bp, bmi):
    disease_ids = ''
    if bp != 'NORMAL':
        disease_ids += '1,'
    if bmi != 'NORMAL':
        disease_ids += '2,'
    return disease_ids


def get_complications(disease_ids):
    complications = ''
    disease_ids = disease_ids.split(',')
    for disease_id in disease_ids:
        if disease_id != '':
            sql = 'SELECT complications FROM complication WHERE id=%s'
            cursor.execute(sql, disease_id)
            res = cursor.fetchall()
            complications += res[0][0]
    return complications


def main():
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
                if 'BMI' in item['result'] and item['result']['BMI']['result'] != 'NORMAL':
                    bmi = item['result']['BMI']['result']
                    break

        disease_ids = get_diseases(bp, bmi)
        if disease_ids == '':
            continue
        complications = get_complications(disease_ids)

        try:
            sql = 'INSERT INTO user_info(open_id, disease_id, complications) VALUES(%s, %s, %s)'
            cursor.execute(sql, (open_id, disease_ids, complications))
            db.commit()
        except MySQLdb.IntegrityError as e:
            continue


if __name__ == "__main__":
    main()
