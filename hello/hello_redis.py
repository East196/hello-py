#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

print redis.__file__
# 连接，可选不同数据库
redis = redis.Redis(host='10.40.100.16', port=6379, db=0)

info = redis.info()
print info
keys = redis.keys("*")
print keys

keys = redis.hkeys("keys")
print keys
print len(keys)

key__value = redis.hget("key", 'hashkey')
print key__value
