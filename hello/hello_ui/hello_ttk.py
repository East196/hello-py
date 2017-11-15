#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ttk
import Tkinter

root = Tkinter.Tk()

ttk.Style().configure("TButton", padding=6, relief="flat",
                      background="#ccc")

count = 0


def show_hello():
    ttk.Label(text="Hello World!!").pack()


btn = ttk.Button(text="Sample", command=show_hello)
btn.pack()

root.mainloop()
