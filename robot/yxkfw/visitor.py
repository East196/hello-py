# coding=utf-8
from selenium import webdriver
import time
import random

browser = webdriver.Chrome()
browser.get("http://www.yxkfw.com/forum.php")
time.sleep(2)
username = browser.find_element_by_id("ls_username")
username.send_keys("user")
password = browser.find_element_by_id("ls_password")
password.send_keys("pass")
submit = browser.find_element_by_css_selector("button.pn.vm")
submit.click()
time.sleep(2)

articles = []
page_nums = list(range(3, 5))
for page_num in page_nums:
    page = "http://www.yxkfw.com/forum-41-%s.html" % page_num
    browser.get(page)
    time.sleep(random.randint(5, 10))
    acks = browser.find_elements_by_css_selector("tbody tr td.by cite a")
    for ack in acks[1::2]:
        acker = ack.get_attribute("href")
        if acker != "http://www.yxkfw.com/space-uid-1.html":
            articles.append(acker)

articles = list(set(articles))
print(len(articles), articles)

for article in articles:
    index = articles.index(article)
    print(index, article)
    try:
        browser.get(article)
        time.sleep(2)
        msg = browser.find_element_by_css_selector("#profile_content ul li.ul_msg a").get_attribute("href")
        poke = browser.find_element_by_css_selector("#profile_content ul li.ul_poke a").get_attribute("href")
        time.sleep(2)

        browser.get(msg)
        textarea = browser.find_element_by_css_selector("#comment_message")
        textarea.send_keys("[em:4:]")
        time.sleep(2)
        submit = browser.find_element_by_css_selector("#commentsubmit_btn")
        submit.click()
        time.sleep(5)

        browser.get(poke)
        submit = browser.find_element_by_css_selector("#pokesubmit_btn")
        submit.click()
        time.sleep(5)
    except:
        pass
    time.sleep(random.randint(60, 80))
browser.close()
