import json

EMPTY_FILE_NUM = 100
req_id = 0
missed = 0

log_path = '/home/dick/filter/check/0_log.txt'
f_log = open(log_path, 'w')

while True:
    if missed > EMPTY_FILE_NUM:
        break
    req_id += 1
    read_path = '/home/dick/yi18/check/%d.txt' % req_id
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
    # { "yi18": { "menu": }
    #           { "symptom": }
    #           { "disease": }
    #           { "name": }
    # }
    content = ''
    if 'menu' in dct['yi18']:
        content += dct['yi18']['menu']
    if 'symptom' in dct['yi18']:
        content += dct['yi18']['symptom']
    if 'disease' in dct['yi18']:
        content += dct['yi18']['disease']
    content += dct['yi18']['name']
    # print type(content)
    f_log.write('%d %s\n' % (req_id, content.encode('utf8')))
    print "We're done with %s" % read_path
f_log.close()
