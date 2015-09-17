__author__ = 'dick'
import urllib2
import socket

MIN_RESP_CONTENT_LENGTH = 81
EMPTY_RESP_NUM = 100
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
api_item = [
    'disease', 'symptom', 'check', 'surgery',
    'lore', 'ask', 'book',
    'drug', 'food', 'cook',
    'news'
]

for item in api_item:
    req_id = 0
    empty_resp = 0
    missed = 0
    fetch_resp = 0
    log_file = '/home/dick/tmp/%s/0_log.txt' % item
    f_log = open(log_file, 'w')

    while True:
        if empty_resp > EMPTY_RESP_NUM:
            break
        req_id += 1
        url = 'http://api.yi18.net/%s/show?id=%d' % (item, req_id)
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request, timeout=1)
            content = response.read()
            if len(content) < MIN_RESP_CONTENT_LENGTH:
                empty_resp += 1
                continue

        except urllib2.URLError as e:
            missed += 1
            f_log.write('%s %r\n' % (url, e))
            print type(e)
            continue
        except socket.timeout as e:
            missed += 1
            f_log.write('%s %r\n' % (url, e))
            print type(e)
            continue

        empty_resp = 0
        filename = '/home/dick/tmp/%s/%d.txt' % (item, req_id)
        fp = open(filename, 'w')
        fp.write(content)
        fp.close()
        print url
        last_resp_id = req_id
        fetch_resp += 1
    f_log.write('%d responses missed in total.\n' % missed)
    f_log.write('Fetch %d responses in total.\n' % fetch_resp)
    f_log.write('Last response id is %d.\n' % last_resp_id)
    f_log.close()


