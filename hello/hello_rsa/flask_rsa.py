#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import imp

imp.reload(sys)
sys.setdefaultencoding('utf8')
import os
from flask import Flask, render_template, request, current_app
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
import urllib.parse

# 获取当前路径
curr_dir = os.path.dirname(os.path.realpath(__file__))
private_key_file = os.path.join(curr_dir, "ghost-private.pem")
public_key_file = os.path.join(curr_dir, "ghost-public.pem")

app = Flask(__name__)


def decrypt_data(inputdata, code="123456"):
    # URLDecode
    data = urllib.parse.unquote(inputdata)

    # base64decode
    data = base64.b64decode(data)

    private_key = RSA.importKey(
        open(private_key_file).read(),
        passphrase=code
    )
    # 使用 PKCS1_v1_5，不要用 PKCS1_OAEP
    # 使用 PKCS1_OAEP 的话，前端 jsencrypt.js 加密的数据解密不了
    cipher_rsa = PKCS1_v1_5.new(private_key)

    # 当解密失败，会返回 sentinel
    sentinel = None
    ret = cipher_rsa.decrypt(data, sentinel)

    return ret


@app.route('/', methods=["GET", "POST"])
def rsa():
    public_key = None
    if "GET" == request.method:
        with open(public_key_file) as file:
            public_key = file.read()
    elif "POST" == request.method:
        username = request.values.get("username")
        password = request.values.get("passwd")
        current_app.logger.debug("username:" + username + "\n" + "password:" + password)

        # decrypt
        username_ret = decrypt_data(username)
        password_ret = decrypt_data(password)
        if username_ret and password_ret:
            current_app.logger.debug(username_ret.decode() + " " + password_ret.decode())

    return render_template("rsa_view.html", public_key=public_key)


@app.route('/demo', methods=["GET", "POST"])
def js_rsa_test():
    return render_template("demo.html")


if __name__ == '__main__':
    app.run(debug=True)