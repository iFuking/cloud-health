# encoding:utf-8

KEY_WORD = ['血压', '感冒', '脊椎', '消化', '泌尿']
DIRECTORY = ['bp', 'cold', 'back', 'digest', 'pee']

read_log_file = '/home/dick/filter/drug/0_log.txt'

for i in range(0, len(KEY_WORD)):
    read_log = open(read_log_file, 'r')
    write_log_path = '/home/dick/classify/%s/drug/0_log.txt' % DIRECTORY[i]
    write_log = open(write_log_path, 'w')
    for line in read_log.readlines():
        s = line.split(' ')
        if line.find(KEY_WORD[i]) is not -1:
            req_id = s[0]
            read_path = '/home/dick/yi18/drug/%s.txt' % req_id
            f = open(read_path, 'r')
            content = f.read()
            f.close()

            write_path = '/home/dick/classify/%s/drug/%s.txt' % (DIRECTORY[i], req_id)
            f = open(write_path, 'w')
            f.write(content)
            f.close()

            write_log.write(line)
            print "We're done with %s" % write_path
    write_log.close()
read_log.close()
