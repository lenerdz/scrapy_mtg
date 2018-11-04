# -*- coding: utf-8 -*-
import scrapy


class CardsSpider(scrapy.Spider):
    name = 'cards'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/index/M10#paper']

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        for card in response.css("tr"):
            if card.css("td.card > a::text"):
                link = url + card.css("td.card > a::attr(href)")[0].extract()
                cards = {
                    'set': card.css("td:nth-child(2)::text")[0].extract(),
                    'name': card.css("td.card > a::text")[0].extract(),
                    'link': link,
                    'image': card.css("td.card > a::attr(data-full-image)")[0].extract()
                }
                yield cards
