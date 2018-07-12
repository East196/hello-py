#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con

print("Hello,world!")


def find_idxSubHandle(pHandle, winClass, index=0):
    """ 
                已知子窗口的窗体类名 
                寻找第index号个同类型的兄弟窗口 
    """
    assert type(index) == int and index >= 0
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)
    while index > 0:
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)
        index -= 1
    return handle


def find_subHandle(pHandle, winClassList):
    """ 
             递归寻找子窗口的句柄 
    pHandle是祖父窗口的句柄 
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈 
    """
    assert type(winClassList) == list
    if len(winClassList) == 1:
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
    else:
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
        return find_subHandle(pHandle, winClassList[1:])


"""输出phandle的所有子控件"""


def p_sub_handle(phandle):
    handle = -1
    while handle != 0:
        if handle == -1:
            handle = 0
        handle = win32gui.FindWindowEx(phandle, handle, None, None)
        if handle != 0:
            className = win32gui.GetClassName(handle)
            print(className)


"""
    记事本实例
"""
notepadHhandle = win32gui.FindWindow("Notepad", None)
print("%x" % (notepadHhandle))

editHandle = find_subHandle(notepadHhandle, [("Edit", 0)])
print("%x" % (editHandle))

"""修改edit中的值"""
win32api.SendMessage(editHandle, win32con.WM_SETTEXT, 0, "666666")

command_dict = {  # [目录的编号, 打开的窗口名]
    "open": [3, u"打开"]
}

"""操作菜单"""
menu = win32gui.GetMenu(notepadHhandle)
menu = win32gui.GetSubMenu(menu, 0)
cmd_ID = win32gui.GetMenuItemID(menu, command_dict["open"][0])
if cmd_ID == -1:
    print("没有找到相应的菜单")
else:
    print("菜单id:%x" % (cmd_ID))
win32gui.PostMessage(notepadHhandle, win32con.WM_COMMAND, cmd_ID, 0)