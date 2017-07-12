#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install elasticsearch elasticsearch-dsl

from elasticsearch import Elasticsearch
es = Elasticsearch([
    'http://admin:adminadmin@hadoop-16:9200/',
    'http://admin:adminadmin@hadoop-17:9200/',
    'http://admin:adminadmin@hadoop-18:9200/'
])

res = es.search(index="visn_sub_info_v2", body={
                "query": {"match_all": {}}, "size": "10"})
for hit in res['hits']['hits']:
    print hit["_source"]

res = es.search(index="visn_line_info", body={
                "query": {"match_all": {}}, "size": "10"})
for hit in res['hits']['hits']:
    print hit["_source"]

res = es.search(index="visn_mac_areas", body={
                "query": {"match_all": {}}, "size": "10"})
for hit in res['hits']['hits']:
    print hit["_source"]
