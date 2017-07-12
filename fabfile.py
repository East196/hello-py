#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import local


def install():
    local('pip install flask')  # flask web开发库
    local('pip install arrow')  # arrow python时间库
