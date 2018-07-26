#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinydb import TinyDB, Query

# init db
db = TinyDB('gene.json')
# init table
tpls = db.table('tpl')
Tpl= Query()

from appJar import gui

# init gui
app = gui()

app.startLabelFrame("模版")


def edit(btn):
    print("edit: %s" % btn, app.getListBox(btn))
    if not app.getListBox(btn): return
    name = app.getListBox(btn)[0]
    tpl = tpls.get(Tpl.name == name)
    print(tpl)
    if tpl:
        
        app.setEntry("名称", tpl["name"])
        
        
        
        app.clearTextArea("内容")
        app.setTextArea("内容", tpl["content"])
        
        


app.addListBox("模版列表", [tpl["name"] for tpl in tpls.all()])
app.setListBoxSubmitFunction("模版列表", edit)


app.addLabelEntry("名称")



app.addScrolledTextArea("内容")




def save(btn):
    print("save: %s" % btn)
    
    name = app.getEntry("名称")
    
    
    
    content = app.getTextArea("内容")
    
    


    tpl = {
        "name" : name,
        "content" : content
        }


    print(tpl)
    tpls.upsert(tpl, Tpl.name == tpl["name"])
    app.updateListBox("模版列表", [tpl["name"] for tpl in tpls.all()])
    print("show all tpls:")
    for tpl in tpls.all():
        print(tpl)


app.addButton("保存", save)


def clear(btn):
    print("clear: %s" % btn)
    
    app.setEntry("名称", "")
    
    
    
    app.clearTextArea("内容")
    
    

app.addButton("清除", clear)


def delete(btn):
    print("delete: %s" % btn)
    tpl = tpls.get(Tpl.name == app.getEntry("名称"))
    if tpl:
        tpls.remove(doc_ids=[tpl.doc_id])
        app.updateListBox("模版列表", [tpl["name"] for tpl in tpls.all()])


app.addButton("删除", delete)

app.stopLabelFrame()
app.go()


