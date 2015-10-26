import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class TutorialSpider(CrawlSpider):
	name = 'tutorial'
	allowed_domains = ['jbk.39.net']
	start_urls = ['http://jbk.39.net/gm/']
	rules = (Rule(LinkExtractor(allow=('http://jbk.39.net/gm/')), callback='parse_item', follow=True),)

	def parse_item(self, response):
		filename = response.url.split("/")[-2] + '.txt'
		filename = '/home/dick/tmp/htmls/gm/%s' % (filename)
		fp = open(filename, 'wb')
		fp.write(response.request.headers.get('Referer', None) \
			+ '\n' + response.url + '\n')
		fp.write(response.body)
		fp.close()
