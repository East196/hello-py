#!/usr/bin/env python
# -*- coding: utf-8 -*
import ConfigParser
import random

import requests
import time
from bs4 import BeautifulSoup

from fastlist import get_article_ids


def login():
    config = ConfigParser.ConfigParser()
    config.read("csdn.conf")

    u = config.get("east", "username")
    p = config.get("east", "password")

    login_url = "https://passport.csdn.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    session = requests.session()
    session.headers.update(headers)
    r = session.get(login_url, verify=False)
    page = BeautifulSoup(r.text, "lxml")
    authentication = {
        "username": u,
        "password": p,
        "lt": page.select("[name=lt]")[0]["value"],
        "execution": page.select("[name=execution]")[0]["value"],
        "_eventId": "submit",
    }
    r = session.post(login_url, authentication)
    return session


def show_my_msg(session):
    """
    查看自己的信息
    :param session: 
    :return: 
    """
    msg_url = "http://msg.csdn.net/"
    r2 = session.get(msg_url)
    print(r2.text)


if __name__ == '__main__':

    session = login()
    show_my_msg(session)

    blog = "https://blog.csdn.net/junkie0901"

    comments = ['学习一下，多谢楼主分享！！！', '看起来很不错的样子，GOOD！', '谢谢分享，大好人啊 ~~~',
                '楼主真是个大好人，谢谢了！', '谢谢博主的分享 ~~ 手动点赞', '好，这个太好了，下载看看学习哈',
                '这个看起来非常完整啊，顶一个！', '我的征途是星辰大海……', '也在做相关的东西。谢谢博主了。',
                '谢谢，好东东就应该是分享，哈哈哈', '很不错,非常值得学习，楼主威武！！！',
                '感谢分享！！！你的分享是我们前进的方向^', "刚入门没多久, 求带路！",
                "最近这个好像很火，纠结要不要入门，博主求博主指引~~"]

    article_ids = get_article_ids(blog)
    for article_id in article_ids:
        comment = random.choice(comments)
        article_comment_url = blog + "/phoenix/comment/submit?id=" + article_id
        r2 = session.post(article_comment_url, {
            "content": comment,
        })
        print(article_comment_url)
        print(comment)
        print(r2.json())
        seconds = random.randint(60, 180)
        print("sleep {}s".format(seconds))
        time.sleep(seconds)
