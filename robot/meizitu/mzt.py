#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import time

import requests
from bs4 import BeautifulSoup


class mzitu():
    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_url(self, url):
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a[1:]:
            title = a.get_text()
            print(('开始保存：', title))  ##加点提示不然太枯燥了
            path = title.replace("?", '_').replace(":", '_')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            time.sleep(random.randrange(50, 200) / 4000.0)
            self.mkdir(path)  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            href = a['href']
            print(href)
            self.html(href)  ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！

    def html(self, href):  ##这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)
        self.headers['referer'] = href
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        print(max_span, len(os.listdir(os.path.curdir)))
        if int(max_span) > len(os.listdir(os.path.curdir)):
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                time.sleep(random.randrange(50, 200) / 4000.0)
                self.img(page_url)  ##调用img函数

    def img(self, page_url):  ##这个函数处理图片页面地址获得图片的实际地址
        print(page_url)
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):  ##这个函数保存图片
        name = img_url[-9:-4] + '.jpg'
        if name in os.listdir(os.path.curdir): return
        img = self.request(img_url)
        f = open(name, 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        base = "E:/backup/Downloads/mzitu"
        isExists = os.path.exists(os.path.join(base, path))
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(os.path.join(base, path))
            os.chdir(os.path.join(base, path))  ##切换到目录
            return True
        else:
            print('名字叫做', path, '的文件夹已经存在了！')
            os.chdir(os.path.join(base, path))  ##切换到目录
            return False

    def request(self, url):  ##这个函数获取网页的response 然后返回
        content = requests.get(url, headers=self.headers)
        return content


if __name__ == '__main__':
    def crawl():
        try:
            Mzitu = mzitu()  ##实例化
            Mzitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
        except Exception as e:
            print(e)
            print("sleep hahaha and restart")
            # TODO 根据异常状态调整3处的sleep
            # TODO 修正只要异常就重爬的不合理行为
            time.sleep(random.randrange(50, 500) / 100.0)
            crawl()
    crawl()
    # 颜：李凌子 艾小青 杉原杏璃
    # 身：杨晨晨