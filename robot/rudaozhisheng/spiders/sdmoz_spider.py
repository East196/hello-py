import scrapy


class SmallDmozSpider(scrapy.Spider):
    name = "sdmoz"
    allowed_domains = ["biquge.tw"]
    start_urls = [
        "http://www.biquge.tw/0_52/"
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="list"]/dl/dd'):
            yield {
                'title': sel.xpath('a/text()').extract()[0],
                'link': sel.xpath('a/@href').extract()[0],
                'desc': sel.xpath('text()').extract()[0],
                'url': response.urljoin(sel.xpath('a/@href').extract()[0])
            }
