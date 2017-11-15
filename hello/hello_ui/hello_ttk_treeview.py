#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import ttk

root = Tk()
root.geometry("800x600")

tv = ttk.Treeview(root, height=10, columns=('col1', 'col2', 'col3'))
tv.column('col1', width=100, anchor='center')
tv.column('col2', width=100, anchor='center')
tv.column('col3', width=100, anchor='center')
tv.heading('col1', text='一列')
tv.heading('col2', text='二列')
tv.heading('col3', text='三列')


def onDBClick(event):
    item = tv.selection()[0]
    print item
    print "you clicked on ", tv.item(item, "values")


for i in range(1000):
    tv.insert('', i, values=('a' + str(i), 'b' + str(i), 'c' + str(i)))

tv.bind("<Double-1>", onDBClick)
tv.pack()

# ----vertical scrollbar------------
vbar = ttk.Scrollbar(root, orient=VERTICAL, command=tv.yview)
tv.configure(yscrollcommand=vbar.set)
tv.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=0, column=1, sticky=NS)

# # ----horizontal scrollbar----------
# hbar = ttk.Scrollbar(root, orient=HORIZONTAL, command=tv.xview)
# tv.configure(xscrollcommand=hbar.set)
# hbar.grid(row=1, column=0, sticky=EW)
root.mainloop()
