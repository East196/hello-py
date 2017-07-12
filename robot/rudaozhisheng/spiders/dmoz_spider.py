import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    url = scrapy.Field()


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["biquge.tw"]
    start_urls = [
        "http://www.biquge.tw/0_52/"
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="list"]/dl/dd'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()[0]
            item['link'] = sel.xpath('a/@href').extract()[0]
            item['desc'] = sel.xpath('text()').extract()[0]
            item['url'] = response.urljoin(sel.xpath('a/@href').extract()[0])
            yield item
