# -*- coding: utf-8 -*-

import scrapy

from robot.rudaozhisheng import RudaozhishengItem


class RudaozhishengSpider(scrapy.Spider):
    name = "rudaozhisheng"
    allowed_domains = ["biquge.tw"]
    start_urls = [
        "http://www.biquge.tw/0_52/"
    ]

    def parse(self, response):
        for href in response.css("#list > dl > dd > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    @staticmethod
    def parse_dir_contents(response):
        item = RudaozhishengItem()
        item['title'] = response.css("div.bookname > h1").extract_first()
        item['link'] = response.url
        item['desc'] = response.css("#content").extract_first()
        yield item
