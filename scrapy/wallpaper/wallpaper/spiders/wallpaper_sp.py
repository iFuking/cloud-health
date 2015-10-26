import urllib2, os, re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from wallpaper.items import WallpaperItem
from scrapy.selector import Selector
from scrapy.http import Request

class wallpaper(CrawlSpider):
	name = "wallpaperSpider"
	allowed_domains = ['sj.zol.com.cn']
	start_urls = ['http://sj.zol.com.cn/bizhi/']
	number = 0
	rules = (
			Rule(LinkExtractor(allow = ('detail_\d{4}_\d{5}\.html')), callback = 'parse_image', follow=False),
			)
	
	def parse_image(self, response):
		sel = Selector(response)
		sites = sel.xpath("//div[@class='wrapper mt15']//dd//a[contains(@href,'.html')]/@href").extract()
		# self.log('sites length is %d' % len(sites))
		for site in sites:
			url = 'http://sj.zol.com.cn%s' % site
			# self.log(url + '\n')
			item = WallpaperItem()
			item['size'] = re.search('\d*x\d*', site).group()
			item['altInfo'] = sel.xpath("//h1//a/text()").extract()[0]
			return Request(url, meta={'item': item}, callback=self.parse_href)

	def parse_href(self, response):
		item = response.meta['item']
		items = []
		sel = Selector(response)
		src = sel.xpath("//body//img/@src").extract()[0]
		item['imgSrc'] = src
		items.append(item)
		# self.download(src)
		return items

	def download(self, url):
		self.number += 1
		savePath = '/home/dick/tmp/image/%d.jpg' % (self.number)
		self.log('downloading...' + url)
		try:
			img_url = urllib2.urlopen(url)
			img = img_url.read()
			downloadImg = open(savePath, 'wb')
			downloadImg.write(img)
			img_url.close()
			downloadImg.close()
		except:
			self.log(savePath % 'can not download.')

