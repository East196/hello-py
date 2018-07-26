#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itchat


@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg)

    itchat.send('greeting, filehelper!', "filehelper")
    name = itchat.search_friends(name='谁啊')[0]
    print(name)
    name.send("good")


itchat.auto_login(hotReload=True)
itchat.run()

## and 基于itchat的wxpy
