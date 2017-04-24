# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    url = scrapy.Field(default='null')
    country = scrapy.Field(default='null')
    state = scrapy.Field(default='null')
    reg_num = scrapy.Field(default='null')
    address = scrapy.Field(default='null')
    foreign_principal = scrapy.Field(default='null')
    date = scrapy.Field(default='null')
    registrant = scrapy.Field(default='null')
    exhibit_url = scrapy.Field(default='null')
