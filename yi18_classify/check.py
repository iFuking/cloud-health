# encoding:utf-8
KEY_WORD = '血压'

read_log_path = '/home/dick/filter/check/0_log.txt'
read_log = open(read_log_path, 'r')
write_log_path = '/home/dick/classify/bp/check/0_log.txt'
write_log = open(write_log_path, 'w')

for line in read_log.readlines():
    item = line.split(' ')
    if item[1].find(KEY_WORD) is not -1:
        req_id = item[0]
        read_path = '/home/dick/yi18/check/%s.txt' % req_id
        f = open(read_path, 'r')
        content = f.read()
        f.close()

        write_path = '/home/dick/classify/bp/check/%s.txt' % req_id
        f = open(write_path, 'w')
        f.write(content)
        f.close()

        write_log.write(line)
        print "We're done with %s" % write_path
read_log.close()
write_log.close()
