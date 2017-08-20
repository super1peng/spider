# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    like = scrapy.Field()       #点赞数
    transfer = scrapy.Field()   #转载数
    comment = scrapy.Field()    #评论数
    pass
