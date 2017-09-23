# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LuxrentItem(scrapy.Item):
    # define the fields for your item here like:
    Date = scrapy.Field()
    Company = scrapy.Field()
    Building = scrapy.Field()
    Floorplan = scrapy.Field()
    City = scrapy.Field()
    Localaddress = scrapy.Field()
    Floor = scrapy.Field()
    Roomnumber = scrapy.Field()
    Pets = scrapy.Field()
    Dateavailable = scrapy.Field()
    Price = scrapy.Field()

    
