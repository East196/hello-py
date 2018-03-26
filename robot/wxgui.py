#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import time
import urllib2 as request
from random import randint
from threading import *
from wx.lib.pubsub import pub
import re

ID_START = wx.NewId()
ID_STOP = wx.NewId()
EVT_RESULT_ID = wx.NewId()

url = ""
n = 0
flag = 0
time_x = 0
proxy = [{'https': '110.88.10.198'}, {'https': '182.88.117.118'}, {'https': '180.158.109.60'},
         {'https': '110.88.10.198'}, {'https': '122.235.184.109'}, {'https': '221.3.39.207'},
         {'https': '122.72.18.34'}, {'https': '61.155.164.111'}, {'https': '221.222.31.229'}]


def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class WorkerThread(Thread):
    """Worker Thread Class."""

    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        global url
        global n
        global flag
        global time_x
        global proxy
        try:
            for _ in range(n):
                proxy_support = request.ProxyHandler(proxy[randint(0, len(proxy) - 1)])
                opener = request.build_opener(proxy_support)
                opener.addheaders = [('User-Agent',
                                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
                request.install_opener(opener)
                time.sleep(time_x)
                response = request.urlopen(url)
                # print((_ + 1) / n * 100)
                wx.CallAfter(pub.sendMessage, "update", msg=str((_ + 1) / n * 100))
        except:
            # print("ERROR")
            return

    def abort(self):
        """abort worker thread."""
        self._want_abort = 1


class InfoPanel(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "Boomer", pos=(0, 0), size=(660, 500))
        panel = wx.Panel(self, -1)
        self.text = wx.TextCtrl(panel, wx.ID_ANY, pos=(90, 5), size=(550, 25))
        self.num = wx.TextCtrl(panel, wx.ID_ANY, pos=(90, 47), size=(100, 25))
        self.pro_xy = wx.TextCtrl(panel, wx.ID_ANY, pos=(90, 220), size=(200, 150), style=wx.TE_MULTILINE)
        self.pro_xy_add = wx.TextCtrl(panel, wx.ID_ANY, pos=(400, 270), size=(200, 50))
        # 创建普通文本实例，并设置其属性－前/背景色
        wx.StaticText(panel, -1, 'URL:', pos=(35, 8))
        wx.StaticText(panel, -1, 'Quantity:', pos=(27, 50))
        wx.StaticText(panel, -1, 'Progress:', pos=(27, 100))
        wx.StaticText(panel, -1, 'Faster', pos=(225, 50))
        wx.StaticText(panel, -1, 'Slower', pos=(470, 50))
        wx.StaticText(panel, -1, '-----------------------------------------------------Advanced Function'
                                 '------------------------------------------------------', pos=(0, 200))
        button = wx.Button(panel, wx.ID_ANY, pos=(100, 145), size=(200, 50), label='Run Now')
        button.Bind(wx.EVT_BUTTON, self.running)
        button = wx.Button(panel, wx.ID_ANY, pos=(400, 145), size=(200, 50), label='Clear and Stop')
        button.Bind(wx.EVT_BUTTON, self.clear_all)
        button = wx.Button(panel, wx.ID_ANY, pos=(400, 380), size=(200, 50), label='Proxy Adding')
        button.Bind(wx.EVT_BUTTON, self.proxy_add)
        button = wx.Button(panel, wx.ID_ANY, pos=(90, 380), size=(200, 50), label='All Proxy')
        button.Bind(wx.EVT_BUTTON, self.output)
        button = wx.Button(panel, wx.ID_ANY, pos=(400, 330), size=(200, 50), label='Clear Proxy')
        button.Bind(wx.EVT_BUTTON, self.clear_proxy)
        self.slider = wx.Slider(panel, wx.ID_ANY, 0, 0, 250, pos=(260, 47), size=(200, 30))
        self.slider.Bind(wx.EVT_SCROLL, self.transparent)
        self.SetTransparent(240)
        self.bar = wx.Gauge(panel, wx.ID_ANY, pos=(90, 95), size=(550, 30))
        wx.StaticText(panel, -1, '  Proxy Used:', pos=(5, 320))
        wx.StaticText(panel, -1, '  Proxy Adding Down:', pos=(420, 230))
        wx.StaticText(panel, -1, '  HTTPS ONLY!!!', pos=(420, 250))
        wx.StaticText(panel, -1, '  OmegaXYZ.com', pos=(20, 440))
        pub.subscribe(self.run_set_value, "update")
        self.output(self)

    def clear_proxy(self, event):
        self.pro_xy.Clear()
        global proxy
        proxy = []

    def proxy_add(self, event):
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        if reip.match(self.pro_xy_add.GetValue()):
            temp = {}
            temp['https'] = self.pro_xy_add.GetValue()
            proxy.append(temp)
            self.output(self)
        else:
            dlg = wx.MessageDialog(self,
                                   'ERROR proxy错误', 'ERROR!', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        self.pro_xy_add.Clear()

    def output(self, event):
        self.pro_xy.Clear()
        for _ in range(len(proxy)):
            self.pro_xy.AppendText(str(proxy[_]) + '\n')

    def transparent(self, event):
        global time_x
        time_x = self.slider.GetValue() / 300

    def clear_all(self, event):
        self.text.Clear()
        self.num.Clear()
        self.bar.SetValue(0)
        self.worker.abort()

    def running(self, msg):
        global url
        global n
        global flag
        url = self.text.GetValue()
        if url == "":
            dlg = wx.MessageDialog(self,
                                   'ERROR 请填写URL', 'ERROR!', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        elif "http" not in url:
            dlg = wx.MessageDialog(self,
                                   'ERROR URL错误', 'ERROR!', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            try:
                n = int(self.num.GetValue())
                self.worker = WorkerThread(self)

            except ValueError:
                dlg = wx.MessageDialog(self,
                                       'ERROR 数量输入错误', 'ERROR！', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

    def run_set_value(self, msg):
        self.bar.SetValue(float(msg))
        if self.bar.GetValue() > 99.0:
            dlg = wx.MessageDialog(self,
                                   'URL:' + url + '\n成功刷了' + str(n) + '个访客', 'Mission Accomplished',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()


class MainApp(wx.App):
    def OnInit(self):
        self.frame1 = InfoPanel(None, -1)
        self.frame1.Center()
        self.frame1.Show(True)
        self.SetTopWindow(self.frame1)
        return True


if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
