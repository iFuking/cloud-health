import urllib2
import os
import re

from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request

class ExaSpider(CrawlSpider):
	name = "exa"
	allowed_domains = ['patest.cn']
	start_urls = ['http://www.patest.cn/']
	rules = (
			Rule(LinkExtractor(), callback = 'parse_url', follow = True), 
			)

	def parse_url(self, response):
		fp = open('/home/dick/pat_urls.txt', 'a+')
		fp.write(response.url + '\n')
		fp.close()

