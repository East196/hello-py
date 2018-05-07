#!/usr/bin/env python
# coding: utf-8
import configparser
import random
import time

from pymongo import MongoClient

from .by_id import DouYin
from .by_video_id import vedio_download

config = configparser.ConfigParser()
config.read("douyin.conf")

host = config.get("mongodb", "host")
port = config.getint("mongodb", "port")
username = config.get("mongodb", "username")
password = config.get("mongodb", "password")
db_name = config.get("mongodb", "db_name")
client = MongoClient("mongodb://%s:%s/" % (host, port))
db_auth = client.admin
db_auth.authenticate(username, password)
db = client[db_name]

#
# for post in db.author.find():
#     # pprint.pprint(post)
#     print(post["_id"])

if __name__ == '__main__':

    print(db.author.count())
    print(db.aweme.count())

    douyin = DouYin()

    # for post in db.author.find()[1:5]:
    #     print(post["_id"])
    #     uid = post["_id"]
    #     douyin.by_uid(uid)

    # awemes = db.aweme.find({'comment_count': {"$gt": 5000}, 'share_count': {"$gte": 50000}})
    awemes = db.aweme.find({'video_id': {"$exists": True}, 'comment_count': {"$gt": 5000}, 'share_count': {"$gte": 50000}})
    print(awemes.count())
    awemes = sorted(awemes, key=lambda a: a["share_count"], reverse=True)
    for aweme in awemes[1:50]:
        print(aweme)
        video_id = aweme["video_id"]
        video_name = "mp4/{video_id}.mp4".format(video_id=video_id)
        video_url = "https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}".format(video_id=video_id)
        vedio_download(video_name, video_url)
        time.sleep(random.randint((1, 6)))
