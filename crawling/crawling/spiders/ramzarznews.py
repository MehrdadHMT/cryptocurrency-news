import scrapy

from ..items import CryptocurrencyNewsItem


class RamzarzNewsSpider(scrapy.Spider):
	name = 'ramzarznews'
	allowed_domains = ['ramzarz.news']
	start_urls = [
		"https://ramzarz.news/category/news/bitcoin-news/page/1/",
		"https://ramzarz.news/category/news/altcoins-news/page/1/",
		"https://ramzarz.news/category/news/ethereum-news/page/1/"
	]

	def __init__(self):
		self.my_pipeline = None

	def parse(self, response, **kwargs):
		next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()

		news_links = response.xpath('//div[@class="content-column"]/div/article/div/div[1]/a/@href').getall()

		for link in news_links:
			if self.my_pipeline.duplicate_record_flag:
				break
			yield scrapy.Request(url=link, callback=self.parse_item)

		if next_page and not self.my_pipeline.duplicate_record_flag:
			yield scrapy.Request(url=next_page, callback=self.parse)

	def parse_item(self, response):
		item = CryptocurrencyNewsItem()
		item['title'] = response.xpath('//h1/span[@class="post-title"]/text()').get()
		item['category'] = response.xpath('//div[@class="term-badges "]/span[1]/a/text()').get()
		item['author'] = response.xpath('//span[@class="post-author-name"]/b/text()').get()
		item['description'] = response.xpath(
			'//div[@class="entry-content clearfix single-post-content"]/p[position()<=3]/text()'
		).get()
		item['source'] = response.request.url
		item['publish_date'] = response.xpath(
			'//span[@class="time"]/time[@class="post-published updated"]/b/text()'
		).get()
		return item
