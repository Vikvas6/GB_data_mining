# -*- coding: utf-8 -*-
import scrapy
from kinopoisk_parser.items import KinopoiskParserItem, PersonItem
from time import sleep
import random

class KinopoiskSpider(scrapy.Spider):
    name = 'kinopoisk'
    allowed_domain = ['kinopoisk.ru']
    start_urls = ['https://www.kinopoisk.ru/top/lists/']

    def parse(self, response):
        list_links = response.xpath('//td[@id="block_left_pad"]//div[contains(@class,"list_main")]//a/@href').getall()
        for link in list_links:
            print(link)
            yield response.follow(link, callback=self.list_parse)

    def list_parse(self, response):
        sleep(2 + 2 * random.random())
        next_page = response.xpath('//td[@id="block_left_pad"]//div[@class="navigator"]//a[text()="»"]/@href').get()

        items = response.xpath('//table[@id="itemList"]//a[@class="all"]/@href').getall()
        for item in items:
            yield response.follow(item, callback=self.item_parse)
        
        if next_page:
            yield response.follow(next_page, callback=self.list_parse)

    def item_parse(self, response):
        sleep(2 + 2 * random.random())
        
        director_raw = response.xpath(f'{self._create_xpath_for_info_table_short("режиссер")}//a')
        director = []
        yield self._process_persons(director_raw, director, 'director')
        
        writers_raw = response.xpath(f'{self._create_xpath_for_info_table_short("сценарий")}//a')
        writers = []
        yield self._process_persons(writers_raw, writers, 'writer')
        
        producer_raw = response.xpath(f'{self._create_xpath_for_info_table_short("продюсер")}//a')
        producer = []
        yield self._process_persons(producer_raw, producer, 'producer')
        
        crew1_raw = response.xpath(f'{self._create_xpath_for_info_table_short("оператор")}//a')
        crew1 = []
        yield self._process_persons(crew1_raw, crew1, 'Other')
        
        crew2_raw = response.xpath(f'{self._create_xpath_for_info_table_short("композитор")}//a')
        crew2 = []
        yield self._process_persons(crew2_raw, crew2, 'Other')
        
        crew3_raw = response.xpath(f'{self._create_xpath_for_info_table_short("художник")}//a')
        crew3 = []
        yield self._process_persons(crew3_raw, crew3, 'Other')
        
        crew4_raw = response.xpath(f'{self._create_xpath_for_info_table_short("монтаж")}//a')
        crew4 = []
        yield self._process_persons(crew4_raw, crew4, 'Other')

        crew = []
        crew.extend(crew1)
        crew.extend(crew2)
        crew.extend(crew3)
        crew.extend(crew4)

        budget = response.xpath(self._create_xpath_for_info_table('бюджет')).get()
        if budget:
            budget = budget.replace('\xa0', '')

        box_office = response.xpath(self._create_xpath_for_info_table('сборы в мире')).get()
        if box_office:
            box_office = box_office.replace('\xa0', '')

        data = {
            'name': response.xpath('//div[@id="headerFilm"]/h1[@itemprop="name"]/span/text()').get(),
            'english_name': response.xpath('//div[@id="headerFilm"]/span[@itemprop="alternativeHeadline"]/text()').get(),
            'year': response.xpath(self._create_xpath_for_info_table('год')).get(),
            'country': response.xpath(self._create_xpath_for_info_table('страна')).get(),
            'slogan': response.xpath(f'{self._create_xpath_for_info_table_short("слоган")}/text()').get(),
            'director': director,
            'writers': writers,
            'producer': producer,
            'other_crew': crew,
            'genres': response.xpath(f'{self._create_xpath_for_info_table_short("жанр")}/span[@itemprop="genre"]/a/text()').getall(),
            'budget': budget,
            'box_office': box_office,
            'release_date': response.xpath(self._create_xpath_for_info_table('премьера (мир)')).get(),
            'runtime': response.xpath('//td[@id="runtime"]/text()').get().rstrip()
        }

        item = KinopoiskParserItem(**data)

        yield item 

    def _create_xpath_for_info_table(self, name):
        return f'{self._create_xpath_for_info_table_short(name)}//a/text()'

    def _create_xpath_for_info_table_short(self, name):
        return f'//div[@id="infoTable"]//td[text()="{name}"]//following-sibling::td'
    
    def _process_persons(self, raw, crew_list, position):
        for person in raw:
            person_data = {
                'url': person.xpath('.//@href').get(),
                'name': person.xpath('.//text()').get()
            }
            crew_list.append({
                'url': person.xpath('.//@href').get(),
                'position': position
            })
            person_item = PersonItem(**person_data)
            yield person_item
