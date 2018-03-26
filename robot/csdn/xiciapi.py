#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

text = requests.get("http://api.xicidaili.com/free2016.txt").text

print(text)