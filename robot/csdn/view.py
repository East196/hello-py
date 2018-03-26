#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8
import random

from selenium import webdriver
import time

from fastlist import get_article_ids


def view(browser, blog):
    browser.maximize_window()
    browser.get(blog)
    time.sleep(5)

    articles = ['{}/article/list/{}'.format(blog, article_id) for article_id in get_article_ids(blog)]

    for html in articles:
        try:
            browser.get(html)
            s = random.randint(3, 5)
            print(s)
            time.sleep(s)
        except Exception, e:
            print e


blogs = ["https://blog.csdn.net/q809198545", "http://blog.csdn.net/east196"]

browser = webdriver.PhantomJS()
while True:

    for blog in blogs:
        view(browser, blog)

browser.close()
