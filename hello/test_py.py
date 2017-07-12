#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_isdigit():
    assert True == "1234".isdigit()
    assert False == "1234a".isdigit()
