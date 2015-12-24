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


# def _get_access_token():
#     # app_id & app_secret, generate access_token
#
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
#         logging.info('GET access token successfully!')
#         return dct[item]
#     else:
#         logging.warning('Failed to GET access token.')
#         return ''


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


def get_article_resp(media_id, title, source_url, content, digest):
    article_id_api = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s' % access_token
    # POST data format(json) & data example
    data = """{
        "articles": [
            {
                "thumb_media_id": "%s",
                "author": "cloud-health",
                "title": "%s",
                "content_source_url": "%s",
                "content": "%s",
                "digest": "%s",
                "show_cover_pic": "1"
            }
        ]
    }""" % (media_id, title, source_url, content, digest)
    # POST request, json format `str`
    response = requests.post(article_id_api, data)

    # response text, log for debug
    logging.info(response.text)
    print response.text
    return response


def get_article_id(item_index, item_id):
    # get media_id
    media_id = str(get_media_id('../image/%s.jpg' % RECOMMEND_ITEM[item_index]))
    # get title from database `filter`, table `RECOMMEND_ITEM[item_index]`
    sql = 'SELECT '+TITLE[item_index]+' FROM '+RECOMMEND_ITEM[item_index]+' WHERE id=%s'
    cursor_filter.execute(sql, item_id)
    res = cursor_filter.fetchall()
    # fetch result as title
    title = res[0][0]
    print 'Title: ' + title

    # get content from database `filter`, table `RECOMMEND_ITEM[item_index]_cache`
    sql = 'SELECT content FROM '+RECOMMEND_ITEM[item_index]+'_cache WHERE id=%s'
    cursor_filter.execute(sql, item_id)
    res = cursor_filter.fetchall()
    # fetch result as content
    content = res[0][0]

    # get digest, simplify content
    digest = title

    # POST request, json format `str`
    response = get_article_resp(media_id, title, 'www.jtang.cn', content, digest)

    dct = json.loads(response.text)
    article_id = ''
    if 'media_id' in dct:
        # generate article_id
        article_id = dct['media_id']
    logging.info('Article_id: %s' % article_id)
    print 'Article_id: %s' % article_id
    return article_id


# cloudtest database & its cursor, encoding: utf8
db_classify = MySQLdb.connect(host='localhost', user='web', passwd='web', db='classify')
cursor_classify = db_classify.cursor()
db_classify.set_character_set('utf8')


# send message to users
# query database, grouping users according to disease
# wechat dev api, send message using open_id list
def send_msg():
    # group users by disease_id
    sql = 'SELECT disease_id FROM user_info GROUP BY disease_id'
    cursor_classify.execute(sql)
    results = cursor_classify.fetchall()

    for record in results:
        # for each group, generate open_id list
        sql = 'SELECT open_id, complications FROM user_info WHERE disease_id=%s'
        cursor_classify.execute(sql, record[0])
        res = cursor_classify.fetchall()
        open_id_list = []
        for r in res:
            open_id_list.append(r[0])
        # nickname: chmwang, append to each group
        open_id_list.append('o8AvqvsA4EPC6HkAfIz-lQOJUl-0')
        open_id_list.append('o8AvqvmmE20ISJslNhaB2oxYHxxg')
        print 'Open_id_list: ' + str(open_id_list)

        # candidate disease list
        disease_id_list = record[0]+res[0][1]
        # parse disease_id to type list & remove the last element
        disease_id_list = disease_id_list.split(',')
        disease_id_list.pop()

        # randomly decide which disease to recommend
        disease_id = disease_id_list[random.randint(0, len(disease_id_list)-1)]
        sql = 'SELECT name FROM disease_info WHERE id=%s'
        cursor_classify.execute(sql, disease_id)
        disease_name = cursor_classify.fetchall()
        print 'Disease_name: ' + disease_name[0][0]

        # iterate until disease_info_column not null
        while True:
            # randomly decide which column to choose in table `disease_info`
            recommend_item_index = random.randint(0, len(RECOMMEND_ITEM)-1)

            # fetch such disease_info column with specific disease_id
            # return list of related results, for example, book results(id=1, 2, ..)
            sql = 'SELECT '+RECOMMEND_ITEM[recommend_item_index]+' FROM disease_info WHERE id=%s'
            cursor_classify.execute(sql, disease_id)
            r = cursor_classify.fetchall()
            if len(r[0][0]) > 0:
                break

        # related result list
        item_id_list = r[0][0].split(',')
        item_id_list.pop()
        # choose only one in these results
        item_id = item_id_list[random.randint(0, len(item_id_list)-1)]
        print 'Item: ' + RECOMMEND_ITEM[recommend_item_index]
        print 'Item_id: ' + item_id

        # get article_id
        article_id = get_article_id(recommend_item_index, item_id)

        send_msg_api = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s' % access_token
        data = {
            'touser': open_id_list,
            'mpnews': {
                'media_id': article_id
            },
            'msgtype': 'mpnews'
        }
        # POST request, json format
        response = requests.post(send_msg_api, json.dumps(data))
        # response text, log for debug
        logging.info(response.text)
        print response.text + '\n\n'
    return


# cloudtest database & its cursor, encoding: utf8
db_cloudtest = MySQLdb.connect(host='localhost', user='web', passwd='web', db='cloudtest')
cursor_cloudtest = db_cloudtest.cursor()
db_cloudtest.set_character_set('utf8')


def send_apk():
    cursor_cloudtest.execute('SELECT open_id FROM user')
    results = cursor_cloudtest.fetchall()
    open_id_list = []
    for res in results:
        open_id_list.append(res[0])
    open_id_list.append('o8AvqvsA4EPC6HkAfIz-lQOJUl-0')
    open_id_list.append('o8AvqvmmE20ISJslNhaB2oxYHxxg')
    print 'Open_id_list: ' + str(open_id_list)

    cursor_classify.execute('SELECT COUNT(*) FROM apk')
    results = cursor_classify.fetchall()
    apk_numbers = results[0][0]
    apk_id = random.randint(0, apk_numbers % 100)

    sql = 'SELECT * FROM apk WHERE id=%s'
    cursor_classify.execute(sql, apk_id)
    results = cursor_classify.fetchall()
    title = results[0][1]
    print 'Title: ' + title

    source_url = results[0][5]
    content = results[0][6]
    digest = title

    media_id = str(get_media_id('../image/apk_img/%d.jpg' % apk_id))
    response = get_article_resp(media_id, title, source_url, content, digest)
    print response.text
    dct = json.loads(response.text)
    article_id = ''
    if 'media_id' in dct:
        # generate article_id
        article_id = dct['media_id']
    logging.info('Article_id: %s' % article_id)
    print 'Article_id: %s' % article_id

    send_msg_api = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s' % access_token
    data = {
        'touser': open_id_list,
        'mpnews': {
            'media_id': article_id
        },
        'msgtype': 'mpnews'
    }
    # POST request, json format
    response = requests.post(send_msg_api, json.dumps(data))
    # response text, log for debug
    logging.info(response.text)
    print response.text + '\n\n'

    return


def main():
    send_msg()
    send_apk()
    return


if __name__ == '__main__':
    main()
