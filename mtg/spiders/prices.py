# -*- coding: utf-8 -*-
import scrapy
import json
import time
import mysql.connector
from mysql.connector import Error

# https://blog.michaelyin.info/scrapy-tutorial-11-how-to-extract-data-from-native-javascript-statement/

class CardSpider(scrapy.Spider):
    name = 'prices'
    allowed_domains = ['mtggoldfish.com']
    # start_urls = ['https://www.mtggoldfish.com/price/Dragons+of+Tarkir/Stormrider+Rig#paper']
    start_urls=[]

    # with open('data/cardlist.json') as f:
    #     cardlist = json.load(f)
    #     total_cards = len(cardlist)
    # for x in cardlist:
    #     start_urls.append(x['url'])

    try:
        mySQLconnection = mysql.connector.connect(host='localhost', database='scrapy', user='root', password='root')
        sql_select_Query = "select * from cards"
        cursor = mySQLconnection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of cards - ", cursor.rowcount)
        total_cards = cursor.rowcount
        for row in records:
            # print(row[2])
            start_urls.append(row[3])
        cursor.close()
        
    except Error as e :
        print ("Error while connecting to MySQL", e)

    finally:
        #closing database connection.
        if(mySQLconnection.is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")


    error = False
    error_count = 0
    current_card = 0
    errorlist=[]

    custom_settings = {
        'MYSQL_TABLE': 'prices'
    }

    def parse(self, response):
        

    #     temp=[]
    #     # Foreach card, execute it
    #     for x in data:
    #         # If the card was not processed before or was processed and throttled, execute it
    #         if x["error"] <= 0:
    #             temp = scrapy.Request(x["url"], self.parse_price)
    #             # temp['id'] = x['id']
    #             # cardlist.append(x)
    #             if not self.error:
    #                 # temp["id"] = x["id"]
    #                 x["error"] = -1
    #                 cardlist.append(x)
    #                 yield temp
    #             else:
    #                 x["error"] = 1
    #                 cardlist.append(x)
    #                 errorlist.append(x)
    #         else:
    #             cardlist.append(x)

        

    # def parse_price(self, response):
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
        self.current_card+=1
        if len(history)>3:
            # print(history)
            # card = cardname.re('\n(.*)\n')[0]
            print('PARSED CARD '+str(self.current_card)+ ' of '+str(self.total_cards)+' | '+str("{0:.2f}".format(self.current_card/self.total_cards*100))+'% | '+str(self.error_count)+' errors | '+card)
            self.error = False
            yield {
                'setcode': setname,
                'name': card,
                'paper': history[0],
                'online': history[2]
            }
        elif len(history)>1:
            # cards = cardname.re('\n(.*)\n')[0]
            print('PARSED CARD '+str(self.current_card)+ ' of '+str(self.total_cards)+' | '+str("{0:.2f}".format(self.current_card/self.total_cards*100))+'% | '+str(self.error_count)+' errors | '+card)
            self.error = False
            yield {
                'setcode': setname,
                'name': card,
                'paper': history[0],
                'online': ''
            }
        else:
            self.error_count+=1
            self.errorlist.append(response.url)
            print('PARSED CARD '+str(self.current_card)+ ' of '+str(self.total_cards)+' | '+str("{0:.2f}".format(self.current_card/self.total_cards*100))+'% | '+str(self.error_count)+' errors.')
            print (response.text)
            # for count in reversed(range(1, 60)):
            print("Restarting in 1 minute...")
            time.sleep(60)
            # print("Restarting in "+str(count)+"...")
            self.error = True
            # return False
        #     n+=1

    def spider_closed(self, spider):
        with open('data/errorlist.json', 'w') as errors:
            json.dump(self.errorlist, errors, indent=2)