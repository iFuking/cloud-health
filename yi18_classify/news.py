# encoding:utf-8
KEY_WORD = '血压'

read_log_path = '/home/dick/filter/news/0_log.txt'
read_log = open(read_log_path, 'r')
write_log_path = '/home/dick/classify/bp/news/0_log.txt'
write_log = open(write_log_path, 'w')

for line in read_log.readlines():
    item = line.split(' ')
    for i in range(0, len(item)):
        # print type(item[i]), item[i].decode('utf8')
        if i % 2 and item[i].find(KEY_WORD) is not -1:
            req_id = item[0]
            # print type(req_id)
            read_path = '/home/dick/yi18/news/%s.txt' % req_id
            f = open(read_path, 'r')
            content = f.read()
            # print type(content)
            f.close()

            write_path = '/home/dick/classify/bp/news/%s.txt' % req_id
            f = open(write_path, 'w')
            f.write(content)
            f.close()
            # print type(line)
            write_log.write(line)
            print "We're done with %s" % write_path
            break
read_log.close()
write_log.close()
