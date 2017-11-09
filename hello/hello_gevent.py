#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gevent import monkey

monkey.patch_all()

import urllib2
from gevent.pool import Pool


def download(url):
    """
    查看url对应内容
    :param url: http url
    :return: response doc
    """
    return urllib2.urlopen(url).read()


if __name__ == '__main__':
    urls = ['http://httpbin.org/get'] * 100
    pool = Pool(20)
    results = pool.map(download, urls)
    print len(results)
    print results
