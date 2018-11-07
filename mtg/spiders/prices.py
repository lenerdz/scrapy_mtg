# -*- coding: utf-8 -*-
import scrapy
import json
import time

# https://blog.michaelyin.info/scrapy-tutorial-11-how-to-extract-data-from-native-javascript-statement/

class CardSpider(scrapy.Spider):
    name = 'prices'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/price/Dragons+of+Tarkir/Stormrider+Rig#paper']

    custom_settings = {
        'MYSQL_TABLE': 'prices'
    }
    def parse(self, response):
        with open('data/cardlist.json') as f:
            data = json.load(f)

        cardlist=[]
        temp=[]
        # Foreach card, execute it
        for x in data:
            # If the card was not processed before or was processed and throttled, execute it
            if x["error"] <= 0:
                temp = scrapy.Request(x["url"], self.parse_price)
                # temp['id'] = x['id']
                # cardlist.append(x)
                if temp != 'error':
                    # temp["id"] = x["id"]
                    x["error"] = -1
                    cardlist.append(x)
                    yield temp
                else:
                    x["error"] = 1
                    cardlist.append(x)
            else:
                cardlist.append(x)
        with open('data/cardlist-processed.json', 'w') as newfile:
            json.dump(cardlist, newfile, indent=2)

    def parse_price(self, response):
        history = response.css("script").re('(var d (.*\n)*?)g = new')
        # dates[0] = dates[0].replace("\n", "")
        # dates[0] = dates[0].replace("\"", "")
        # dates[0] = dates[0].replace("d += \\", "")
        # vals = re.split('n(2.*?),', dates[0])
        # vals = vals.group(0)
        # yield {
        #     'paper-price-history': history[0],
        #     'online-price-history': history[2]
        # }
        # prices = response.css("script").re('n2.*?, (.*?)";')
        cardname = response.css("div.price-card-name-header-name::text")
        # if cardname:
        # card = cardname.re('\n(.*)\n')[0]
        card = cardname.extract_first()
        if card:
            card = card.replace("\n", "")
        # else:
        #     card = "------------"
        setname = response.css("img.price-card-name-set-symbol::attr(alt)").extract_first()
        # if not setname:
        #     setname = '???'
        # n = 0
        # for x in dates:
        
        # print(history)
        
        # if setname:
        if len(history)>3:
            # print(history)
            # card = cardname.re('\n(.*)\n')[0]
            print('PARSED CARD '+card)
            return {
                'setcode': setname,
                'name': card,
                'paper': history[0],
                'online': history[2]
            }
        elif len(history)>1:
            # cards = cardname.re('\n(.*)\n')[0]
            print('PARSED CARD '+card)
            return {
                'setcode': setname,
                'name': card,
                'paper': history[0],
                'online': ''
            }
        else:
            print (response.text)
            time.sleep(10)
            return 'error'
        #     n+=1
