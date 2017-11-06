#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *

if __name__ == '__main__':

    # 官方有ScrolledText的实现！ from ScrolledText import ScrolledText
    # 官方没有Listbox的Scrollbar实现！
    master = Tk()

    scrollbar = Scrollbar(master)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(master, yscrollcommand=scrollbar.set)
    for i in range(1000):
        listbox.insert(END, str(i))
    listbox.pack(side=LEFT, fill=BOTH)

    scrollbar.config(command=listbox.yview)

    mainloop()