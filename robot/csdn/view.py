#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8
import random

from selenium import webdriver
import time


def view(browser, blog):
    browser.maximize_window()
    browser.get(blog)
    time.sleep(5)

    urls = []
    html_as = browser.find_elements_by_css_selector("li.blog-unit a")
    for html_a in html_as:
        urls.append(html_a.get_attribute("href"))

    print urls

    for html in urls:
        try:
            browser.get(html)
            time.sleep(random.randint(3, 5))
        except Exception, e:
            print e


browsers = [webdriver.Firefox(), webdriver.PhantomJS()]
# browsers = [webdriver.Ie()]
blogs = ["https://blog.csdn.net/q809198545", "http://blog.csdn.net/east196"]

for browser in browsers:
    for blog in blogs:
        view(browser, blog)
    browser.close()
