from pymongo import MongoClient
import urllib2
import socket
import json
import logging


# configure logging level
logging.basicConfig(level=logging.INFO)

client = MongoClient()
db = client.test
host = '172.18.9.7'


# disease grouped by diagnose
def get_diseases(bp, bmi, jizhui, zangfu, xiaohua, miniao):
    disease_ids = ''
    if bp != 'NORMAL':
        disease_ids += '1,'
    if bmi != 'NORMAL':
        disease_ids += '2,'
    if jizhui != 'NORMAL':
        disease_ids += '3,'
    if zangfu != 'NORMAL':
        disease_ids += '4,'
    if xiaohua != 'NORMAL':
        disease_ids += '5,'
    if miniao != 'NORMAL':
        disease_ids += '6,'
    return disease_ids


# def get_complications(disease_ids):
#     complications = str()
#     disease_ids = disease_ids.split(',')
#     disease_ids.pop()
#     for disease_id in disease_ids:
#         # sql = 'SELECT complications FROM complication WHERE disease_id=%s'
#         # cursor.execute(sql, disease_id)
#         # res = cursor.fetchall()
#         # complications += res[0][0]
#         res = db['w_complication2s'].find({'disease_id': int(disease_id)})
#         complications += res[0]['complications']
#     return complications


def init_db_collection():
    db['w_user_info2s'].drop()
    logging.info('Initial/Drop collection `w_user_info2s`.')
    return


# parse diagnose result, json object
def diagnose(dct, bp, bmi, jizhui, zangfu, xiaohua, miniao):
    if 'data' in dct and 'data' in dct['data']:
        for item in dct['data']['data']:
            if 'bp' in item['others'] and item['others']['bp']['result'] != 'NORMAL':
                bp = item['others']['bp']['result']
                break

        for item in dct['data']['data']:
            if 'BMI' in item['others'] and item['others']['BMI']['result'] != 'NORMAL':
                bmi = item['others']['BMI']['result']
                break

        for item in dct['data']['data']:
            if 'jizhui' in item and item['jizhui']['result'] != 'NORMAL':
                jizhui = item['jizhui']['result']
                break

        for item in dct['data']['data']:
            if 'zangfu' in item and item['zangfu']['result'] != 'NORMAL':
                zangfu = item['zangfu']['result']
                break

        for item in dct['data']['data']:
            if 'xiaohua' in item and item['xiaohua']['result'] != 'NORMAL':
                xiaohua = item['xiaohua']['result']
                break

        for item in dct['data']['data']:
            if 'miniao' in item and item['miniao']['result'] != 'NORMAL':
                miniao = item['miniao']['result']
                break
    return bp, bmi, jizhui, zangfu, xiaohua, miniao


def classify_user():

    # results = db['guests'].find()
    results = ['o8AvqvqYPNJxXMSPOiXSEFjbxsVs']
    for record in results:

        # open_id = record['openId']
        open_id = 'o8AvqvqYPNJxXMSPOiXSEFjbxsVs'

        # open api, fetch all reports using open_id
        url = 'http://%s/api/reports?openId=%s&diagnose=true' % (host, open_id)
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request, timeout=1)
            # response, json format content
            content = response.read()

        # catch exception, not found host or connection timeout
        except (urllib2.URLError, socket.timeout) as e:
            logging.error(e)
            print e
            continue

        dct = json.loads(content)
        bp = bmi = jizhui = zangfu = xiaohua = miniao = 'NORMAL'

        bp, bmi, jizhui, zangfu, xiaohua, miniao = diagnose(dct, bp, bmi, jizhui, zangfu, xiaohua, miniao)
        disease_ids = get_diseases(bp, bmi, jizhui, zangfu, xiaohua, miniao)
        if disease_ids == '':
            continue
        complications = ''

        dct = dict()
        dct['open_id'] = open_id
        dct['disease_id'] = disease_ids
        dct['complications'] = complications
        db['w_user_info2s'].insert_one(dct)
    logging.info('Finish classify user.')
    return


def main():
    init_db_collection()
    classify_user()
    return


if __name__ == "__main__":
    main()
