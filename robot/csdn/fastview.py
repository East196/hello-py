#!/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding:utf-8 -*-
import random

import requests
from lxml import etree
import time


def auto_click(url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    # random.choice(proxys)
    # 获取最后一页的链接
    resp = requests.get(url, headers=req_headers)
    if resp.status_code == requests.codes.ok:
        html = etree.HTML(resp.text)
        print(html)
        last_page_num = 1

        last_page_link = html.xpath('//div[@class="pagelist"]/a[last()]/@href')
        if last_page_link:
            last_page_link = last_page_link[0]
            last_page_num = int(last_page_link[-1])  # 最后一页页码

        # 构建所有页面的链接
        base_page_link = url + '/article/list/'
        for i in range(1, last_page_num + 1):
            real_page_link = base_page_link + str(i)
            print(real_page_link)
            for j in range(5):
                # 提取本页所有文章链接
                resp = requests.get(real_page_link, headers=req_headers)
                if resp.status_code == requests.codes.ok:
                    html = etree.HTML(resp.text)
                    article_links = html.xpath('//li[@class="blog-unit"]/a/@href')  # 新版博客目录
                    if not article_links:
                        article_links = html.xpath('//span[@class="link_title"]/a/@href')  # 旧版博客目录
                        article_links = ['https://blog.csdn.net' + article_link for article_link in article_links]
                    # 访问每一篇文章，模拟点击
                    article_link = random.choice(article_links)
                    requests.get(article_link, headers=req_headers)
                    time.sleep(1)
                    print('正在第 [{0}] 次点击 {1}'.format(j, article_link))
                    # for article_link in article_links:
                    #     print(article_link)
                    #     requests.get(article_link, headers=req_headers)
                    #     time.sleep(1)
                    #     print('正在第 [{0}] 次点击 {1}'.format(num, article_link))
            time.sleep(2)


if __name__ == '__main__':
    blogs = ["http://blog.csdn.net/q809198545", "http://blog.csdn.net/east196"]
    for _ in range(10):
        blog = random.choice(blogs)
        for blog in blogs:
            auto_click(blog)
