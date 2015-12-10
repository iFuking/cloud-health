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

    dct = json.loads(content)
    if 'ip_list' in dct:
        logging.info('Valid access token.')
        return True
    logging.info('Invalid access token.')
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
    return token


# wechat dev api, get access token
# def get_access_token():
#     # access token item
#     item = 'access_token'
#
#     # wechat access token api usage
#     access_token_api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
#                        (app_id, app_secret)
#     # GET request
#     request = urllib2.Request(access_token_api)
#     try:
#         response = urllib2.urlopen(request, timeout=1)
#         # response, json format access token if status=200
#         # else response error
#         content = response.read()
#
#     # catch exception, not found host or connection timeout
#     except (urllib2.URLError, socket.timeout) as e:
#         logging.error(e)
#
#     # json format response return
#     dct = json.loads(content)
#     if item in dct:
#         logging.info('Get access token successfully!')
#         return dct[item]
#     else:
#         logging.warning('Failed to get access token.')
#         return ''


# get access token, ensure access token valid
# def get_access_token():
#     access_token_path = './access_token'
#     # store access token in file
#     if not os.path.exists(access_token_path):
#         write_file = open(access_token_path, 'w')
#         write_file.write('null\n-1\n')
#         write_file.close()
#
#     # read access token file
#     read_file = open(access_token_path)
#     token = read_file.readline()
#     # last 7200 seconds since GET request to wechat server
#     expire_time = read_file.readline()
#
#     # update access token if expired
#     current_time = int(time.time())
#     if expire_time == '' or current_time > int(expire_time)-100:
#         response = wechat_basic_ins.get_access_token()
#         token = response['access_token']
#         expire_time = response['access_token_expires_at']
#         write_file = open(access_token_path, 'w')
#         write_file.write(token+'\n'+str(expire_time)+'\n')
#         write_file.close()
#     return token


# global variable, get access token
access_token = get_access_token()


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
#         logging.info('Get user list successfully!')
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
        logging.info('Get group list successfully!')
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
db = MySQLdb.connect(host='localhost', user='web', passwd='web', db='classify')
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

            for record in results:
                wechat_basic_ins.move_user(record[0], group['id'])
            break

            # open_id_list = []
            # for record in results:
            #     open_id_list.append(record[0])
            # # move bunches of users
            # move_user_list(open_id_list, group['id'])
    return


def grouping():
    init_group()
    create_groups()
    move_users()
    return


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
def get_media_id(item):
    img_path = '../image/%s.jpg' % item
    # WechatBasic python sdk
    response = wechat_basic_ins.upload_media('image', open(img_path, 'r'))
    # response text, log for debug
    logging.info(response)
    if 'media_id' in response:
        media_id = response['media_id']
    logging.info('Media_id: %s' % media_id)
    return media_id

# def get_media_id(item):
#     # media_id file path
#     file_path = '../request_param/media_id/%s' % item
#     if not os.path.exists(file_path):
#         # create file
#         write_file = open(file_path, 'w')
#         write_file.close()
#
#     # read media_id file
#     read_file = open(file_path, 'r')
#     # media_id & expire time (lasting three days, 3*24*3600 seconds)
#     media_id = read_file.readline()
#     expire_time = read_file.readline()
#
#     # update media_id if expired or expire_time invalid
#     current_time = int(time.time())
#     if expire_time == '' or current_time > int(expire_time)-3600:
#         img_path = '../image/%s.jpg' % item
#         # WechatBasic python sdk
#         response = wechat_basic_ins.upload_media('image', open(img_path, 'r'))
#         # response text, log for debug
#         logging.info(response)
#         if 'media_id' in response:
#             # generate media_id & expire time
#             media_id = response['media_id']
#             expire_time = response['created_at']+3*24*3600
#             logging.info('Update media_id and expire time.')
#             # write file
#             write_file = open(file_path, 'w')
#             write_file.write(media_id+'\n'+str(expire_time)+'\n')
#             write_file.close()
#             logging.info('Save media_id and expire time in file %s' % file_path)
#     logging.info('Media_id: %s' % media_id)
#     return media_id


# filter database & its cursor, encoding: utf8
db_filter = MySQLdb.connect(host='localhost', user='web', passwd='web', db='filter')
cursor_filter = db_filter.cursor()
db_filter.set_character_set('utf8')

# digest len
DIGEST_LENGTH = 67


