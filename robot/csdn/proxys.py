# !/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import random

import requests
from lxml import etree
import time

url = "https://www.kuaidaili.com/free/inha/"
req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}


# 获取最后一页的链接
def get_last_page_num(url):
    resp = requests.get(url, headers=req_headers, proxies={"http": ""})
    if resp.status_code != requests.codes.ok:
        print("resp error")
        pass

    html = etree.HTML(resp.text)
    print(html)
    last_page_num = 1

    last_page_link = html.xpath('//div[@id="listnav"]/ul/li/a[last()]/text()')
    print(last_page_link)
    if last_page_link:
        last_page_num = int(last_page_link[-1])  # 最后一页页码
        print(last_page_num)
    return last_page_num


# 构建所有页面的链接
def get_proxys():
    for i in range(1, 2):
        real_page_link = url + str(i) + "/"
        print(real_page_link)
        resp = requests.get(real_page_link, headers=req_headers)
        # print(resp.text)
        if resp.status_code != requests.codes.ok:
            print(resp.status_code)
            print("resp error")
            pass
        html = etree.HTML(resp.text)
        trs = html.xpath('//div[@id="list"]/table/tbody/tr')  # 新版博客目录
        print(len(trs))
        time.sleep(1)
        for tr in trs:
            ip = tr.xpath('td[@data-title="IP"]/text()')[0]
            port = tr.xpath('td[@data-title="PORT"]/text()')[0]
            safe = tr.xpath(u'td[@data-title="匿名度"]/text()')[0]
            type = tr.xpath(u'td[@data-title="类型"]/text()')[0]
            address = tr.xpath(u'td[@data-title="位置"]/text()')[0]
            speed = tr.xpath(u'td[@data-title="响应速度"]/text()')[0]
            last_time = tr.xpath(u'td[@data-title="最后验证时间"]/text()')[0]
            proxy = {
                "ip": ip, "port": port, "safe": safe, "type": type, "address": address, "speed": speed, "last_time": last_time
            }
            print(json.dumps(proxy, ensure_ascii=False))
            yield u"{proto}://{ip}:{port}".format(proto=type.lower(), ip=ip, port=port)


if __name__ == '__main__':
    for proxy in get_proxys():
        print(proxy)
