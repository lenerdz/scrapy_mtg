# -*- coding: utf-8 -*-
import scrapy


class ScgSpider(scrapy.Spider):
    name = 'scg'
    allowed_domains = ['starcitygames.com']
    start_urls = [
        'http://www.starcitygames.com/catalog/magic_the_gathering/?t=english_singles']

    def parse(self, response):
        for sets in response.css('ul.cardset_lists>li'):
            tset = {
                'name': sets.css('a::text').extract_first(),
                'link': sets.css('a::attr(href)').extract_first()
            }
            # yield tset
            yield scrapy.Request(tset['link'], self.parse_set)

    def parse_set(self, response):
        name = ''
        for cards in response.css('tr.deckdbbody_row, tr.deckdbbody2_row'):
            if cards.css("td.search_results_1>b>a::text").extract():
                name = cards.css("td.search_results_1>b>a::text").extract_first()
                name = name.replace("\n", "")
            if cards.css("td.search_results_2>a::text").extract():
                tset = cards.css("td.search_results_2>a::text").extract_first()
            if cards.css("td.search_results_9>span:last-of-type"):
                price = cards.css(
                    "td.search_results_9>span:last-of-type::text").extract_first()
            else:
                price = cards.css("td.search_results_9::text").extract_first()
            if not price:
                price = ""
            price = price.replace("$", "")
            yield {
                'set': tset,
                'name': name,
                'condition': cards.css("td.search_results_7>a::text").extract_first(),
                'qtd': cards.css("td.search_results_8::text").extract_first(),
                'price': price
            }

        link = response.css('section#content > div:last-child > a:last-of-type::attr(href)').extract_first()
        if response.css('section#content > div:last-child > a:last-of-type::text').extract_first() == ' - Next>> ':
            yield scrapy.Request(link, self.parse_set)

