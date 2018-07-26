#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the library
from appJar import gui


# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        usr = app.getEntry("用户名")
        pwd = app.getEntry("密码")
        print(("User:", usr, "Pass:", pwd))


# create a GUI variable called app
app = gui("Login Window", "400x200")
app.setBg("orange")
app.setFont(18, "微软雅黑")

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to appJar")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

app.addLabelEntry("用户名")
app.addLabelSecretEntry("密码")

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)

app.setFocus("用户名")

# start the GUI
app.go()
