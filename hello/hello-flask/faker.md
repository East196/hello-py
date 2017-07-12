## faker使用
pip install faker
https://github.com/joke2k/faker/
https://faker.readthedocs.io/en/master/locales/zh_CN.html

faker -l zh_CN name

or

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from faker import Faker
fake = Faker('zh_CN')
print fake.name().encode("utf-8")

from faker import Factory
fake = Factory.create('zh_CN')
print fake.name().encode("utf-8")
```

## 应用思路
json --  entity --- faker json

##### plus realfaker
基于城市/道路/POI等信息
基于真实IP/地址/经纬度等信息