#coding=utf-8
from selenium import webdriver
import time
import random
 
browser = webdriver.Firefox()
browser.maximize_window()
browser.get("https://passport.csdn.net/account/login")
time.sleep(20)
username = browser.find_element_by_id("username") 
username.send_keys("user")
time.sleep(2)
password = browser.find_element_by_id("password") 
password.send_keys("pass")
time.sleep(2)
submit = browser.find_element_by_css_selector("input.logging")
submit.click()
time.sleep(2)

htmls=[]
page_nums = range(1,14)
for page_num in page_nums:
    page="http://download.csdn.net/my/downloads/%s"%page_num
    browser.get(page)
    time.sleep(random.randint(2,5))
    html_as= browser.find_elements_by_css_selector("div.btns a.btn-comment")
    for html_a in html_as:
        htmls.append(html_a.get_attribute("href"))

print htmls
words=[u'学习一下，多谢楼主分享！！！',u'看起来很不错的样子，GOOD！',u'看来我要努力赚钱了！',
       u'楼主真是个大好人，谢谢了！',u'我想下载这个游戏……',u'好，这个太好了，下载看看学习哈',
       u'这个看起来非常完整啊，顶一个！',u'我的征途是星辰大海……',u'升职CEO，迎娶白富美就靠它了！！！',
       u'谢谢，好东东就应该是分享，哈哈哈',u'很不错,非常值得学习，楼主威武！！！',u'感谢分享！！！你的分享是我们前进的方向^']

for html in htmls:
    try:
        browser.get(html)
        time.sleep(20)
        star=browser.find_elements_by_css_selector("div.star-rating a")[-1]
        star.click()
        time.sleep(2)
        textarea = browser.find_element_by_css_selector("#cc_body")
        textarea.send_keys(words[random.randint(0,len(words)-1)])
        time.sleep(3)
        submit = browser.find_element_by_css_selector("div.cc_comment_form.recom_sub th input.btn.btn-primary")
        submit.click()
    except Exception,e:
        print e
    print htmls.index(html),html
    time.sleep(random.randint(62,276))
browser.close()