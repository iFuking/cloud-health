# encoding:utf-8

using_item = ['disease', 'lore', 'news', 'symptom']

KEY_WORD = ['血压', '肥胖', '脊椎', '消化']
DIRECTORY = ['bp', 'fat', 'back', 'digestion']


for item in using_item:
    for i in range(0, len(KEY_WORD)):
        read_log_file = '/home/dick/filter/%s/0_log.txt' % item
        read_log = open(read_log_file, 'r')

        write_log_file = '/home/dick/classify/%s/%s/0_log.txt' % (DIRECTORY[i], item)
        write_log = open(write_log_file, 'w')
        for line in read_log.readlines():
            s = line.split(' ')
            if line.find(KEY_WORD[i]) is not -1:
                req_id = s[0]
                read_file = '/home/dick/yi18/%s/%s.txt' % (item, req_id)
                f = open(read_file, 'r')
                content = f.read()
                f.close()

                write_file = '/home/dick/classify/%s/%s/%s.txt' % (DIRECTORY[i], item, req_id)
                f = open(write_file, 'w')
                f.write(content)
                f.close()
                write_log.write(line)
                print "We're done with %s" % write_file
        write_log.close()

    read_log.close()
