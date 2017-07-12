# coding=utf-8
from selenium import webdriver
import time
import random

browser = webdriver.Chrome()
# browser.maximize_window()
browser.get("http://www.yxkfw.com/forum.php")
time.sleep(2)
username = browser.find_element_by_id("ls_username")
username.send_keys("user")
password = browser.find_element_by_id("ls_password")
password.send_keys("pass")
submit = browser.find_element_by_css_selector("button.pn.vm")
submit.click()
time.sleep(2)

htmls = []
page_nums = range(2, 6)  # 精品，一共13页
for page_num in page_nums:
    page = "http://www.yxkfw.com/forum-48-%s.html" % page_num
    browser.get(page)
    time.sleep(random.randint(2, 5))
    html_as = browser.find_elements_by_css_selector("th.common a.s.xst")
    for html_a in html_as:
        htmls.append(html_a.get_attribute("href"))

print len(htmls), htmls
words = [u'学习一下，多谢楼主分享！！！', u'看起来很不错的样子，GOOD！', u'看来我要努力赚钱了！',
         u'楼主真是个大好人，谢谢了！', u'我想下载这个游戏……', u'好，这个太好了，下载看看学习哈',
         u'这个看起来非常完整啊，顶一个！', u'我的征途是星辰大海……', u'升职CEO，迎娶白富美就靠它了！！！',
         u'谢谢，好东东就应该是分享，哈哈哈', u'很不错,非常值得学习，楼主威武！！！', u'感谢分享！！！你的分享是我们前进的方向^']

for html in htmls:
    print time.time(), htmls.index(html), html
    browser.get(html)
    time.sleep(5)
    try:
        alink = browser.find_element_by_css_selector("#online_link")
        alink.click()
        time.sleep(3)
        browser.get(html)
        time.sleep(5)
        textarea = browser.find_element_by_css_selector("#fastpostmessage")
        textarea.send_keys(words[random.randint(0, len(words) - 1)])
        submit = browser.find_element_by_css_selector("#fastpostsubmit")
        submit.click()
    except:
        username = browser.find_element_by_id("ls_username")
        username.send_keys("username")
        password = browser.find_element_by_id("ls_password")
        password.send_keys("password")
        submit = browser.find_element_by_css_selector("button.pn.vm")
        submit.click()
        time.sleep(2)
        textarea = browser.find_element_by_css_selector("#fastpostmessage")
        textarea.send_keys(words[random.randint(0, 4)])
        submit = browser.find_element_by_css_selector("#fastpostsubmit")
        submit.click()
    time.sleep(random.randint(700, 750))
browser.close()
