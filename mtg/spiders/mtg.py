# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request


class MtgSpider(scrapy.Spider):
    name = 'mtg'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/prices/select']

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        # urls = response.css("li > a::attr(href)").extract()
        for mtgset in response.css("li"):
            if mtgset.css("img::attr(src)") and mtgset.css("a::text"):
                link = url + mtgset.css("a::attr(href)")[0].extract()
                sets = {
                    'code': mtgset.css("img::attr(alt)")[0].extract(),
                    'name': mtgset.css("a::text")[1].extract(),
                    'icon': mtgset.css("img::attr(src)")[0].extract(),
                    'link': link
                }
                # yield sets
                yield scrapy.Request(sets["link"], self.parse_set)
                
    def parse_set(self, response):
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
        print("Finished "+cards["set"])