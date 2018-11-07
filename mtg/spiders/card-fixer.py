# -*- coding: utf-8 -*-
import scrapy
import json


class CardsSpider(scrapy.Spider):
    name = 'card-fixer'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/prices/select']

    custom_settings = {
        'MYSQL_TABLE': 'cards'
    }

    def parse(self, response):
        with open('data/cardlist.json') as f:
            data = json.load(f)

        for x in data:
            yield x
