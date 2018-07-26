#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from .tool import *


def test_search_path():
    yo = """
    a: 
      b: 
        c: 焦飞
    d: 太上化龙决
    e: 解
    """

    o = yaml.load(yo)
    assert "e" == search_path(o, "解")
    assert "a.b.c" == search_path(o, "焦飞")


def test_leaf_path():
    yo = """
    a: 
      b: 
        c: 焦飞
    d: 太上化龙决
    e: 解
    """

    o = yaml.load(yo)
    for k, v in leaf_path(o):
        print(k, v)
