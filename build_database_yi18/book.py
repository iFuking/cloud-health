import MySQLdb
import logging
import json

# yi18 database & its cursor, encoding: utf8
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='yi18')
cursor = db.cursor()
db.set_character_set('utf8')

# database data reading from file system, read path
home_path = '/home/dick/yi18'
logging.basicConfig(level=logging.INFO)

EMPTY_RESP_NUM = 100


def main():
    req_id = empty_resp = 0
    while True:
        # break if response is empty for continuous certain times
        if empty_resp > EMPTY_RESP_NUM:
            break
        req_id += 1

        try:
            file_name = '%s/book/%d.txt' % (home_path, req_id)
            read_file = open(file_name)
            content = read_file.read()

            empty_resp = 0
            # parse content, json format
            dct = json.loads(content)
            req_id = dct['yi18']['id']
            book_class = dct['yi18']['bookclass']
            name = dct['yi18']['name']

            # mysql operation
            sql = 'INSERT INTO book(id, name, bookclass, content) VALUES(%s, %s, %s, %s)'
            cursor.execute(sql, (req_id, name, book_class, content))
            db.commit()
            logging.info('Building DATABASE `yi18`, TABLE `book`, ' + file_name)

        except (IOError, ValueError, TypeError, MySQLdb.IntegrityError) as e:
            empty_resp += 1
            # error log
            logging.error(e)
            continue

        finally:
            read_file.close()


if __name__ == '__main__':
    main()
