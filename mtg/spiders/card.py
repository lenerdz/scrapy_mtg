# -*- coding: utf-8 -*-
import scrapy

# https://blog.michaelyin.info/scrapy-tutorial-11-how-to-extract-data-from-native-javascript-statement/

class CardSpider(scrapy.Spider):
    name = 'card'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/price/Guilds+of+Ravnica/Pause+for+Reflection#paper']

    def parse(self, response):
        dates = response.css("script").re('n(2.*?), .*?";')
        prices = response.css("script").re('n2.*?, (.*?)";')
        n = 0
        for x in dates:
            yield {
                'date': dates[n],
                'price': prices[n]
            }
            n+=1