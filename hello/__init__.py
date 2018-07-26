#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import datetime
import logging.config


def log(func):
    def wrapper(*args, **kw):
        print('call %s() in %s :' % (func.__name__, datetime.datetime.now()))
        result = func(*args, **kw)
        time.sleep(0.1)
        print('called %s() in %s :' % (func.__name__, datetime.datetime.now()))
        return result

    return wrapper


@log
def now():
    print('2013-12-25')

now()

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("hello")
logger.debug("started logging hello.")
