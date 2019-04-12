#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import smtplib
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read("d:/influence.conf")
username = config.get('qqmail', 'username')
password = config.get('qqmail', 'password')

to = username
title = "测试严思思是否在线"
content = "这个是测试内容，ok？"

def send_mail(to,title,content):
    msg = MIMEText(content)
    msg["Subject"] = title
    msg["From"] = username
    msg["To"] = to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(username, password)
        s.sendmail(username, to, msg.as_string())
        s.quit()
        print("Success!")
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)


if __name__ == "__main__":
    send_mail(to,title,content)