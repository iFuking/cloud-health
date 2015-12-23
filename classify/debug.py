# encoding: utf-8
from wechat_sdk import WechatBasic
import urllib2
import socket
import json
import logging
import requests
import MySQLdb
import random


# ignore ssl InsecurePlatform warning
requests.packages.urllib3.disable_warnings()

# configure logging level
logging.basicConfig(level=logging.INFO)

# app_id & app_secret, generate access_token
app_id = 'wx1071ef65b25ab039'
app_secret = '235aaa4ed220afbf47af54939bebcff3'
wechat_basic_ins = WechatBasic(appid=app_id, appsecret=app_secret)


# check access token validity
def check_token_validity(token):
    wechat_server_api = 'https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s' % token
    # GET request
    request = urllib2.Request(wechat_server_api)
    try:
        response = urllib2.urlopen(request, timeout=1)
        content = response.read()
    except (urllib2.URLError, socket.timeout) as e:
        logging.error(e)
        print e

    dct = json.loads(content)
    if 'ip_list' in dct:
        logging.info('Valid access token.')
        print 'Valid access token.'
        return True
    logging.info('Invalid access token.')
    print 'Invalid access token.'
    return False


# get access token, server api
def get_access_token():
    refresh = 'false'
    while True:
        access_token_api = 'http://172.18.9.7/api/data/wechat-token?appId=%s&secret=%s&refresh=%s' % \
                           (app_id, app_secret, refresh)
        # GET request
        request = urllib2.Request(access_token_api)
        try:
            response = urllib2.urlopen(request, timeout=1)
            # response, json format access token if status=200
            # else response error
            content = response.read()

        # catch exception, not found host or connection timeout
        except (urllib2.URLError, socket.timeout) as e:
            logging.error(e)
            print e

        # json format response return
        dct = json.loads(content)
        if 'data' in dct and 'token' in dct['data']:
            token = dct['data']['token']

        # check the validity of access token
        if check_token_validity(token) is True:
            break
        else:
            refresh = 'true'
    logging.info('Access_token: %s' % token)
    print 'Access_token: %s' % token
    return token


access_token = get_access_token()


# recommend system, items included
RECOMMEND_ITEM = [
    'ask', 'book', 'checks', 'disease', 'drug',
    'food', 'lore', 'news', 'surgery', 'symptom'
]
# in different tables, column title differ
TITLE = [
    'title', 'name', 'name', 'name', 'name',
    'name', 'title', 'title', 'name', 'name'
]


# WechatBasic sdk, upload media & get media_id
# save valid media_id in file, update when expired
def get_media_id(img_path):
    # WechatBasic python sdk
    response = wechat_basic_ins.upload_media('image', open(img_path, 'r'))
    # response text, log for debug
    logging.info(response)
    print response
    if 'media_id' in response:
        media_id = response['media_id']
    logging.info('Media_id: %s' % media_id)
    print 'Media_id: %s' % media_id
    return media_id


# filter database & its cursor, encoding: utf8
db_filter = MySQLdb.connect(host='localhost', user='web', passwd='web', db='filter')
cursor_filter = db_filter.cursor()
db_filter.set_character_set('utf8')


def main():
    # send_msg()
    # send_apk()
    media_id = get_media_id('./img.jpg')
    print media_id
    return


if __name__ == '__main__':
    main()
