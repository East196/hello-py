# -*- coding: utf-8 -*-
import ConfigParser
import json
import urllib2
from bs4 import BeautifulSoup


def del_id(record):
    del record['_id']
    return record


def test_del_id():
    record = {"_id": 123, "name": "east196"}
    assert {"name": "east196"} == del_id(record)


def get_soup(page):
    response = urllib2.urlopen(page)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    return soup


def get_json_object(url):
    response = urllib2.urlopen(url)
    json_object = json.loads(response.read())
    return json_object
