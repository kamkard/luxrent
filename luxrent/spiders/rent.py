"""
To find rent prices from Amli Southshore only.  Need to build out to find all Amli sites.
"""
import scrapy

class RentSpider(scrapy.Spider):
	name = 'rent'

	
	start_urls = ['https://www.amli.com/apartments/austin/central-east-austin/austin/south-shore/floorplans']

	def parse(self, response):

		
		#Find the apt room infos

		for data in response.xpath('//tr[@class="highlightRowClicked" or @class = "highlightRow"]'):
			yield {

			'Floor' : data.xpath('.//span[contains(@id, "Floor")]/text()').extract(),
			'RoomNumber' : data.xpath('.//span[contains(@id, "Number")]/text()').extract(),
			'Pets' : data.xpath('.//span[contains(@id, "Pets")]/text()').extract(),
			'Dates' : data.xpath('.//span[contains(@id, "UnitDates")]/text()').extract(),
			'Price' : data.xpath('.//span[contains(@id, "Price")]/text()').extract(),

			}

			#print(dict(floor=floor, RoomNumber=RoomNumber, Pets=Pets, Dates=Dates, Price=Price))

		#java link to all rooms
		
		response.xpath('//div[@id="fpHolder"]/a/@href').extract()



		
		

