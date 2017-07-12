#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from faker import Faker
from flask import Flask, jsonify

app = Flask(__name__)

fake = Faker("zh_CN")


@app.route("/name")
def name():
    return fake.name()


@app.route("/username")
def username():
    return fake.user_name()


@app.route("/password")
def password():
    return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)


@app.route("/url")
def url():
    return fake.url()


@app.route("/email")
def email():
    return fake.email()


@app.route("/phone")
def phone():
    return fake.phone_number()


@app.route("/address")
def address():
    return fake.address()


@app.route("/profile")
def profile():
    profile = fake.profile(fields=None, sex=None)
    (lat, lon) = profile.pop("current_location")
    profile['current_location'] = {
        "lat": lat.__float__(),
        "lon": lon.__float__()
    }
    return jsonify(profile)


@app.route("/sentence")
def sentence():
    return fake.sentence()


@app.route("/mac")
def mac():
    return fake.mac_address()


@app.route("/ip")
def ip():
    return fake.ipv4()


@app.route("/_int/<int:min>-<int:max>")
def _int(min=0, max=9999):
    return str(random.randint(min, max))


if __name__ == "__main__":
    fake.pyint()
    app.run(debug=True)
