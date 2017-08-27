"""
To find rent prices from Amli Southshore only.  Need to build out to find all Amli sites.
"""
import scrapy
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider

HEADERS = {
	 'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}

URL = 'https://www.amli.com/apartments/austin/central-east-austin/austin/south-shore/floorplans' 

class RentSpider(scrapy.Spider):
	name = 'rent'
	page = 0
	
	start_urls = [URL]

	def parse(self, response):		
		#submit a form (first page)

		page = 0
		ViewState = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract().pop()
		ViewStateGenerator = response.xpath('//input[@id = "__VIEWSTATEGENERATOR"]/@value').extract().pop()
		EventValidation = response.xpath('//input[@id = "__EVENTVALIDATION"]/@value').extract().pop()

		self.link = {}

		self.link['__EVENTTARGET'] = response.xpath('//div[@id="fpHolder"]/a/@href').extract()[page][25:112]
		self.link['__EVENTARGUMENT'] = ''
		self.link['__VIEWSTATE'] = ViewState
		self.link['__VIEWSTATEGENERATOR'] = ViewStateGenerator
		self.link['__SCROLLPOSITIONX'] = '0'
		self.link['__SCROLLPOSITIONY'] = '0'
		self.link['__EVENTVALIDATION'] = EventValidation

		return FormRequest(url=URL,
						   method = 'POST',
						   callback = self.parse_page,
						   formdata=self.link,
						   meta = {'page':1},
						   dont_filter = True,
						   headers = HEADERS)

	def parse_page(self, response):
		#Find the apt room infos
		for data in response.xpath('//tr[@class="highlightRowClicked" or @class = "highlightRow"]'):
			yield {

			'Floor' : data.xpath('.//span[contains(@id, "Floor")]/text()').extract(),
			'RoomNumber' : data.xpath('.//span[contains(@id, "Number")]/text()').extract(),
			'Pets' : data.xpath('.//span[contains(@id, "Pets")]/text()').extract(),
			'Dates' : data.xpath('.//span[contains(@id, "UnitDates")]/text()').extract(),
			'Price' : data.xpath('.//span[contains(@id, "Price")]/text()').extract(),

			}


		#Get Next Page
		page += 1
		ViewState = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract().pop()
		ViewStateGenerator = response.xpath('//input[@id = "__VIEWSTATEGENERATOR"]/@value').extract().pop()
		EventValidation = response.xpath('//input[@id = "__EVENTVALIDATION"]/@value').extract().pop()


		link = {
			'__EVENTTARGET' : response.xpath('//div[@id="fpHolder"]/a/@href').extract()[page][25:112], 
			'__VIEWSTATE' : ViewState,
			'__VIEWSTATEGENERATOR' : ViewStateGenerator,
			'__EVENTVALIDATION' : EventValidation,
		}

		return FormRequest(url=URL,
						   method = 'POST',
						   callback = self.parse_page,
						   formdata=self.link,
						   meta = {'page':1},
						   dont_filter = True,
						   headers = HEADERS)

			#print(dict(floor=floor, RoomNumber=RoomNumber, Pets=Pets, Dates=Dates, Price=Price))

		#java link to all rooms
		
		#response.xpath('//div[@id="fpHolder"]/a/@href').extract()
		#response.xpath('//div[@id="fpHolder"]/a/@href').extract()[page][25:112]


		
		

