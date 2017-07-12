#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from prettytable import PrettyTable

pt = PrettyTable(field_names=["name", "sex"])
persons = [("tung", "male"), ("snow", "female")]# 非常适合sqlite数据集
[pt.add_row(kv) for kv in persons]
print pt

# TODO 做json处理
persons = [{"name": "tung", "sex": "male"}, {"name": "snow", "sex": "female"}]
print json.dumps(persons,indent=2)

field_names=persons[1].keys()
pt = PrettyTable(field_names=field_names)
[pt.add_row(person.values()) for person in persons]
print pt
