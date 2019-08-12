# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from kinopoisk_parser.items import KinopoiskParserItem, PersonItem

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.kinopoisk

class KinopoiskParserPipeline(object):
    COLLECTION = MONGO_DB.films
    def process_item(self, item, spider):
        if (isinstance(item, KinopoiskParserItem)):
            _ = self.COLLECTION.insert_one(item)
        return item

class PersonPipeline(object):
    COLLECTION = MONGO_DB.persons
    def process_item(self, item, spider):
        if (isinstance(item, PersonItem)):
            if not self.COLLECTION.find_one(item):
                _ = self.COLLECTION.insert_one(item)
        return item
