#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from gevent import monkey

monkey.patch_socket()
import gevent

import requests
import time
from bs4 import BeautifulSoup

req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

TIME_OUT = 15


def get_page_num(blog):
    # 获取最后一页的链接
    resp = requests.get(blog, timeout=TIME_OUT, headers=req_headers)
    soup = BeautifulSoup(resp.text, "lxml")
    page_as = soup.select("li.page-item > a")
    if not page_as:
        return 1
    page_num = page_as[-1].get("data-ci-pagination-page")
    print("page_num:", page_num)
    return page_num


def get_article_ids(blog):
    article_ids = []
    try:
        page_num = get_page_num(blog)

        for page in range(1, int(page_num) + 1):
            url = blog + "/article/list/" + str(page)
            print url
            resp = requests.get(url, timeout=TIME_OUT, headers=req_headers)
            soup = BeautifulSoup(resp.text, "lxml")
            article_as = soup.select("li.blog-unit a")
            article_ids += [article_a.get("href").split("details/")[1] for article_a in article_as]
            print len(article_ids), article_ids
    except:
        pass

    return article_ids


def get_proxy(page=10):
    proxies = []
    try:
        for p in range(1, page + 1):
            resp = requests.get("http://www.xicidaili.com/nn/%s" % p, timeout=TIME_OUT, headers=req_headers)
            html = BeautifulSoup(resp.text, 'lxml')
            ip_list = html.select_one("#ip_list")
            trs = ip_list.select("tr")[:80]
            for i, tr in enumerate(trs):
                if i > 0:
                    tds = tr.select("td")
                    proxies.append("%s://%s:%s" % (tds[5].text.lower(), tds[1].text, tds[2].text))
            time.sleep(12)
    except:
        pass
    print u"爬取%s代理IP" % len(proxies)
    return proxies


def ip2proxy(ip):
    proto = "https" if ip.startswith("https") else "http"
    proxy = {proto: ip}
    return proxy


def protoarticle(ip, article):
    proto = "https" if ip.startswith("https") else "http"
    article = article.replace("http", proto)
    return article


def is_useful(ip):
    try:
        resp = requests.get("http://ip.chinaz.com/", headers=req_headers, timeout=TIME_OUT, proxies=ip2proxy(ip))
        html = BeautifulSoup(resp.text, 'lxml')
        print(html.select_one(".getlist"))
        print u"%s有效" % ip
        return True
    except:
        print u"%s无效" % ip
        return False


def get_useful_ips(ips, batch=10):
    all_jobs = [gevent.spawn(is_useful, ip) for ip in ips]

    sub_jobs = [all_jobs[i:i + batch] for i in range(0, len(all_jobs), batch)]
    usefuls = []
    for jobs in sub_jobs:
        gevent.joinall(jobs, timeout=5)
        usefuls += [job.value for job in jobs]

    useful_ips = [ips[i] for i, useful in enumerate(usefuls) if useful]
    return useful_ips


if __name__ == '__main__':
    # blog = "http://blog.csdn.net/east196"
    # print get_article_ids(blog)
    article_link = "https://blog.csdn.net/east196/article/details/79632539"
    while True:
        try:
            requests.get(article_link, timeout=TIME_OUT, headers=req_headers)
            print article_link
        except:
            print "error"

        s = random.randint(12, 60)
        print "sleep: {}s".format(s)
        time.sleep(s)
