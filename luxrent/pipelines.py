# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import os
con = None

class LuxrentPipeline(object):
    
    def __init__(self):
    	self.setupDBCon()
    	self.createTables()

    def setupDBCon(self):
    	self.conn = sqlite3.connect(os.getcwd() + '/LuxData.sqlite')
    	self.cur = self.conn.cursor()

    def createTables(self):
    	self.dropLuxTable()
    	self.createLuxTable()

    def dropLuxTable(self):
    	#drop table if it exists
    	self.cur.execute("DROP TABLE IF EXISTS Lux")

    def closeDB(self):
    	self.conn.close()
        
    def __del__(self):
        self.closeDB()    

    def createLuxTable(self):
	   	self.cur.execute(
	   		'''CREATE TABLE IF NOT EXISTS Lux(
	   		id INTEGER PRIMARY KEY NOT NULL,
	   		Date TEXT,
	   		Company TEXT,
	   		Building TEXT,
	   		Floorplan TEXT,
	   		City TEXT,
	   		Localaddress TEXT,
	   		Floor TEXT,
	   		Roomnumber TEXT,
	   		Dateavailable TEXT,
	   		Price TEXT
	   		)'''
	   	)

    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def storeInDb(self, item):
    	self.cur.execute(
    		'''INSERT INTO Lux (
    			Date,
    			Company, 
    			Building, 
    			Floorplan, 
    			City, 
    			Localaddress,
    			Floor,
    			Roomnumber,
    			Dateavailable,
    			Price) 
    		VALUES (?,?,?,?,?,?,?,?,?,?)''',
    		(item['Date'],
    		item['Company'],
    		item['Building'],
    		item['Floorplan'],
    		item['City'],
    		item['Localaddress'],
    		item['Floor'],
    		item['Roomnumber'],
    		item['Dateavailable'],
    		item['Price']
    		))

    	print("Data Stored")
    	self.conn.commit()