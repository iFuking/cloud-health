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


EMPTY_FILE_NUM = 100
req_id = 0
missed = 0

log_path = '/home/dick/filter/symptom/0_log.txt'
f_log = open(log_path, 'w')

while True:
    if missed > EMPTY_FILE_NUM:
        break
    req_id += 1
    read_path = '/home/dick/yi18/symptom/%d.txt' % req_id
    try:
        f = open(read_path, 'r')
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
        if isinstance(dct_filter[key], int) is False and isinstance(dct_filter[key], bool) is False:
            content += str(dct_filter[key].encode('utf8'))

    soup = BeautifulSoup(content)
    content = soup.getText().encode('utf8')
    write_path = '/home/dick/filter/symptom/%d.txt' % req_id
    f = open(write_path, 'w')
    f.write(content)
    f.close()
    f_log.write('%d ' % req_id)
    tags = jieba.analyse.extract_tags(content, 5, True)
    for word, weight in tags:
        f_log.write('%s %f ' % (word.encode('utf8'), weight))
    f_log.write('\n')
    print "We're done with %s" % write_path
f_log.close()
