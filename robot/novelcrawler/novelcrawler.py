#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import urlparse
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
}


def get_soup(url):
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def get_json(url):
    r = requests.get(url, headers)
    return r.json()


def get_domain(url):
    split = urlparse.urlsplit(url)
    domain = "{scheme}://{netloc}".format(scheme=split.scheme, netloc=split.netloc)
    return domain


def get_chapter(url):
    soup = get_soup(url)
    chapter = soup.select_one("div.bookname > h1").get_text()
    content = soup.select_one("#content").get_text()
    return chapter, content


if __name__ == '__main__':
    url = 'http://www.xxbiquge.com/2_2327/'
    soup = get_soup(url)
    book_name = soup.select_one("head > meta[property='og:novel:book_name']").get("content")
    author = soup.select_one("head > meta[property='og:novel:author']").get("content")
    category = soup.select_one("head > meta[property='og:novel:category']").get("content")
    description = soup.select_one("head > meta[property='og:description']").get("content")
    txt_name = book_name + ".txt"
    with open(txt_name, "a") as fp:
        fp.write(book_name + os.linesep)
        fp.write(author + os.linesep)
        fp.write(category + os.linesep)
        fp.write(description + os.linesep)
    for href in soup.select("#list > dl > dd > a"):
        suburl = get_domain(url) + href.get('href')
        chapter, content = get_chapter(suburl)
        print chapter, content
        with open(txt_name, "a") as fp:
            fp.write(chapter + os.linesep)
            contents = content.split("。")
            for sub_content in contents:
                fp.write(sub_content + "。" + os.linesep)
