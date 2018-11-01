# -*- coding: utf-8 -*-
import scrapy


class MtgSpider(scrapy.Spider):
    name = 'mtg'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/prices/select']

    def parse(self, response):
        for mtgset in response.css("li"):
            if mtgset.css("img::attr(src)") and mtgset.css("a::text"):
                yield {
                    'name': mtgset.css("a::text")[1].extract(),
                    'icon': mtgset.css("img::attr(src)")[0].extract(),
                    'link': mtgset.css("a::attr(href)")[0].extract()
                }