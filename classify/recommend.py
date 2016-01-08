from pymongo import MongoClient
import urllib2
import socket
import json

client = MongoClient()
db = client.test

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
host = '172.18.9.7'


def get_diseases(bp, bmi):
    disease_ids = ''
    if bp != 'NORMAL':
        disease_ids += '1,'
    if bmi != 'NORMAL':
        disease_ids += '2,'
    return disease_ids


def get_complications(disease_ids):
    complications = str()
    disease_ids = disease_ids.split(',')
    disease_ids.pop()
    for disease_id in disease_ids:
        # sql = 'SELECT complications FROM complication WHERE disease_id=%s'
        # cursor.execute(sql, disease_id)
        # res = cursor.fetchall()
        # complications += res[0][0]
        res = db['w_complication2s'].find({'disease_id': int(disease_id)})
        complications += res[0]['complications']
    return complications


def init_db_collection():
    db['w_user_info2s'].drop()
    return


def classify_user():

    results = db['guests'].find()
    for record in results:

        open_id = record['openId']

        # open api, fetch all reports using open_id
        url = 'http://%s/api/history?openId=%s&diagnose=true' % (host, open_id)
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request, timeout=1)
            # response, json format content
            content = response.read()

        # catch exception, not found host or connection timeout
        except (urllib2.URLError, socket.timeout) as e:
            print e
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

        dct = dict()
        dct['open_id'] = open_id
        dct['disease_id'] = disease_ids
        dct['complications'] = complications
        db['w_user_info2s'].insert_one(dct)
    return


def main():
    init_db_collection()
    classify_user()
    return


if __name__ == "__main__":
    main()
