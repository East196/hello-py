#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymemcache.client.base import Client

client = Client(('localhost', 11211))
client.set('some_key', 'some_value')
result = client.get('some_key')
print(result)
