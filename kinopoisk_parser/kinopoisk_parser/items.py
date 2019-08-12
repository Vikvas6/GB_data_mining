# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KinopoiskParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    english_name = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    slogan = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field()
    producer = scrapy.Field()
    other_crew = scrapy.Field()
    genres = scrapy.Field()
    budget = scrapy.Field()
    box_office = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()

class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    url_id = scrapy.Field()
    name = scrapy.Field()
