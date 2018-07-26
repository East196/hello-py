#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install pyyaml flask tinydb appJar

import os

import yaml
from jinja2 import Template
from tinydb import TinyDB, Query

# init db
db = TinyDB('gene.json')
# init table
configs = db.table('config')
Config = Query()

models = db.table('model')
Model = Query()

tpls = db.table('tpl')
Tpl = Query()

from appJar import gui

# init gui
app = gui()

app.startLabelFrame("models")
app.setSticky("nwe")


def model_change(f):
    print((f, app.getOptionBox("model")))
    model_name = app.getOptionBox("model")
    model = models.get(Model.name == model_name)
    print(model)
    if model:
        app.setEntry("model_name", model["name"])
        app.clearTextArea("model_content")
        app.setTextArea("model_content", model["content"])


app.addOptionBox("model", [])
app.setOptionBoxChangeFunction("model", model_change)
app.addLabelEntry("model_name")
app.addScrolledTextArea("model_content")
app.setTextAreaHeight("model_content", 30)
model_names = [model["name"] for model in models.all()]
if model_names:
    print("change model_names")
    app.changeOptionBox("model", model_names, len(model_names) - 1, True)
    app.setOptionBox("model", len(model_names) - 1)

app.stopLabelFrame()

app.startLabelFrame("tpls", 0, 1)
app.setSticky("nwe")


def tpl_change(f):
    print((f, app.getOptionBox("tpl")))
    tpl_name = app.getOptionBox("tpl")
    tpl = tpls.get(Model.name == tpl_name)
    print(tpl)
    if tpl:
        app.setEntry("tpl_name", tpl["name"])
        app.clearTextArea("tpl_content")
        app.setTextArea("tpl_content", tpl["content"])


app.addOptionBox("tpl", [])
app.setOptionBoxChangeFunction("tpl", tpl_change)
app.addLabelEntry("tpl_name")
app.addScrolledTextArea("tpl_content")
app.setTextAreaHeight("tpl_content", 30)
tpl_names = [tpl["name"] for tpl in tpls.all()]
if tpl_names:
    print("change tpl_names")
    app.changeOptionBox("tpl", tpl_names, len(tpl_names) - 1, True)
    app.setOptionBox("tpl", len(tpl_names) - 1)

app.stopLabelFrame()

app.addScrolledTextArea("result", 0, 2)
app.setTextAreaHeight("result", 30)
app.addLabelEntry("路径", 1, 2)

if not app.getEntry("路径"):
    config = configs.get(Config.name == "path")
    if config:
        path = config["value"]
    else:
        path = app.exe_path
        configs.insert({"name": "path", "value": path})
    app.setEntry("路径", path)

app.addLabelEntry("数据库", 2, 2)

if not app.getEntry("数据库"):
    config = configs.get(Config.name == "database")
    if config:
        database = config["value"]
    else:
        database = "database"
        configs.insert({"name": "database", "value": database})
    app.setEntry("数据库", database)


def gene_it(f):
    print(f)
    model_name = app.getEntry("model_name")
    model_content = app.getTextArea("model_content")
    models.upsert({"name": model_name, "content": model_content}, Model.name == model_name)
    model = yaml.load(model_content)
    print(model)

    tpl_name = app.getEntry("tpl_name")
    tpl_content = app.getTextArea("tpl_content")
    tpls.upsert({"name": tpl_name, "content": tpl_content}, Tpl.name == tpl_name)
    print(tpl_content)

    model.update({"database": app.getEntry("数据库")})
    result = Template(tpl_content).render(**model)
    print(result)
    app.clearTextArea("result")
    app.setTextArea("result", result)
    path = app.getEntry("路径")
    if not os.path.exists(path):
        os.mkdir(path)
    configs.update({"value": path}, Config.name == "path")
    database = app.getEntry("数据库")
    configs.update({"value": database}, Config.name == "database")
    with open("%s/%s.py" % (path, model["name"]), "w", encoding="utf-8") as fp:
        fp.write(result)


# TODO 考虑装插件直接使用 yaml和 jinja2 文件
app.enableEnter(gene_it)

app.go()
