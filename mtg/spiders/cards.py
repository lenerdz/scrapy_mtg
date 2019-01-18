# -*- coding: utf-8 -*-
import scrapy
import json
import mysql.connector
from mysql.connector import Error


class CardsSpider(scrapy.Spider):
    name = 'cards'
    allowed_domains = ['mtggoldfish.com']
    # start_urls = ['https://www.mtggoldfish.com/prices/select']
    start_urls = []

    # with open('data/sets.json') as f:
    #     data = json.load(f)

    try:
        mySQLconnection = mysql.connector.connect(host='localhost', database='scrapy', user='root', password='root')
        sql_select_Query = "select * from sets"
        cursor = mySQLconnection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of sets - ", cursor.rowcount)
        for row in records:
            # print(row[2])
            start_urls.append(row[4])
        cursor.close()
        
    except Error as e :
        print ("Error while connecting to MySQL", e)

    finally:
        #closing database connection.
        if(mySQLconnection.is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")

    # for x in data:
    #     start_urls.append(x['url'])

    custom_settings = {
        'MYSQL_TABLE': 'cards'
    }

    def parse(self, response):
        url = 'https://www.mtggoldfish.com'
        for card in response.css("tr"):
            if card.css("td.card > a::text"):
                link = url + card.css("td.card > a::attr(href)")[0].extract()
                cards = {
                    'setcode': card.css("td:nth-child(2)::text")[0].extract(),
                    'name': card.css("td.card > a::text")[0].extract(),
                    'url': link,
                    'image': card.css("td.card > a::attr(data-full-image)")[0].extract()
                }
                yield cards
        print("Finished "+cards["setcode"])
