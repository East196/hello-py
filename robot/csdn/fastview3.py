#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .fastlist import *


def auto_click(articles, proxies=[]):
    if not articles:
        return
    for ip in proxies:
        if not is_useful(ip):
            continue
        for _ in range(40):
            article_link = random.choice(articles)
            try:
                requests.get(protoarticle(article_link), timeout=TIME_OUT, headers=req_headers, proxies=ip2proxy(ip))
                print((article_link, "ok"))
                time.sleep(0.25)
            except:
                print((article_link, "fail"))
                time.sleep(0.1)
                break


if __name__ == '__main__':
    # blogs = ["https://blog.csdn.net/east196", "https://blog.csdn.net/q809198545"]
    blog = "https://blog.csdn.net/east196"
    articles = ['{}/article/list/{}'.format(blog, article_id) for article_id in get_article_ids(blog)]
    while True:
        proxies = get_proxy(page=1)
        # useful_ips = get_useful_ips(proxies)
        # print(useful_ips)
        auto_click(articles, proxies)
