# -*- coding: utf-8 -*-
import scrapy


class SetsSpider(scrapy.Spider):
    name = 'sets'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/prices/select']

    custom_settings = {
        'MYSQL_TABLE': 'sets'
    }

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        for mtgset in response.css("li"):
            if mtgset.css("img::attr(src)") and mtgset.css("a::text"):
                link = url + mtgset.css("a::attr(href)")[0].extract()
                sets = {
                    'code': mtgset.css("img::attr(alt)")[0].extract(),
                    'name': mtgset.css("a::text")[1].re('\n(.*)\n')[0],
                    'icon': mtgset.css("img::attr(src)")[0].extract(),
                    'url': link
                }
                yield sets
