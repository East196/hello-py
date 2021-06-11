
# pip install pyctuator

import os
from flask import Flask
from pyctuator.pyctuator import Pyctuator

app_name = "Flask App with Pyctuator"
app = Flask(app_name)


@app.route("/")
def hello():
    return "Hello World!"


Pyctuator(
    app,
    app_name,
    app_url="http://localhost:5000",
    pyctuator_endpoint_url="http://localhost:5000/pyctuator",
    registration_url="http://localhost:9000/instances"
)

app.run()