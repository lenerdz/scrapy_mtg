# -*- coding: utf-8 -*-
import scrapy


class CardsSpider(scrapy.Spider):
    name = 'cards'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/prices/select']

    custom_settings = {
        'MYSQL_TABLE': 'cards'
    }

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        for mtgset in response.css("li"):
            if mtgset.css("img::attr(src)") and mtgset.css("a::text"):
                link = url + mtgset.css("a::attr(href)")[0].extract()
                yield scrapy.Request(link, self.parse_set)

    def parse_set(self, response):
        url = 'https://www.mtggoldfish.com'
        for card in response.css("tr"):
            if card.css("td.card > a::text"):
                link = url + card.css("td.card > a::attr(href)")[0].extract()
                cards = {
                    'setname': card.css("td:nth-child(2)::text")[0].extract(),
                    'name': card.css("td.card > a::text")[0].extract(),
                    'link': link,
                    'image': card.css("td.card > a::attr(data-full-image)")[0].extract()
                }
                yield cards
