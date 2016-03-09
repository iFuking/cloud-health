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
app_id = 'wxe7db3628dfaa5eb9'
app_secret = 'd4624c36b6795d1d99dcf0547af5443d'
wechat_basic_ins = WechatBasic(appid=app_id, appsecret=app_secret)


def get_access_token():
    # app_id & app_secret, generate access_token

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
    print response
    if 'media_id' in response:
        media_id = response['media_id']
    print 'Media_id: %s' % media_id
    return media_id


def get_article_resp(media_id, title, source_url, content, digest):
    article_id_api = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s' % access_token
    # POST data format(json) & data example
    data = {
        'articles': [
            {
                'thumb_media_id': media_id,
                'author': "cloud-health",
                'title': title,
                'content_source_url': source_url,
                'content': content,
                'digest': digest,
                'show_cover_pic': 1
            }
        ]
    }
    print data
    print json.dumps(data, ensure_ascii=False)
    # POST request, json format `str`
    response = requests.post(article_id_api, json.dumps(data, ensure_ascii=False))

    # response text, log for debug
    print response.text
    return response


db_filter = MySQLdb.connect(host='localhost', user='web', passwd='web', db='filter')
cur_filter = db_filter.cursor()
db_filter.set_character_set('utf8')


def get_article_id():
    # media_id = str(get_media_id('./img.jpg'))
    media_id = 'ZlYOpNhD0MEhlm9d_JU7i3Ny_w5IrxIvV0VdHdfAYChZOafBFyyJKWuiPtEGxtGf'

    sql = 'SELECT content FROM ask_cache WHERE id=1'
    cur_filter.execute(sql)
    result = cur_filter.fetchall()

    title = 'tag test'
    content = result[0][0]
    # content = '<p>啊"双引号"哦</p>\n0嘿嘿嘿\n0哈哈哈<p>换行哈</p>'
    # content = content.replace('\n', '<br></br>')
    print content
    response = get_article_resp(media_id, title, 'www.jtang.cn', content, title)

    dct = json.loads(response.text)
    if 'media_id' in dct:
        # generate article_id
        article_id = dct['media_id']
    print 'Article_id: %s' % article_id
    return article_id


def send_msg():
    open_id_list = [
        'oJjGiuBr4RprdzR-CSHhHS6LWWZ4',
        'oJjGiuL_cgIzxAW8o45_6eHT_8IA',
        'o8AvqvsA4EPC6HkAfIz-lQOJUl-0'
    ]
    article_id = get_article_id()

    send_msg_api = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s' % access_token

    data = {
        'touser': open_id_list,
        'mpnews': {
            'media_id': article_id
        },
        'msgtype': 'mpnews'
    }
    print type(data)
    print type(json.dumps(data))
    print json.dumps(data)
    response = requests.post(send_msg_api, json.dumps(data))
    print response.text + '\n\n'
    return


# cloudtest database & its cursor, encoding: utf8
db_cloudtest = MySQLdb.connect(host='localhost', user='web', passwd='web', db='cloudtest')
cursor_cloudtest = db_cloudtest.cursor()
db_cloudtest.set_character_set('utf8')

# cloudtest database & its cursor, encoding: utf8
db_classify = MySQLdb.connect(host='localhost', user='web', passwd='web', db='classify')
cursor_classify = db_classify.cursor()
db_classify.set_character_set('utf8')


def send_apk():
    cursor_cloudtest.execute('SELECT open_id FROM user')
    results = cursor_cloudtest.fetchall()
    open_id_list = []
    for res in results:
        open_id_list.append(res[0])
    open_id_list.append('o8AvqvsA4EPC6HkAfIz-lQOJUl-0')
    open_id_list.append('o8AvqvmmE20ISJslNhaB2oxYHxxg')
    print 'Open_id_list: ' + str(open_id_list)
    logging.info('Open_id_list: ' + str(open_id_list))

    cursor_classify.execute('SELECT COUNT(*) FROM apk')
    results = cursor_classify.fetchall()
    apk_numbers = results[0][0] / 10
    apk_id = random.randint(0, apk_numbers)
    print 'Apk_id: ' + str(apk_id)
    logging.info('Apk_id: ' + str(apk_id))

    sql = 'SELECT * FROM apk WHERE id=%s'
    cursor_classify.execute(sql, apk_id)
    results = cursor_classify.fetchall()
    title = results[0][1]
    print 'Title: ' + title
    logging.info('Title: ' + title)

    source_url = 'http://www.jtang.cn'
    print source_url
    content = results[0][7]
    content = content.replace('\n', '<br>')
    print content
    digest = title

    media_id = str(get_media_id('../image/apk_img/%d.jpg' % apk_id))
    response = get_article_resp(media_id, title, source_url, content, digest)

    dct = json.loads(response.text)
    article_id = ''
    if 'media_id' in dct:
        # generate article_id
        article_id = dct['media_id']
    logging.info('Article_id: %s' % article_id)
    print 'Article_id: %s' % article_id

    send_msg_api = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s' % access_token
    data = {
        'touser': [
            'oJjGiuBr4RprdzR-CSHhHS6LWWZ4',
            'oJjGiuL_cgIzxAW8o45_6eHT_8IA',
            'o8AvqvsA4EPC6HkAfIz-lQOJUl-0'
        ],
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
    # send_msg()
    send_apk()
    return


if __name__ == '__main__':
    main()
