# encoding: utf-8
from wechat_sdk import WechatBasic
from pymongo import MongoClient
import json
import urllib2
import socket
import logging

app_id = 'wx1071ef65b25ab039'
app_secret = '235aaa4ed220afbf47af54939bebcff3'
wechat_basic_ins = WechatBasic(appid=app_id, appsecret=app_secret)


# configure logging level
logging.basicConfig(level=logging.INFO)

client = MongoClient()
db = client.test


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

# def wx_group():
#     disease_id = [1, 2, 3, 4, 5, 6]
#     for i in range(1, 64):
#         mirror_i = i
#         s = str()
#         cnt = 0
#         while mirror_i > 0:
#             digit = mirror_i & 1
#             if digit > 0:
#                 s += str(disease_id[cnt])+','
#             cnt += 1
#             mirror_i >>= 1
#         print s
#     return

def wx_find_group(group_name):
    response = wechat_basic_ins.get_groups()
    for record in response['groups']:
        if record['name'] == group_name:
            logging.info('Find group %s, group_id=%d' % (group_name, record['id']))
            return True, record['id']
    logging.info('No such group %s' % group_name)
    return False, -1

def wx_create_group(group_name):
    response = wechat_basic_ins.create_group(group_name)
    logging.info(response)
    return

def wx_move_user_to_group(open_id, group_id):
    response = wechat_basic_ins.update_group(open_id, group_id)
    logging.info(response)
    return

def wx_group():
    # fetch all records of collection `w_user_info2s`
    results = db['w_user_info2s'].find()
    for record in results:
        # open_id and group name
        group_name = record['disease_id']
        open_id = record['open_id']

        # find if group name exists in wechat management platform
        have_group, group_id = wx_find_group(group_name)
        if have_group is False:
            # create such group if group name not exists
            wx_create_group(group_name)
        # move user to specific group, finish user classify
        wx_move_user_to_group(open_id, group_id)
    return

def main():
    wx_group()
    return

if __name__ == '__main__':
    main()
