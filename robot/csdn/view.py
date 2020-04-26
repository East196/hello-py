#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8
import random

from selenium import webdriver
import time

from robot.csdn.fastlist import get_article_ids


def view(browser, blog):
    browser.maximize_window()
    browser.get(blog)
    print("ok")
    time.sleep(5)

    for html in articles[29:]:
        try:
            browser.get(html)
            s = random.randint(3, 5)
            print((s, html))
            time.sleep(s)
        except Exception as  e:
            print(e)


blog = "http://blog.csdn.net/east196"  # "https://blog.csdn.net/q809198545",
articles = ['{}/article/list/{}'.format(blog, article_id) for article_id in get_article_ids(blog)]
print(articles)
options = webdriver.FirefoxOptions()
# options.headless = True
browser = webdriver.Firefox(options=options)
while True:
    view(browser, blog)

browser.close()
