#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import json

if __name__ == '__main__':
    with open("jianke.json") as fp:
        json_array = json.load(fp)
    with open("jianke.md", "w") as fp:
        for d in json_array:
            print d['title']
            fp.write(d['title'] + os.linesep)
