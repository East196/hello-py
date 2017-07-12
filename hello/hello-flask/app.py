#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from flask import Flask, jsonify
from flask import json
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def json(self):
        return to_json(self, self.__class__)


@app.route("/")
def hello():
    app.logger.debug("hello run")
    app.logger.info("hello run")
    app.logger.warn("hello run")
    return render_template('index.html',aaa=User.query.first().username)


@app.route("/log")
def log():
    logging.debug("log run")
    logging.info("log run")
    logging.warn("log run")
    return render_template('index.html')


@app.route("/user")
def user():
    print User.query.all()
    print User.query.first()
    return User.query.first().json


@app.route("/dsuser")
def dsuser():
    import dataset

    db = dataset.connect('sqlite:///:memory:')

    table = db['sometable']
    table.insert(dict(name='John Doe', age=37))
    table.insert(dict(name='Jane Doe', age=34, gender='female'))

    john = table.find_one(name='John Doe')
    return jsonify(john)


if __name__ == "__main__":
    db.create_all()
    user = User("tung", "tung@visn")
    db.session.add(user)
    db.session.commit()
    # the toolbar is only enabled in debug mode:
    app.debug = True

    # set a 'SECRET_KEY' to enable the Flask session cookies
    app.config['SECRET_KEY'] = '<replace with a secret key>'

    toolbar = DebugToolbarExtension(app)
    app.run()
