# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from bs4 import BeautifulSoup


class RudaozhishengPipeline(object):
    def process_item(self, item, spider):
        soup = BeautifulSoup(item['title'], 'html.parser')
        item['title'] = soup.get_text()
        soup = BeautifulSoup(item['desc'], 'html.parser')
        item['desc'] = soup.get_text().replace("readx();","").strip()
        return item


class TutorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('rudaozhisheng.txt', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + '\n'
        # self.file.write(line.decode("unicode_escape"))
        self.file.write(item['title']+"=====\n")
        self.file.write(item['desc']+"\n")
        return item
