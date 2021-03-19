import scrapy

from scrapy.loader import ItemLoader

from ..items import BabbremendeItem
from itemloaders.processors import TakeFirst


class BabbremendeSpider(scrapy.Spider):
	name = 'babbremende'
	start_urls = ['https://www.bab-bremen.de/bab/erfolgsgeschichten.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-md-6 col-sm-6 col-xs-12"]')
		for post in post_links:
			url = post.xpath('./h3/a/@href').get()
			date = post.xpath('./h5/text()').get()
			title = post.xpath('./h3/a/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, title, date):
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "col-xs-12", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "col-xs-12", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "col-sm-12", " " ))]//text()[normalize-space()] | //*[contains(concat( " ", @class, " " ), concat( " ", "col-md-12", " " )) and contains(concat( " ", @class, " " ), concat( " ", "col-xs-12", " " ))]//div//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BabbremendeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
