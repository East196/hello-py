
# 一些小例子
[定时关机](http://blog.csdn.net/cch1024/article/details/54603716)

# 自定义事件
To answer your specific question of "How do you invoke a TkInter event from a separate object", use the event_generate command. It allows you to inject events into the event queue of the root window. Combined with Tk's powerful virtual event mechanism it becomes a handy message passing mechanism.

For example:
```
from tkinter import *

def doFoo(*args):
    print("Hello, world")

root = Tk()
root.bind("<<Foo>>", doFoo)

# some time later, inject the "<<Foo>>" virtual event at the
# tail of the event queue
root.event_generate("<<Foo>>", when="tail")

```
Note that the event_generate call will return immediately. It's not clear if that's what you want or not. Generally speaking you don't want an event based program to block waiting for a response to a specific event because it will freeze the GUI.

# 窗口总在最前
Assuming you mean your application windows when you say "my other windows", you can use the lift() method on a Toplevel or Tk:

root.lift()
If you want the window to stay above all other windows, use:

root.attributes("-topmost", True)
Where root is your Toplevel or Tk. Don't forget the - infront of "topmost"!

To make it temporary, disable topmost right after:

def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
Just pass in the window you want to raise as a argument, and this should work.

# 快捷键
python中tkinter需要使用accelerator添加菜单的快捷键，该选项仅显示，并没有实现加速键的功能，添加功能需按键绑定，代码如下：

```
from tkinter import *
root = Tk()
def callback():
    print("~被调用了~")
# 创建一个顶级菜单
menubar = Menu(root)
# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="打开", command=callback, accelerator='Ctrl+N')
filemenu.add_command(label="保存", command=callback)
filemenu.add_separator()
filemenu.add_command(label="退出", command=root.quit)
menubar.add_cascade(label="文件", menu=filemenu)
# 显示菜单
root.config(menu=menubar)
root.bind_all("<Control-n>", lambda event: print('加速键Ctrl+N'))
mainloop()
```


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
