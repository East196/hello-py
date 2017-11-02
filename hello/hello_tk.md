
# 一些小例子
[定时关机](http://blog.csdn.net/cch1024/article/details/54603716)

# treeview 类似 table + tree
其实还是很强大的
[官方文档的TreeView](https://docs.python.org/2.7/library/ttk.html#treeview)
[tkdocs的TreeView](http://www.tkdocs.com/tutorial/tree.html)

# text 类似 web的text area
1.设置python Tkinter Text控件文本的方法
   text.insert(index,string)  index = x.y的形式,x表示行，y表示列
   向第一行插入数据,text.insert(1.0,'hello world')
2.清空python Tkinter Text控件文本的方法
  #思路：从第一行清除到最后一行
             text.delete(1.0,Tkinter.END)

# [登录](http://blog.csdn.net/bnanoou/article/details/38515083)

登陆可以用这个思路,用一个管理类去destroy login页面，开启主页面：
```python
from Tkinter import *

class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Value").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()

        self.top.destroy()


root = Tk()
Button(root, text="Hello!").pack()
root.update()

d = MyDialog(root)

root.wait_window(d.top)
```