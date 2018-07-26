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

msg = MIMEText("Test")
msg["Subject"] = "don't panic"
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
