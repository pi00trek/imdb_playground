# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Movies(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    extra_info = scrapy.Field()
    genres = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    metacritic_rating = scrapy.Field()

