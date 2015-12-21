# encoding: utf-8

from bs4 import BeautifulSoup
import urllib2
import logging
import MySQLdb

db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='classify')
cursor = db.cursor()
db.set_character_set('utf8')

logging.basicConfig(level=logging.INFO)

user_agent = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) ' \
             'AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'

# search key word
word = '医疗'


def get_soup_by_url(url):
    success = True
    try:
        req = urllib2.Request(url, headers={'User-Agent': user_agent})
        web_page = urllib2.urlopen(req)
        return BeautifulSoup(web_page.read(), 'lxml')
    except Exception, e:
        success = False
        raise e
    finally:
        logging.info("request url %s: %s", "success" if success else "fail", url)


def sync_db(app_id, name, star, down_num, img_url, apk_url, description):
    try:
        sql = 'INSERT INTO apk(id, name, star, down_num, img_url, apk_url, description) ' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (app_id, name, star, down_num, img_url, apk_url, description))
        db.commit()
    except Exception, e:
        logging.info(e)
    return


def chr_replace(content):
    content_tmp = ''
    for i in range(0, len(content)):
        # if ord(content[i]) == 12288:
        #     continue
        if i > 2 and ord(content[i]) == ord('\n') and ord(content[i-1]) == ord('\n') and ord(content[i-2]) == ord('\n'):
            continue
        content_tmp += content[i]
    content = content_tmp.replace('\t', '').replace(' ', '')
    return content


def get_360_info(url):
    total_pages = 75
    app_id = 0

    for i in range(1, total_pages):
        url_now = ''.join([url, str(i)])
        soup = get_soup_by_url(url_now)

        app_list = soup.find('div', class_='SeaCon').find_all('li')
        for app in app_list:
            app_id += 1
            app_name = app.find_all('a')[1].get('title')
            app_star = unicode(app.find('div', class_='sdlft').contents[2])
            download_numbers = app.find('p', class_='downNum').getText()
            apk_url = app.find('div', class_='download comdown').find_all('a')[0].get('href')

            detailed_url = app.find_all('a')[0].get('href').encode('utf8')
            req = urllib2.Request(''.join(['http://zhushou.360.cn', detailed_url]))
            web_page = urllib2.urlopen(req)
            s = BeautifulSoup(web_page.read(), 'lxml')
            # s = get_soup_by_url(''.join(['http://zhushou.360.cn', detailed_url]))
            img_url = s.find('dl', class_='clearfix').find_all('img')[0].get('src')
            content = s.find('div', class_='breif').getText()
            # content = content.replace('\r', ' ').replace('\t', '').replace(' ', '')
            content = chr_replace(content)

            sync_db(app_id, app_name, app_star, download_numbers, img_url, apk_url, content)
            logging.info('App name: %s' % app_name)
    return


def main():
    try:
        url = ''.join(['http://zhushou.360.cn/search/index/?kw=', word, '&page='])
        get_360_info(url)
    except Exception, e:
        logging.info(e)


if __name__ == '__main__':
    main()
