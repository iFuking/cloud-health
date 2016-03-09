# encoding: utf-8

import urllib2
import logging
import MySQLdb

db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='classify')
cursor = db.cursor()
db.set_character_set('utf8')

logging.basicConfig(level=logging.INFO)


def download(img_id, url):
    save_path = '../image/apk_img/%d.png' % img_id
    logging.info('downloading...' + url)
    try:
        img_url = urllib2.urlopen(url)
        img = img_url.read()
        download_img = open(save_path, 'wb')
        download_img.write(img)
        img_url.close()
        download_img.close()
    except Exception, e:
        logging.info(e)
    return


def main():
    cursor.execute('SELECT id, img_url FROM apk')
    results = cursor.fetchall()
    for res in results:
        img_id = res[0]
        img_url = res[1]
        download(img_id, img_url)
    return


if __name__ == '__main__':
    main()
