# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarRentalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	pickupDate = scrapy.Field()
	returnDate = scrapy.Field()
	carClass = scrapy.Field()
	carType = scrapy.Field()
	dailyPrice = scrapy.Field()
	totalPrice = scrapy.Field()

    pass
