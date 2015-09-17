import json
from bs4 import BeautifulSoup


def parse_content(d):
    for k in d.keys():
        if isinstance(d[k], dict):
            parse_content(d[k])
        else:
            dct_filter[k] = d[k]
    return


f = open('/home/dick/yi18/disease/7.txt', 'r')
data = f.read()
dct = json.loads(data)
dct_filter = {}
parse_content(dct)
content = ""
for key in dct_filter.keys():
    if isinstance(dct_filter[key], int) or isinstance(dct_filter[key], bool):
        dct_filter[key] = str(dct_filter[key])
    content += str(dct_filter[key].encode('utf8'))
    print key
    print dct_filter[key].encode('utf8')

f = open('/home/dick/yi18/foo.txt', 'w')
f.write(content)
f.close()

soup = BeautifulSoup(open('/home/dick/yi18/foo.txt'))
print soup.getText()