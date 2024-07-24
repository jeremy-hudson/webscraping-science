# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    # define the fields for your item here like:
    article_type = scrapy.Field()
    access = scrapy.Field()
    access_label = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    src_title = scrapy.Field()
    src_url = scrapy.Field()
    src_extra = scrapy.Field()
    authors = scrapy.Field()
    out_position = scrapy.Field()
