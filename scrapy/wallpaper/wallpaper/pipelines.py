# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys, MySQLdb, hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class WallpaperPipeline(object):
	def process_item(self, item, spider):
		conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="demo")
		curs = conn.cursor()
		conn.set_character_set('utf8')  # declare necessary. 
		curs.execute('SET NAMES utf8;')
		curs.execute('SET CHARACTER SET utf8;')
		curs.execute('SET character_set_connection=utf8;')

		SQL = "INSERT INTO img(size, info, src) VALUES('%s', '%s', '%s')" % (item['size'], item['altInfo'], item['imgSrc'])
		try:
			curs.execute(SQL)
			conn.commit()
		except MySQLdb.Error, e:
			self.log("MySQL Error %d: %s" % (e.args[0], e.args[1]))
		conn.close()
		return item
		
