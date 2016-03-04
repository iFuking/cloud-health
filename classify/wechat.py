# encoding: utf-8
from wechat_sdk import WechatBasic
from pymongo import MongoClient
import urllib2
import socket
import json
import logging
import requests
import random
import subprocess


# ignore ssl InsecurePlatform warning
requests.packages.urllib3.disable_warnings()

# configure logging level
logging.basicConfig(level=logging.INFO)

# app_id & app_secret, generate access_token
app_id = 'wx1071ef65b25ab039'
app_secret = '235aaa4ed220afbf47af54939bebcff3'
wechat_basic_ins = WechatBasic(appid=app_id, appsecret=app_secret)

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
    # response = wechat_basic_ins.upload_media('image', open(img_path, 'r'))

    # official upload image api instead of WechatBasic python sdk
    upload_media_api = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image' % access_token
    # bash shell commend, write file
    bash_cmd = 'curl -F media=@%s "%s"' % (img_path, upload_media_api)

    upload_media_shell_path = '../image/upload_media.sh'
    f = open(upload_media_shell_path, 'w')
    f.write(bash_cmd)
    f.close()

    response = subprocess.Popen(upload_media_shell_path, shell=True, stdout=subprocess.PIPE).stdout.read()
    response = json.loads(response)

    # response text, log for debug
    logging.info(response)
    print response
    if 'media_id' in response:
        media_id = response['media_id']
    logging.info('Media_id: %s' % media_id)
    print 'Media_id: %s' % media_id
    return media_id


def get_article_resp(article_list):
    article_id_api = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s' % access_token
    # POST data format(json) & data example
    data = {
        'articles': [
            {
                'thumb_media_id': article_list[1]['media_id'],
                'author': 'cloud-health',
                'title': article_list[1]['title'],
                'content_source_url': article_list[1]['source_url'],
                'content': article_list[1]['content'],
                'digest': article_list[1]['digest'],
                'show_cover_pic': 1
            },
            {
                'thumb_media_id': article_list[0]['media_id'],
                'author': 'cloud-health',
                'title': article_list[0]['title'],
                'content_source_url': article_list[0]['source_url'],
                'content': article_list[0]['content'],
                'digest': article_list[0]['digest'],
                'show_cover_pic': 1
            }
        ]
    }
    # POST request, json format `str`
    response = requests.post(article_id_api, json.dumps(data, ensure_ascii=False), verify=False)

    # response text, log for debug
    logging.info(response.text)
    print response.text
    return response


def get_article_id(item_index, item_id, article_list):
    # get media_id
    media_id = str(get_media_id('../image/%s.jpg' % RECOMMEND_ITEM[item_index]))

    collection_name = 'f_'+RECOMMEND_ITEM[item_index]+'2s'
    res = db[collection_name].find({RECOMMEND_ITEM[item_index]+'_id': item_id})
    # fetch result as title
    title = res[0][TITLE[item_index]]
    print 'Title: ' + title.encode('utf8')
    logging.info('Title: ' + title)

    disease_json = dict()
    # fetch result as content
    disease_json['content'] = res[0]['content'].encode('utf8')

    disease_json['title'] = title.encode('utf8')
    # get digest, simplify content
    disease_json['digest'] = title.encode('utf8')

    disease_json['media_id'] = media_id
    disease_json['source_url'] = 'www.jtang.cn'

    article_list.append(disease_json)

    # POST request, json format `str`
    response = get_article_resp(article_list)

    dct = json.loads(response.text)
    article_id = ''
    if 'media_id' in dct:
        # generate article_id
        article_id = dct['media_id']
    logging.info('Article_id: %s' % article_id)
    print 'Article_id: %s' % article_id
    return article_id


def get_apk_article():
    # generate apk recommend article
    apk_numbers = db['w_apk2s'].count() / 10
    apk_id = random.randint(1, apk_numbers)
    print 'Apk_id: ' + str(apk_id)
    logging.info('Apk_id: ' + str(apk_id))

    results = db['w_apk2s'].find({'apk_id': apk_id})
    title = '应用推荐： ' + results[0]['name'].encode('utf8')
    print 'Title: ' + title
    logging.info('Title: ' + title)

    apk_json = dict()
    apk_json['title'] = title

    apk_json['source_url'] = results[0]['web_url'].encode('utf8')
    content = results[0]['description'].encode('utf8')
    apk_json['content'] = content.replace('\n', '<br>')

    apk_json['digest'] = title

    apk_json['media_id'] = str(get_media_id('../image/apk_img/%d.jpg' % apk_id))
    article_list = list()
    article_list.append(apk_json)

    # generate disease recommend article
    # group users by disease_id
    results = db['w_user_info2s'].aggregate([{'$group': {'_id': '$disease_id'}}])
    return article_list, results


def send_article():
    resp = get_apk_article()
    article_list = resp[0]
    results = resp[1]

    for record in results:
        # for each group, generate open_id list
        res = db['w_user_info2s'].find({'disease_id': record['_id']})
        open_id_list = list()
        disease_id_list = str()
        for r in res:
            open_id_list.append(r['open_id'])
            if not disease_id_list:
                disease_id_list = r['complications']

        # # move user to specific group
        # for open_id in open_id_list:
        #     wechat_basic_ins.update_group(open_id, int(group_id))
        # group_id += 1

        # nickname: chmwang, append to each group
        open_id_list.append('o8AvqvsA4EPC6HkAfIz-lQOJUl-0')
        print 'Open_id_list: ' + str(open_id_list)
        logging.info('Open_id_list: ' + str(open_id_list))

        # candidate disease list
        disease_id_list = record['_id']+disease_id_list
        # parse disease_id to type list & remove the last element
        disease_id_list = disease_id_list.split(',')
        disease_id_list.pop()

        # randomly decide which disease to recommend
        disease_id = int(disease_id_list[random.randint(0, len(disease_id_list)-1)])
        print disease_id

        disease_info = db['w_disease_info2s'].find({'disease_id': disease_id})
        print 'Disease_name: ' + disease_info[0]['name'].encode('utf8')
        logging.info('Disease_name: ' + disease_info[0]['name'])

        # iterate until disease_info_column not null
        while True:
            # randomly decide which column to choose in table `disease_info`
            recommend_item_index = random.randint(0, len(RECOMMEND_ITEM)-1)

            # fetch such disease_info column with specific disease_id
            # return list of related results, for example, book results(id=1, 2, ..)
            r = db['w_disease_info2s'].find({'disease_id': disease_id})
            if len(r[0][RECOMMEND_ITEM[recommend_item_index]]) > 0:
                break

        # related result list
        item_id_list = r[0][RECOMMEND_ITEM[recommend_item_index]].split(',')
        item_id_list.pop()
        # choose only one in these results
        item_id = item_id_list[random.randint(0, len(item_id_list)-1)]
        print 'Item: ' + RECOMMEND_ITEM[recommend_item_index]
        print 'Item_id: ' + item_id
        logging.info('Item: ' + RECOMMEND_ITEM[recommend_item_index])
        logging.info('Item_id: ' + item_id)

        # get article_id
        article_id = get_article_id(recommend_item_index, int(item_id), article_list)
        article_list.pop()

        send_msg_api = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s' % access_token
        data = {
            'touser': open_id_list,
            'mpnews': {
                'media_id': article_id
            },
            'msgtype': 'mpnews'
        }
        # POST request, json format
        response = requests.post(send_msg_api, json.dumps(data), verify=False)
        # response text, log for debug
        logging.info(response.text)
        print response.text + '\n\n'
    return


def main():
    send_article()
    return


if __name__ == '__main__':
    main()
