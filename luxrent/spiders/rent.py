"""
To find rent prices from Amli Southshore only.  Need to build out to find all Amli sites.
"""
import scrapy
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
import datetime

from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response

#HEADERS = {
#	 'X-MicrosoftAjax': 'Delta=true',
#   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
#}



class RentSpider(scrapy.Spider):
	#Spider for finding all rooms available. Right now starting with only South-Shore.

#	start_urls = [
#	'https://www.amli.com/apartments/austin/central-austin/austin/aldrich/floorplans',
#	'https://www.amli.com/apartments/austin/central-east-austin/austin/south-shore/floorplans'
#	] 
	name = 'rent'	

	def start_requests(self):
		URLS = [
		'https://www.amli.com/apartments/austin/central-austin/austin/aldrich/floorplans',
		'https://www.amli.com/apartments/austin/downtown/austin/eastside/floorplans',
		'https://www.amli.com/apartments/austin/central-east-austin/austin/south-shore/floorplans',
		'https://www.amli.com/apartments/austin/central-austin/austin/mueller/floorplans',
		'https://www.amli.com/apartments/austin/west-austin/austin/covered-bridge/floorplans',
		'https://www.amli.com/apartments/austin/central-austin/austin/5350/floorplans',
		'https://www.amli.com/apartments/austin/2nd-street-district/austin/downtown/floorplans',
		'https://www.amli.com/apartments/austin/downtown/austin/2nd-street/floorplans',
		'https://www.amli.com/apartments/austin/downtown/austin/300/floorplans'
		]
		
		for page in URLS:
			yield scrapy.Request (
				url = page,
				callback = self.parse,
				meta = {'URL' : page} )

	def parse(self, response):
		#This is the main crawler that goes through all pages

		for x in range(len(response.xpath('//div[@id="fpHolder"]/a/@href').extract())):
			#Get Next Page
			URL = response.meta['URL']

			ViewState = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract().pop()
			ViewStateGenerator = response.xpath('//input[@id = "__VIEWSTATEGENERATOR"]/@value').extract().pop()
			EventValidation = response.xpath('//input[@id = "__EVENTVALIDATION"]/@value').extract().pop()
			EventTargetVariable = response.xpath('//div[@id="fpHolder"]/a/@href').extract()[x+1][25:112]
			
			#open_in_browser(response)
			
			yield FormRequest(
				url = URL,
				callback = self.parse_info,
				formdata= {
				'__EVENTTARGET' : EventTargetVariable, 
				'__EVENTARGUMENT' : '', '__VIEWSTATE' : ViewState,
				'__VIEWSTATEGENERATOR': ViewStateGenerator, 
				'__EVENTVALIDATION' : EventValidation,
				},
				meta = {'page': x},
				)
			#print(dict(floor=floor, RoomNumber=RoomNumber, Pets=Pets, Dates=Dates, Price=Price))


	def parse_info(self, response):
	# Get Results
	#Format: Date - Company - Building - City - Local Address - Floor Plan - Floor - Room# - Pets - Date Available - Price
	#format #2: Companies: [CompanyName:, Buildings:[buildingName:, CityAddress: , LocalAddress: , Room[] ]]
	#				
		currentFloorPlan = response.meta['page']
		dateToday = datetime.date.today()


		for data in response.xpath('//tr[@class="highlightRowClicked" or @class = "highlightRow"]'):
			yield {
				'Date' : dateToday.strftime("%d/%m/%y"),
				'Company' : response.xpath('//span[@style="font-weight:bold;"]/text()').extract().pop(),
				'Building' : response.xpath('//span[@style="font-weight:bold;"]/span/text()').extract_first(),
				'Floor Plan': response.xpath('//span[@style = "display: block; font-weight: bold; float:left; margin-left: 10px;"]/span/text()').extract()[currentFloorPlan],
				'City' : response.xpath('//span[@id="ContentMain_communityAddress2"]/text()').extract().pop(),
				'Local Address' : response.xpath('//span[@id="ContentMain_communityAddress"]/text()').extract().pop(),
				'Floor' : data.xpath('.//span[contains(@id, "Floor")]/text()').extract(),
				'Room Number' : data.xpath('.//span[contains(@id, "Number")]/text()').extract(),
				'Pets' : data.xpath('.//span[contains(@id, "Pets")]/text()').extract(),
				'Date Available' : data.xpath('.//span[contains(@id, "UnitDates")]/text()').extract(),
				'Price' : data.xpath('.//span[contains(@id, "Price")]/text()').extract(),
				}
		
		#java link to all rooms
		
		#response.xpath('//div[@id="fpHolder"]/a/@href').extract()
		#response.xpath('//div[@id="fpHolder"]/a/@href').extract()[page][25:112]