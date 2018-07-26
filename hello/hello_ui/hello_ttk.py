#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter.ttk
import tkinter

root = tkinter.Tk()

tkinter.ttk.Style().configure("TButton", padding=6, relief="flat",
                      background="#ccc")

count = 0


def show_hello():
    tkinter.ttk.Label(text="Hello World!!").pack()


btn = tkinter.ttk.Button(text="Sample", command=show_hello)
btn.pack()

root.mainloop()
