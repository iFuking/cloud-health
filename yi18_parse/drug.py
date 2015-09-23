import json

EMPTY_FILE_NUM = 100
req_id = 0
missed = 0

log_path = '/home/dick/filter/drug/0_log.txt'
f_log = open(log_path, 'w')

while True:
    if missed > EMPTY_FILE_NUM:
        break
    req_id += 1
    read_path = '/home/dick/yi18/drug/%d.txt' % req_id
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
    # { "yi18": { "categoryName": } }
    if 'categoryName' in dct['yi18']:
        content = dct['yi18']['categoryName'].encode('utf8')
    elif 'PType' in dct['yi18']:
        content = dct['yi18']['PType'].encode('utf8')
    else:
        continue
    f_log.write('%d %s\n' % (req_id, content))
    print "We're done with %s" % read_path
f_log.close()