import scrapy

from scrapy.loader import ItemLoader

from ..items import BanktennesseeItem
from itemloaders.processors import TakeFirst


class BanktennesseeSpider(scrapy.Spider):
	name = 'banktennessee'
	start_urls = ['https://www.banktennessee.com/connect/news-and-media']

	def parse(self, response):
		post_links = response.xpath('//div[@data-content-block="bodyCopy"]//a/@href[not (ancestor::ul | ancestor::em)]').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//em//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="body-content content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BanktennesseeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
