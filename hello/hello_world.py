#! /usr/bin/env python 
#coding=utf-8 

print None
i=None
print i is None
# from addict import Dict
# body = Dict()
# body.query.filtered.query.match.description = 'addictive'
# body.query.filtered.filter.term.created_by = 'Mats'
# print body
#
# from faker import Faker
# fake = Faker(locale='Zh_CN')
# print fake.name()
# print fake.address()

import requests
r = requests.get('http://www.baidu.com')
print r.text


if u"离线" in u"离线啊啊" :
    print "ok"
