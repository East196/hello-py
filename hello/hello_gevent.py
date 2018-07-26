#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gevent import monkey

monkey.patch_all()

import urllib.request, urllib.error, urllib.parse
from gevent.pool import Pool


def download(url):
    """
    查看url对应内容
    :param url: http url
    :return: response doc
    """
    return urllib.request.urlopen(url).read()


class Download():
    def __init__(self):
        pass

    def do(self, url):
        return urllib.request.urlopen(url).read()


if __name__ == '__main__':
    urls = ['http://httpbin.org/get'] * 100
    pool = Pool(20)
    d = Download()

    aresults = pool.map_async(d.do, urls)
    print(aresults)

    results = pool.map(d.do, urls)
    print(len(results))
    print("===", results)
    print("========", aresults.get())
