# encoding: utf-8
import MySQLdb


db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='classify')
cursor = db.cursor()
db.set_character_set('utf8')


def mongo_dump_csv():
    sql = 'SHOW TABLES'
    cursor.execute(sql)
    table_name = cursor.fetchall()

    for table in table_name:
        sql = 'SELECT * FROM %s' % table + \
              ' INTO OUTFILE \'/tmp/db_csv/%s.csv\'' % table + \
              ' FIELDS TERMINATED BY \',\'' \
              ' ENCLOSED BY \'"\'' \
              ' LINES TERMINATED BY \'\\n\';'
        print sql
        cursor.execute(sql)
        db.commit()
    return


def main():
    mongo_dump_csv()
    return


if __name__ == '__main__':
    main()
