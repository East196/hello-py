#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8
import ConfigParser
import random

from selenium import webdriver
import time

config = ConfigParser.ConfigParser()
config.read("csdn.conf")

u = config.get("east", "username")
p = config.get("east", "password")
# print u,p


browser = webdriver.Firefox()
browser.maximize_window()
browser.get("https://passport.csdn.net/account/login")
time.sleep(10)
username = browser.find_element_by_id("username")
username.send_keys(u)
time.sleep(2)
password = browser.find_element_by_id("password")
password.send_keys(p)
time.sleep(2)
submit = browser.find_element_by_css_selector("input.logging")
submit.click()
time.sleep(2)


def view(browser, blog):
    browser.maximize_window()
    browser.get(blog)
    time.sleep(5)

    urls = []
    html_as = browser.find_elements_by_css_selector("li.blog-unit a")
    for html_a in html_as:
        urls.append(html_a.get_attribute("href"))

    print urls

    for url in urls:
        try:
            if url.decode("utf-8").startswith("http"):
                browser.get(url)
                time.sleep(random.randint(1, 3))
        except Exception, e:
            print e


blogs = ["http://blog.csdn.net/q809198545", "http://blog.csdn.net/east196"]

for blog in blogs:
    view(browser, blog)
browser.close()
