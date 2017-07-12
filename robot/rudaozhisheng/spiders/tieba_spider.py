#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2

import scrapy


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ['http://tieba.baidu.com/f?kw=blackpink&ie=utf-8']

    def parse(self, response):
        with open("tieba.html","w") as f:
            f.write(response.text.encode("utf-8"))

        for href in response.css('.threadlist_title a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('.core_title_txt::text').extract_first().strip(),
            'body': response.css('cc>div::text').extract_first().strip(),
            'link': response.url,
        }