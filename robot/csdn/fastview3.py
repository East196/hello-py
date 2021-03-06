#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random

import requests

from robot.csdn.fastlist import *


def auto_click(articles, proxies=[]):
    if not articles:
        return
    for ip in proxies:
        useful = is_useful(ip)
        print(ip, useful)
        if not useful:
            continue
        for _ in range(len(articles)):
            article_link = random.choice(articles)
            print(ip, article_link)
            try:
                requests.get(protoarticle(ip, article_link), timeout=TIME_OUT, headers=req_headers,
                             proxies=ip2proxy(ip))
                print((article_link, "ok"))
                time.sleep(0.25)
            except Exception as e:
                print((article_link, "fail", e))
                time.sleep(0.1)
                break


if __name__ == '__main__':
    # blogs = ["https://blog.csdn.net/east196", "https://blog.csdn.net/q809198545"]
    blog = "https://blog.csdn.net/east196"
    articles = ['{}/article/details/{}'.format(blog, article_id) for article_id in get_article_ids(blog)]
    print("articles:", articles)
    proxies = get_proxy(page=1)
    while True:
        auto_click(articles, proxies)
