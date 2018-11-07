# -*- coding: utf-8 -*-
import scrapy
import json


class CardsSpider(scrapy.Spider):
    name = 'cards'
    allowed_domains = ['mtggoldfish.com']
    # start_urls = ['https://www.mtggoldfish.com/prices/select']

    with open('data/sets.json') as f:
        data = json.load(f)

    start_urls = []
    for x in data:
        start_urls.append(x['url'])

    custom_settings = {
        'MYSQL_TABLE': 'cards'
    }

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        for card in response.css("tr"):
            if card.css("td.card > a::text"):
                link = url + card.css("td.card > a::attr(href)")[0].extract()
                cards = {
                    'setcode': card.css("td:nth-child(2)::text")[0].extract(),
                    'name': card.css("td.card > a::text")[0].extract(),
                    'url': link,
                    'image': card.css("td.card > a::attr(data-full-image)")[0].extract()
                }
                yield cards
        print("Finished "+cards["setcode"])
