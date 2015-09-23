# import os.path
import json
from bs4 import BeautifulSoup
import jieba
import jieba.analyse


def parse_content(d):
    for k in d.keys():
        if isinstance(d[k], dict):
            parse_content(d[k])
        else:
            dct_filter[k] = d[k]
    return

using_item = ['disease', 'lore', 'news', 'symptom']
EMPTY_FILE_NUM = 100

for item in using_item:
    log_file = '/home/dick/filter/%s/0_log.txt' % item
    f_log = open(log_file, 'w')
    req_id = 0
    missed = 0

    while True:
        if missed > EMPTY_FILE_NUM:
            break
        req_id += 1
        read_file = '/home/dick/yi18/%s/%d.txt' % (item, req_id)
        try:
            f = open(read_file, 'r')
        except IOError as e:
            missed += 1
            print e
            continue

        missed = 0
        data = f.read()
        f.close()
        dct = json.loads(data)
        dct_filter = {}
        parse_content(dct)
        content = ''
        for key in dct_filter.keys():
            if isinstance(dct_filter[key], unicode):
                content += dct_filter[key]

        soup = BeautifulSoup(content)
        content = soup.getText().encode('utf8')
        write_file = '/home/dick/filter/%s/%d.txt' % (item, req_id)
        # if os.path.isfile(write_file):
        #    print 'File %s exists, please continue.' % write_file
        #    continue
        f = open(write_file, 'w')
        f.write(content)
        f.close()

        tags = jieba.analyse.extract_tags(content, 5, True)
        f_log.write('%d ' % req_id)
        for word, weight in tags:
            f_log.write('%s %f ' % (word.encode('utf8'), weight))
        f_log.write('\n')
        print "We're done with %s." % write_file
    f_log.close()
