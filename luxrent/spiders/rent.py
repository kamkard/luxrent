"""
To find rent prices from Amli Southshore only.  Need to build out to find all Amli sites.
"""
import scrapy
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider

from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response

HEADERS = {
	 'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}

URL = 'https://www.amli.com/apartments/austin/central-east-austin/austin/south-shore/floorplans' 

class RentSpider(scrapy.Spider):
	name = 'rent'
	
	
	start_urls = [URL]

	def start_requests(self, response):		
		#submit a form (first page)
		current_page = 0
		ViewState = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract().pop()
		ViewStateGenerator = response.xpath('//input[@id = "__VIEWSTATEGENERATOR"]/@value').extract().pop()
		EventValidation = response.xpath('//input[@id = "__EVENTVALIDATION"]/@value').extract().pop()
		EventTargetVariable = response.xpath('//div[@id="fpHolder"]/a/@href').extract()[current_page][25:112]

		
		#open_in_browser(response)
		return [FormRequest(
			url = URL,
			callback = self.parse,
			formdata= {
			'__EVENTTARGET' : EventTargetVariable, 
			'__EVENTARGUMENT' : '', '__VIEWSTATE' : ViewState,
			'__VIEWSTATEGENERATOR': ViewStateGenerator, 
			'__EVENTVALIDATION' : EventValidation,
			},
			meta = {'page':0},
			)]

	def parse(self, response):
		#inspect_response(response,self)

		current_page = response.meta['page'] + 1
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
		
		ViewState = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract().pop()
		ViewStateGenerator = response.xpath('//input[@id = "__VIEWSTATEGENERATOR"]/@value').extract().pop()
		EventValidation = response.xpath('//input[@id = "__EVENTVALIDATION"]/@value').extract().pop()
		EventTargetVariable = response.xpath('//div[@id="fpHolder"]/a/@href').extract()[current_page][25:112]
		yield {
		'View': ViewStateGenerator,
		'Target' : EventTargetVariable
		}
		#open_in_browser(response)
		return [FormRequest(
			url = URL,
			callback = self.parse,
			formdata= {
			'__EVENTTARGET' : EventTargetVariable, 
			'__EVENTARGUMENT' : '', '__VIEWSTATE' : ViewState,
			'__VIEWSTATEGENERATOR': ViewStateGenerator, 
			'__EVENTVALIDATION' : EventValidation,
			},
			meta = {'page': current_page},
			)]
			#print(dict(floor=floor, RoomNumber=RoomNumber, Pets=Pets, Dates=Dates, Price=Price))

		#java link to all rooms
		
		#response.xpath('//div[@id="fpHolder"]/a/@href').extract()
		#response.xpath('//div[@id="fpHolder"]/a/@href').extract()[page][25:112]


		
		

