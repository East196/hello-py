#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

if __name__ == '__main__':
    r = requests.post('http://127.0.0.1:5000/login',
                      data=json.dumps({'email': 'matt@nobien.net', 'password': 'password'}),
                      headers={'content-type': 'application/json'})
    lr = r.json()
    token = lr['response']['user']['authentication_token']
    print lr
    print type(lr)
    print token
    r = requests.get('http://127.0.0.1:5000/',
                     headers={'Authentication-Token': token})
    print r.text
