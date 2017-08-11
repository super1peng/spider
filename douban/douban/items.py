# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	movie = scrapy.Field()
	title = scrapy.Field()
	date = scrapy.Field()
	num = scrapy.Field()
	content = scrapy.Field()
	score = scrapy.Field()

	pass
