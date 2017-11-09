#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import urllib2

# wxpython
import wx
from bs4 import BeautifulSoup

from hello.hello_ml.hello_knn import knn_classify


class MyFrame(wx.Frame):
    def __init__(self):
        html = urllib2.urlopen("http://tool.chinaz.com/Tools/web").read()
        soup = BeautifulSoup(html, "lxml")
        labeled_colors = []
        for color in soup.select("div.color"):
            red = int(color.select_one(".red").text)
            green = int(color.select_one(".green").text)
            blue = int(color.select_one(".blue").text)
            rgb = color.select(".html b")[1].text.strip()
            labeled_colors.append(([red, green, blue], rgb))
        self.labeled_colors = labeled_colors

        self.image = wx.Image("ml_subway.jpg", wx.BITMAP_TYPE_JPEG)
        wx.Frame.__init__(self, None, -1, "My Frame", size=(self.image.GetWidth() + 20, self.image.GetHeight()))
        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "Pos:", pos=(10, 12))
        self.posCtrl = wx.TextCtrl(panel, -1, "", pos=(40, 10))
        self.bitmap = wx.StaticBitmap(parent=panel, bitmap=self.image.ConvertToBitmap(), pos=(0, 40))
        self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.bitmap.Bind(wx.EVT_MOTION, self.OnMove)
        self.traces = []

    def OnMove(self, event):
        pos = event.GetPosition()
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

    def OnClick(self, event):
        pos = event.GetPosition()
        red, green, blue = \
            self.image.GetRed(pos.x, pos.y), \
            self.image.GetGreen(pos.x, pos.y), \
            self.image.GetBlue(pos.x, pos.y)
        rgb = knn_classify(1, self.labeled_colors, [red, green, blue]).encode("utf-8")  # 颜色使用最近的网络安全色
        # rgb = "#%s%s%s" %
        # (str(hex(red))[2:].zfill(2), str(hex(green))[2:].zfill(2), str(hex(blue))[2:].zfill(2))  # 位数
        trace = {'x': pos.x, 'y': pos.y, 'rgb': rgb}
        if len(self.traces) > 0:  # 点序列自动调整
            delta_x = math.fabs(pos.x - self.traces[-1]['x'])
            delta_y = math.fabs(pos.y - self.traces[-1]['y'])
            if delta_x < delta_y:
                trace['x'] = self.traces[-1]['x']
            else:
                trace['y'] = self.traces[-1]['y']
        dlg = wx.TextEntryDialog(None, u"站点的名字是?", u"站点", u"")
        if dlg.ShowModal() == wx.ID_OK:
            trace['name'] = dlg.GetValue()  # 填入名称

        self.traces.append(trace)
        print(self.traces)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
