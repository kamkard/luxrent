"""
To find rent prices from Amli Southshore only.  Need to build out to find all Amli sites.
"""
import scrapy

class RentSpider(scrapy.Spider):
	name = 'rent'

	start_urls = ['https://www.amli.com/apartments/austin/central-east-austin/austin/south-shore/floorplans']

	def parse(self, response):
"""
java link to all rooms
	 response.xpath('//div[@id="fpHolder"]/a/@href').extract()
"""