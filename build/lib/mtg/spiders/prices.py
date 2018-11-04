# -*- coding: utf-8 -*-
import scrapy

# https://blog.michaelyin.info/scrapy-tutorial-11-how-to-extract-data-from-native-javascript-statement/

class CardSpider(scrapy.Spider):
    name = 'prices'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/price/Guilds+of+Ravnica/Pause+for+Reflection#paper']

    def parse(self, response):
        dates = response.css("script").re('n(2.*?), .*?";')
        prices = response.css("script").re('n2.*?, (.*?)";')
        card = response.css("div.price-card-name-header-name::text").re('\n(.*)\n')[0] #extract()[0]
        set = response.css("img.price-card-name-set-symbol::attr(alt)").extract()[0]
        n = 0
        for x in dates:
            yield {
                'set': set,
                'name': card,
                'date': dates[n],
                'price': prices[n]
            }
            n+=1