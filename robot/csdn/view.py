#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8
import random

from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.maximize_window()
browser.get("http://blog.csdn.net/east196")
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

browser.close()
