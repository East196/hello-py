#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver


def github_register(users):
    browser = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
    browser.maximize_window()

    for user in users:
        print((user['username']))
        url = 'https://github.com/join?source=header-home'
        print(url)
        browser.get(url)
        time.sleep(3)
        print((browser.page_source))
        u = browser.find_element_by_id('user_login')
        print((u.text))
        u.send_keys('%s' % user['username'])
        m = browser.find_element_by_id('user_email')
        m.send_keys('%s' % user['email'])
        p = browser.find_element_by_id('user_password')
        p.send_keys('%s' % user['password'])
        submit = browser.find_element_by_id('signup_button')
        submit.click()
    browser.close()


if __name__ == '__main__':
    users = [{'username': 'xxx', 'password': 'xxx', 'email': 'xxx@qq.com'}]
    github_register(users)