# wechat dev api, get article_id
# def get_article_id(item_index, item_id):
#     # article_id file path
#     file_path = '../request_param/article_id/%s' % RECOMMEND_ITEM[item_index]
#     if not os.path.exists(file_path):
#         # create file
#         write_file = open(file_path, 'w')
#         write_file.close()
#
#     # read article_id file
#     read_file = open(file_path, 'r')
#     # article_id & expire time (lasting three days, 3*24*3600 seconds)
#     article_id = read_file.readline()
#     expire_time = read_file.readline()
#
#     # update media_id if expired or expire_time invalid
#     current_time = int(time.time())
#     if expire_time == '' or current_time > int(expire_time)-3600:
#         # get media_id
#         # media_id = get_media_id(RECOMMEND_ITEM[item_index])
#         media_id = 'debug'
#
#         # get title from database `filter`, table `RECOMMEND_ITEM[item_index]`
#         sql = 'SELECT '+TITLE[item_index]+' FROM '+RECOMMEND_ITEM[item_index]+' WHERE id=%s'
#         cursor_filter.execute(sql, item_id)
#         res = cursor_filter.fetchall()
#         # fetch result as title
#         title = res[0][0]
#
#         # get content from database `filter`, table `RECOMMEND_ITEM[item_index]_cache`
#         sql = 'SELECT content FROM '+RECOMMEND_ITEM[item_index]+'_cache WHERE id=%s'
#         cursor_filter.execute(sql, item_id)
#         res = cursor_filter.fetchall()
#         # fetch result as content
#         content = res[0][0]
#
#         # get digest, simplify content
#         digest = ''
#         if len(content) > DIGEST_LENGTH:
#             digest = content[:DIGEST_LENGTH]
#
#         article_id_api = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s' % access_token
#         # POST data format(json) & data example
#         data = """{
#             "articles": [
#                 {
#                     "thumb_media_id": "%s",
#                     "author": "chmwang",
#                     "title": "%s",
#                     "content_source_url": "www.jtang.cn",
#                     "content": "%s",
#                     "digest": "%s",
#                     "show_cover_pic": "1"
#                 }
#             ]
#         }""" % (media_id, title, content, digest)
#         print data
#         # POST request, json format `str`
#         response = requests.post(article_id_api, data)
#         # response text, log for debug
#         logging.info(response.text)
#         dct = json.loads(response.text)
#         if 'media_id' in dct:
#             # generate article_id & expire time
#             article_id = dct['media_id']
#             expire_time = dct['created_at']+3*24*3600
#             logging.info('Update article_id and expire time.')
#             # write file
#             write_file = open(file_path, 'w')
#             write_file.write(media_id+'\n'+str(expire_time)+'\n')
#             write_file.close()
#             logging.info('Save article_id and expire time in file %s' % file_path)
#     logging.info('Article_id: %s' % article_id)
#     return article_id

def get_article_id(item_index, item_id):
    # get media_id
    media_id = str(get_media_id(RECOMMEND_ITEM[item_index]))
    # media_id = 'YrZBy4tLVHmVd32SstiYN_R4aCtOxYVVR2kVJJiide8m-vjNceDcxl6r_7Fy2Tzz'
    # get title from database `filter`, table `RECOMMEND_ITEM[item_index]`
    sql = 'SELECT '+TITLE[item_index]+' FROM '+RECOMMEND_ITEM[item_index]+' WHERE id=%s'
    cursor_filter.execute(sql, item_id)
    res = cursor_filter.fetchall()
    # fetch result as title
    title = res[0][0]

    # get content from database `filter`, table `RECOMMEND_ITEM[item_index]_cache`
    sql = 'SELECT content FROM '+RECOMMEND_ITEM[item_index]+'_cache WHERE id=%s'
    cursor_filter.execute(sql, item_id)
    res = cursor_filter.fetchall()
    # fetch result as content
    content = res[0][0]

    # get digest, simplify content
    digest = title

    article_id_api = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s' % access_token
    # POST data format(json) & data example
    data = """{
        "articles": [
            {
                "thumb_media_id": "%s",
                "author": "chmwang",
                "title": "%s",
                "content_source_url": "www.jtang.cn",
                "content": "%s",
                "digest": "%s",
                "show_cover_pic": "1"
            }
        ]
    }""" % (media_id, title, content, digest)
    # POST request, json format `str`
    response = requests.post(article_id_api, data)
    # response text, log for debug
    logging.info(response.text)
    dct = json.loads(response.text)
    article_id = ''
    if 'media_id' in dct:
        # generate article_id
        article_id = dct['media_id']
    logging.info('Article_id: %s' % article_id)
    return article_id


# send message to users
# query database, grouping users according to disease
# wechat dev api, send message using open_id list
def send_msg():
    # group users by disease_id
    sql = 'SELECT disease_id FROM user_info GROUP BY disease_id'
    cursor.execute(sql)
    results = cursor.fetchall()

    for record in results:
        # for each group, generate open_id list
        sql = 'SELECT open_id, complications FROM user_info WHERE disease_id=%s'
        cursor.execute(sql, record[0])
        res = cursor.fetchall()
        open_id_list = []
        for r in res:
            open_id_list.append(r[0])
        # nickname: chmwang, append to each group
        open_id_list.append('o8AvqvsA4EPC6HkAfIz-lQOJUl-0')

        # candidate disease list
        disease_id_list = record[0]+res[0][1]
        # parse disease_id to type list & remove the last element
        disease_id_list = disease_id_list.split(',')
        disease_id_list.pop()

        # randomly decide which disease to recommend
        disease_id = disease_id_list[random.randint(0, len(disease_id_list)-1)]

        # iterate until disease_info_column not null
        while True:
            # randomly decide which column to choose in table `disease_info`
            recommend_item_index = random.randint(0, len(RECOMMEND_ITEM)-1)

            # fetch such disease_info column with specific disease_id
            # return list of related results, for example, book results(id=1, 2, ..)
            sql = 'SELECT '+RECOMMEND_ITEM[recommend_item_index]+' FROM disease_info WHERE id=%s'
            cursor.execute(sql, disease_id)
            r = cursor.fetchall()
            if len(r[0][0]) > 0:
                break

        # related result list
        item_id_list = r[0][0].split(',')
        item_id_list.pop()
        # choose only one in these results
        item_id = item_id_list[random.randint(0, len(item_id_list)-1)]

        # get article_id
        article_id = get_article_id(recommend_item_index, item_id)

        send_msg_api = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s' % access_token
        data = {
            'touser': ['o8AvqvsA4EPC6HkAfIz-lQOJUl-0', 'o8AvqvsA4EPC6HkAfIz-lQOJUl-0'],
            'mpnews': {
                'media_id': article_id
            },
            'msgtype': 'mpnews'
        }
        # POST request, json format
        response = requests.post(send_msg_api, json.dumps(data))
        # response text, log for debug
        logging.info(response.text)
    return


def main():
    # grouping()
    send_msg()
    return


if __name__ == '__main__':
    main()
