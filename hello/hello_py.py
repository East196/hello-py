#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cPickle

items = [1, 2, 3, "223", 5.0]
cPickle.dump(items, open("a.p", "w"))

print cPickle.load(open("a.p"))

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    # The only supported default encodings in Python are:

    #  Python 2.x: ASCII
    #  Python 3.x: UTF-8
    # So no need to sys.setdefaultencoding('utf-8')
    pass  # py3

import traceback

try:
    raise IOError("io error!!!")  # 抛出第一个异常，被except捕获了
except IOError, io_error:
    traceback.print_exc()  # 打印异常栈，第一个异常的栈
    print sys.exc_info()  # 打印异常信息
    print io_error  # 打印异常消息
    pass  # 异常处理完毕，系统正常继续
finally:
    print "1 print always..."

try:
    raise IOError("io error!!!")  # 抛出第一个异常，被except捕获了
except IOError, io_error:
    raise IOError("raise io error!!!")  # 抛出第二个异常，会被系统捕获，系统退出
finally:
    print "2 print always..."  # 但是还是会运行这里
