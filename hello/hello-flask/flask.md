
# Flask使用
pip install flask
## 基础模板 -> Atom
```
```
## 公网可用
host='0.0.0.0'
## 日志
```pythonstub
app.logger.debug("loggggggggggg")
```
## 输入解析：path/args/form/json


## 输出解析：render_template、jsonify,make_response


## flask-restful使用
> pip install flask-restful

Todo & TodoList


## pymongo使用
> pip install pymongo

```python
from bson import json_util as jsonb
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://10.40.100.16:27017/")
db = client.get_database("test")
```
## pymysql使用
纯python的mysql driver，无需安装其他驱动，只需：
`
pymysql.install_as_MySQLdb()
`
## dataset使用
```python
import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['sometable']
table.insert(dict(name='John Doe', age=37))
table.insert(dict(name='Jane Doe', age=34, gender='female'))

john = table.find_one(name='John Doe')
```

## HTTPie使用
> pip install httpie

```
http GET http://httpbin.org/get
http -f PUT httpbin.org/put data=1

http GET 127.0.0.1:8889/datadict
http -f PUT 127.0.0.1:8889/1 data=1
```

> httpbin 也是 flask 写的，可以本地安装反应速度更快

## or 使用专为人类编写的requests
> pip install requests

[requests](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)



```text
pip install httpbin
gunicorn httpbin:app
```

## flask-jwt
二话不说跑起来：
```python
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()
```



```
http  -j -v POST :5000/auth username=user1 password=abcxyz
```

```
POST /auth HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 43
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.9

{
    "password": "abcxyz",
    "username": "user1"
}

HTTP/1.0 200 OK
Content-Length: 193
Content-Type: application/json
Date: Fri, 26 May 2017 02:46:26 GMT
Server: Werkzeug/0.11.15 Python/2.7.13

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDk1NzY2Nzg2LCJuYmYiOjE0OTU3NjY3ODYsImV4cCI6MTQ5NTc2NzA4Nn0.4ZiutuoN39vLoJ6gt-YdWWmrYhlwMNz0LQ6PzLZRfo4"
}

```



```
http :5000/protected "Authorization:JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDk1NzY2Nzg2LCJuYmYiOjE0OTU3NjY3ODYsImV4cCI6MTQ5NTc2NzA4Nn0.4ZiutuoN39vLoJ6gt-YdWWmrYhlwMNz0LQ6PzLZRfo4"
```

```
HTTP/1.0 200 OK
Content-Length: 12
Content-Type: text/html; charset=utf-8
Date: Fri, 26 May 2017 02:47:13 GMT
Server: Werkzeug/0.11.15 Python/2.7.13

User(id='1')
```


## 使用token验证
http://mandarvaze.github.io/2015/01/token-auth-with-flask-security.html
key:
- 取消csrf便于直接http请求
```pythonstub
app.config['WTF_CSRF_ENABLED'] = False
```

- 使用@auth_token_required代替@login_required

## 使用https保护用户名密码
#### 默认证书
app.run(debug=True, port=8100, ssl_context='adhoc')

## flask debug toolbar
显示的条件是返回页面要有<body></body>
logging需要使用python原生logging

