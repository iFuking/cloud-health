# encoding: utf-8
import MySQLdb
import json
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import logging
import time

db = MySQLdb.connect(host='localhost', user='web', passwd='web', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

ignore_key = [
    'img', 'from', 'author', 'count',
    'image', 'ANumber', 'PType', 'factory',
    'time'
]
dct_value = {}


def ignore_tag(tag):
    for k in ignore_key:
        if k == tag:
            return False
    return True


def json_value(dct):
    for key in dct.keys():
        # type(d[k]) is also dict, call function recursively
        if isinstance(dct[key], dict):
            json_value(dct[key])
        # type(d[k]) is list, parse each node
        elif isinstance(dct[key], list):
            for it in dct[key]:
                json_value(it)
        # until key-value structure, save it
        else:
            dct_value[key] = dct[key]
    return


def main():
    sql = 'select * from ask where id=1700'
    cursor.execute(sql)
    results = cursor.fetchall()
    for record in results:
        json_value(json.loads(record[3]))
        content = ''
        for key in dct_value.keys():
            # only unicode(string) included, int/long/bool.. ignored
            # filter the second time
            if ignore_tag(key) and isinstance(dct_value[key], unicode):
                content += dct_value[key]

        soup = BeautifulSoup(content)
        content = soup.getText()
        res = ''
        for i in range(0, len(content)):
            if ord(content[i]) == 12288:
                continue
            elif i > 0 and ord(content[i]) == ord('\n') and ord(content[i]) == ord(content[i-1]):
                continue
            res += content[i]
        content = res.replace('\r', '').replace('\t', '').replace(' ', '')
        print content

        f = open('/home/dick/tmp/heh.txt', 'w')
        f.write(content.encode('utf8'))
        f.close()
        # res = ''
        # for i in range(0, len(content)):
        #     if ord(content[i]) == 12288:
        #         continue
        #     res += content[i]
        # print res
        # for i in range(16, 22):
        #     print ord(content[i])
        # print content[16:22]


if __name__ == '__main__':
    main()