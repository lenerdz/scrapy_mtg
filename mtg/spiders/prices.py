# -*- coding: utf-8 -*-
import scrapy
import re

# https://blog.michaelyin.info/scrapy-tutorial-11-how-to-extract-data-from-native-javascript-statement/

class CardSpider(scrapy.Spider):
    name = 'prices'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/price/Dragons+of+Tarkir/Stormrider+Rig#paper']

    def parse(self, response):
        history = response.css("script").re('(var d (.*\n)*?)g = new')
        # dates[0] = dates[0].replace("\n", "")
        # dates[0] = dates[0].replace("\"", "")
        # dates[0] = dates[0].replace("d += \\", "")
        # vals = re.split('n(2.*?),', dates[0])
        # vals = vals.group(0)
        yield {
            'paper-price-history': history[0],
            'online-price-history': history[2]
        }
        # prices = response.css("script").re('n2.*?, (.*?)";')
        # cardname = response.css("div.price-card-name-header-name::text")
        # if cardname:
        #     card = cardname.re('\n(.*)\n')[0]
        # else:
        #     card = "------------"
        # setname = response.css("img.price-card-name-set-symbol::attr(alt)").extract_first()
        # if not setname:
        #     setname = '???'
        # n = 0
        # for x in dates:
        #     yield {
        #         'set': setname,
        #         'name': card,
        #         'date': dates[n],
        #         'price': prices[n]
        #     }
        #     n+=1