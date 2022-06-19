import scrapy

from ..items import CryptocurrencyNewsItem


class ArzdigitalSpider(scrapy.Spider):
	name = 'arzdigital'
	allowed_domains = ['arzdigital.com']
	start_urls = [
		"https://arzdigital.com/category/news/bitcoin-news/page/1/",
		"https://arzdigital.com/category/news/altcoins-news/page/1/",
		"https://arzdigital.com/category/news/ethereum-news/page/1/"
	]

	def __init__(self):
		self.my_pipeline = None

	def parse(self, response, **kwargs):
		next_page = response.xpath(
			'//li[@class="arz-pagination__item arz-pagination__next"]/a[@class="arz-pagination__link"]/@href'
		).get()

		news_links = response.xpath('//a[@class="arz-last-post arz-row"]/@href').getall()

		for link in news_links:
			if self.my_pipeline.duplicate_record_flag:
				break
			yield scrapy.Request(url=link, callback=self.parse_item)

		if next_page and not self.my_pipeline.duplicate_record_flag:
			yield scrapy.Request(url=next_page, callback=self.parse)

	def parse_item(self, response):
		item = CryptocurrencyNewsItem()
		item['title'] = response.xpath('//h1[@class="arz-post__title"]/a/text()').get()
		item['category'] = response.xpath('//div[@class="arz-main-categories"]/div[1]/a/span/text()').get()
		item['author'] = response.xpath('//span[@class="arz-post__info-author-name"]/a/text()').get()
		item['description'] = response.xpath(
			'//section[@class="arz-post__content"]/article/p[position()<=3]/text()'
		).get()
		item['source'] = response.request.url
		item['publish_date'] = response.xpath(
			'//div[@class="arz-post__info-publish-date arz-col-sb-6 arz-col-sm-sb-6"]/time/@datetime'
		).get()
		return item
