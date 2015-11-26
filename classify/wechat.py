__author__ = 'dick'
import urllib2
import socket
import json
import logging
import requests
import MySQLdb
from wechat_sdk import WechatBasic

# ignore ssl InsecurePlatform warning
requests.packages.urllib3.disable_warnings()

# configure logging level
logging.basicConfig(level=logging.INFO)

# app_id & app_secret, generate access_token
app_id = 'wx1071ef65b25ab039'
app_secret = '235aaa4ed220afbf47af54939bebcff3'


# wechat dev api, get access token
def get_access_token():
    # access token item
    item = 'access_token'

    # wechat access token api usage
    access_token_api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
                       (app_id, app_secret)
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

    # json format response return
    dct = json.loads(content)
    if item in dct:
        logging.info('GET access token successfully!')
        return dct[item]
    else:
        logging.warning('Failed to GET access token.')
        return ''


# global variable, get access token
# access_token = get_access_token()
access_token = 'p8fqGPiafgOvUD8m5XmbD6S9_5NFwIzVOasN9dzEAXJeJEKC1sL1nF_C-P3AEir_7Ly2fc_JieyqhWWCibJos2W9AXxmaW1G0' + \
               'herMOT5cowHBVcAFAUOI'
logging.info('Access_token: %s' % access_token)


# wechat dev api, move user to the specific group
def move_user(open_id, group_id):
    move_user_api = 'https://api.weixin.qq.com/cgi-bin/groups/members/update?access_token=%s' % access_token
    # POST data format(json) & data example
    data = {'openid': open_id, 'to_groupid': group_id}
    # POST request, json format
    response = requests.post(move_user_api, json.dumps(data))
    dct = json.loads(response.text)
    # check POST response message
    if 'errcode' in dct and dct['errcode'] == 0:
        logging.info('Move user `%s` to group %d successfully!' % (open_id, group_id))
    else:
        logging.warning('Failed to move user `%s` to group %d.' % (open_id, group_id))
    return


# wechat dev api, get all users' open_id
# def get_user_list():
#     user_list_api = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % access_token
#     # GET request
#     request = urllib2.Request(user_list_api)
#     try:
#         response = urllib2.urlopen(request, timeout=1)
#         # response, json format user list
#         content = response.read()
#
#     # catch exception, not found host or connection timeout
#     except (urllib2.URLError, socket.timeout) as e:
#         logging.error(e)
#
#     # json format response return
#     dct = json.loads(content)
#     user_list = []
#     if 'data' in dct and 'openid' in dct['data']:
#         # get user open_id list
#         user_list = dct['data']['openid']
#         logging.info('GET user list successfully!')
#     return user_list


# wechat dev api, get all groups' structure(id, name, count)
def get_group_list():
    group_list_api = 'https://api.weixin.qq.com/cgi-bin/groups/get?access_token=%s' % access_token
    # GET request
    request = urllib2.Request(group_list_api)
    try:
        response = urllib2.urlopen(request, timeout=1)
        # response, json format group list
        content = response.read()

    # catch exception, not found host or connection timeout
    except (urllib2.URLError, socket.timeout) as e:
        logging.error(e)

    # json format response return
    dct = json.loads(content)
    group_list = []
    if 'groups' in dct:
        # get group (id, name, count) list
        group_list = dct['groups']
        logging.info('GET group list successfully!')
    return group_list


# wechat dev api, delete group
def delete_group(group_id):
    delete_group_api = 'https://api.weixin.qq.com/cgi-bin/groups/delete?access_token=%s' % access_token
    # POST data format(json) & data example
    data = {"group": {"id": group_id}}
    # POST request, json format
    response = requests.post(delete_group_api, json.dumps(data))
    dct = json.loads(response.text)
    if 'errcode' in dct:
        logging.warning('Failed to delete group %d' % group_id)
    else:
        logging.info('Delete group %d successfully!' % group_id)
    return


# delete non-system groups, whose group id > 2
def delete_nonsys_group():
    # firstly, get all groups
    group_list = get_group_list()
    for group in group_list:
        # keep system groups, id = 0, 1, 2
        if group['id'] > 2:
            delete_group(group['id'])
    return


# init group: move all users to default group & delete all non-system groups
def init_group():
    # # move all users to default group
    # user_list = get_user_list()
    # for user in user_list:
    #     move_user(user, 0)

    # delete all non-system groups
    # users in these non-system groups will be moved to default group id=0
    delete_nonsys_group()
    return


# cloudtest database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='classify')
cursor = db.cursor()
db.set_character_set('utf8')


# wechat dev api, create a group
def create_group(group_name):
    create_group_api = 'https://api.weixin.qq.com/cgi-bin/groups/create?access_token=%s' % access_token
    # POST data format(json) & data example
    data = {"group": {"name": group_name}}
    # POST request, json format
    response = requests.post(create_group_api, json.dumps(data))
    dct = json.loads(response.text)
    if 'group' in dct:
        logging.info('Create group `%s` successfully!' % group_name)
    else:
        logging.info('Failed to create group `%s`.' % group_name)
    return


# create groups according to
# database `classify`, table `user_info`, columns `disease_id`
def create_groups():
    # mysql operation, get records group by disease_id
    sql = 'SELECT disease_id FROM user_info GROUP BY disease_id'
    cursor.execute(sql)
    results = cursor.fetchall()

    # create each group
    for record in results:
        create_group(record[0])
    return


# wechat dev api, move user list
def move_user_list(open_id_list, group_id):
    move_user_list_api = 'https://api.weixin.qq.com/cgi-bin/groups/members/batchupdate?access_token=%s' % access_token
    # POST data format(json) & data example
    data = {'openid_list': open_id_list, 'to_groupid': group_id}
    # POST request, json format
    response = requests.post(move_user_list_api, json.dumps(data))
    dct = json.loads(response.text)
    # check POST response message
    if 'errcode' in dct and dct['errcode'] == 0:
        logging.info('Move users `%s` to group %d successfully!' % (open_id_list, group_id))
    else:
        logging.warning('Failed to move users `%s` to group %d.' % (open_id_list, group_id))
    return


# move each user to specific group
def move_users():
    # get non_system group (id > 2)
    group_list = get_group_list()

    # for each group, query database to find which user belong to
    for group in group_list:
        if group['id'] > 2:
            sql = 'SELECT open_id FROM user_info where disease_id=%s'
            cursor.execute(sql, group['name'])
            # users' open_id list in the same group
            results = cursor.fetchall()
            # for record in results:
            #     move_user(record[0], group['id'])
            open_id_list = []
            for record in results:
                open_id_list.append(record[0])
            # move bunches of users
            move_user_list(open_id_list, group['id'])
    return


def grouping():
    init_group()
    create_groups()
    move_users()
    return


# WechatBasic sdk
def get_media_id():
    # create wechat basic instance, param: app_id & app_secret
    wechat_basic_ins = WechatBasic(appid=app_id, appsecret=app_secret)
    # WechatBasic python sdk
    response = wechat_basic_ins.upload_media('image', open('./img.jpg', 'r'))
    media_id = ''
    if media_id in response:
        media_id = response['media_id']
    return media_id


def send_msg():
    media_id = 'cWmZ17UuNi_LlPdqRF3K-B1LWjjrfLW_bKJhWVnc_6Rwd7JGi8onDOSB4iwWcpN7'

    return


def main():
    # grouping()
    send_msg()
    return


if __name__ == "__main__":
    main()