#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinydb import TinyDB, Query

# init db
db = TinyDB('gene.json')
# init table
models = db.table('model')
Model= Query()

from appJar import gui

# init gui
app = gui()

app.startLabelFrame("模型")


def edit(btn):
    print("edit: %s" % btn, app.getListBox(btn))
    if not app.getListBox(btn): return
    name = app.getListBox(btn)[0]
    model = models.get(Model.name == name)
    print(model)
    if model:
        
        app.setEntry("名称", model["name"])
        
        
        
        app.clearTextArea("内容")
        app.setTextArea("内容", model["content"])
        
        


app.addListBox("模型列表", [model["name"] for model in models.all()])
app.setListBoxSubmitFunction("模型列表", edit)


app.addLabelEntry("名称")



app.addScrolledTextArea("内容")




def save(btn):
    print("save: %s" % btn)
    
    name = app.getEntry("名称")
    
    
    
    content = app.getTextArea("内容")
    
    


    model = {
        "name" : name,
        "content" : content
        }


    print(model)
    models.upsert(model, Model.name == model["name"])
    app.updateListBox("模型列表", [model["name"] for model in models.all()])
    print("show all models:")
    for model in models.all():
        print(model)


app.addButton("保存", save)


def clear(btn):
    print("clear: %s" % btn)
    
    app.setEntry("名称", "")
    
    
    
    app.clearTextArea("内容")
    
    

app.addButton("清除", clear)


def delete(btn):
    print("delete: %s" % btn)
    model = models.get(Model.name == app.getEntry("名称"))
    if model:
        models.remove(doc_ids=[model.doc_id])
        app.updateListBox("模型列表", [model["name"] for model in models.all()])


app.addButton("删除", delete)

app.stopLabelFrame()
app.go()


