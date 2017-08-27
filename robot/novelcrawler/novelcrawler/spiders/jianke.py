# -*- coding: utf-8 -*-
import scrapy


class JiankeItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


class JiankeSpider(scrapy.Spider):
    name = 'jianke'
    allowed_domains = ['www.xxbiquge.com']
    start_urls = ['http://www.xxbiquge.com/2_2327/']

    def parse(self, response):
        for href in response.css("#list > dl > dd > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    @staticmethod
    def parse_dir_contents(response):
        item = JiankeItem()
        item['title'] = response.css("div.bookname > h1").extract_first()
        item['link'] = response.url
        item['desc'] = response.css("#content").extract_first()
        yield item
