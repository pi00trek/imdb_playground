# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, Compose, MapCompose


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
    runtime = scrapy.Field()
    budget = scrapy.Field()
    opening_weekend_USA = scrapy.Field()
    gross_USA = scrapy.Field()
    cumulative_world_gross = scrapy.Field()


def genres_cleanup(genres_item):
    if not (genres_item == ' ' or genres_item[:5] == 'See A'):
        return genres_item


class MovieLoader(ItemLoader):
    default_output_processor = Identity()

    genres_out = MapCompose(genres_cleanup, str.strip)
    # # year =
    extra_info = Identity()
    # rating =
    # rating_count =
    # metacritic_rating =
    # runtime =
    budget_out = Compose(lambda x: x[1].split('\n')[0], str.strip)
    opening_weekend_USA_out = Compose(lambda x: x[1].split(',\n')[0], str.strip)
    gross_USA_out = Compose(lambda x: x[1], str.strip)
    cumulative_world_gross_out = Compose(lambda x: x[1], str.strip)