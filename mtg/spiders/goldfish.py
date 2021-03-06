# -*- coding: utf-8 -*-
import scrapy
import time
import re
import mysql.connector
from mysql.connector import Error


class GoldfishSpider(scrapy.Spider):
    name = 'goldfish'
    allowed_domains = ['mtggoldfish.com']
    start_urls = ['https://www.mtggoldfish.com/prices/select']

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        sets = []
        first = 0

        for mtgset in response.css("li"):
            if mtgset.css("img::attr(src)") and mtgset.css("a::text") and first<10:
                setcode = mtgset.css("a::attr(href)")[0].re('/index/(.*)')[0],
                setname = mtgset.css("a::text")[1].re('\n(.*)\n')[0],
                icon = mtgset.css("img::attr(src)")[0].extract(),
                set_url = url + mtgset.css("a::attr(href)")[0].extract()

                # print (setname)
                sets.append((setcode[0], setname[0], icon[0], set_url))
                card = yield scrapy.Request(set_url, self.parse_set)
                first+=1

        try:
            mySQLconnection = mysql.connector.connect(host='localhost', database='scrapy', user='root', password='vertrigo')
            insert_sets = "INSERT INTO sets (setcode, setname, icon, url) VALUES (%s, %s, %s, %s)"
            clear_sets = "TRUNCATE sets"
            cursor = mySQLconnection.cursor()
            cursor.execute(clear_sets)
            clear_cards = "TRUNCATE cards"
            cursor.execute(clear_cards)
            clear_prices = "TRUNCATE price"
            cursor.execute(clear_prices)
            cursor.executemany(insert_sets, sets)
            # print(cursor.statement)
            mySQLconnection.commit()
            cursor.close()
                    
        except Error as e :
            print ("Error while connecting to MySQL", e)

        finally:
            #closing database connection.
            if(mySQLconnection.is_connected()):
                mySQLconnection.close()
                print("MySQL connection is closed")
        
        pass 

    def parse_set(self, response):
        url = 'https://www.mtggoldfish.com'
        cards = []

        for card in response.css("tr"):
            if card.css("td.card > a::text"):
                setname = card.css("td:nth-child(2)::text")[0].extract()
                name = card.css("td.card > a::text")[0].extract()
                link = url + card.css("td.card > a::attr(href)")[0].extract()
                image = card.css("td.card > a::attr(data-full-image)")[0].extract()

                cards.append((setname, name, link, image))
                p = yield scrapy.Request(link, self.parse_card)
                print(setname+' - '+name)


        mySQLconnection = mysql.connector.connect(host='localhost', database='scrapy', user='root', password='vertrigo')
        insert_cards = "INSERT INTO cards (setcode, name, url, image) VALUES (%s, %s, %s, %s)"
        cursor = mySQLconnection.cursor()
        cursor.executemany(insert_cards, cards)
        # print(cursor.statement)
        mySQLconnection.commit()
        cursor.close()
        mySQLconnection.close()
        # print(cards)
        print('--------------------------------------------------------')


    def parse_card(self, response):
        url = 'https://www.mtggoldfish.com'
        prices = []
        # https://www.mtggoldfish.com/price/Ixalan/Search+for+Azcanta#paper

        cardname = response.css("div.price-card-name-header-name::text").extract_first().replace("\n", "")
        setname = response.css("img.price-card-name-set-symbol::attr(alt)").extract_first()

        history = response.css("script").re('(var d (.*\n)*?)g = new')
        paper = history[0]
        online = history[2]

        # (\"\\n(.*), (.*)\")

        paper_prices = re.findall(r'(\"\\n(.*), (.*)\")', paper)
        online_prices = re.findall(r'(\"\\n(.*), (.*)\")', online)

        for row in paper_prices:
            date = row[1]
            price = row[2]

            prices.append((setname, cardname, date, price, 'paper'))
            # print(setname+' - '+cardname+' - '+date+' - '+price+' - paper')

        for row in online_prices:
            date = row[1]
            price = row[2]

            prices.append((setname, cardname, date, price, 'online'))
            # print(setname+' - '+cardname+' - '+date+' - '+price+' - online')

        mySQLconnection = mysql.connector.connect(host='localhost', database='scrapy', user='root', password='vertrigo')
        insert_prices = "INSERT INTO price (setname, name, date, price, type) VALUES (%s, %s, %s, %s, %s)"
        cursor = mySQLconnection.cursor()
        cursor.executemany(insert_prices, prices)
        # print(cursor.statement)
        mySQLconnection.commit()
        cursor.close()
        mySQLconnection.close()