#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import dataset

from hello import logger

db = dataset.connect('sqlite:///hello.db')
print(db.tables)
print(db['city'].columns)


class CityRender(object):
    def rend(self, citys=[]):
        body = " | ".join([item.rjust(15, ' ') for item in db['city'].columns]) + os.linesep
        body += "id " + os.linesep
        return body


if __name__ == '__main__':
    # print CityRender().rend([])
    # print "3".rjust(5, ' ')
    print(db['hero'].count())
    result = db['hero'].all()
    for row in result:
        print(row)
    logger.debug(result.keys)
    dataset.freeze(result, format='json', filename='user.json')
