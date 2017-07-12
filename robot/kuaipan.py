#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import urllib
import urllib2
import cookielib
import json
import re
import wx


def create(parent):
    return Frame1(parent)


[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1,
 wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, wxID_FRAME1TEXTCTRL1,
 wxID_FRAME1TEXTCTRL2,
 ] = [wx.NewId() for _init_ctrls in range(8)]


class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
                          pos=wx.Point(529, 321), size=wx.Size(400, 250),
                          style=wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION,
                          title='金山快盘自动签到V1.0')
        self.SetClientSize(wx.Size(392, 216))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
                               pos=wx.Point(0, 0), size=wx.Size(392, 216),
                               style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
                                         label='用户名：', name='staticText1', parent=self.panel1,
                                         pos=wx.Point(8, 16), size=wx.Size(95, 23), style=0)
        self.staticText1.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD,
                                         False, u'Tahoma'))

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
                                         label='密码：', name='staticText2', parent=self.panel1,
                                         pos=wx.Point(8, 56), size=wx.Size(92, 23), style=0)
        self.staticText2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD,
                                         False, u'Tahoma'))

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
                                     parent=self.panel1, pos=wx.Point(112, 16), size=wx.Size(176, 24),
                                     style=0, value='')

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
                                     parent=self.panel1, pos=wx.Point(112, 56), size=wx.Size(176, 22),
                                     style=wx.TE_PASSWORD, value='')

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='签到',
                                 name='button1', parent=self.panel1, pos=wx.Point(304, 56),
                                 size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
                          id=wxID_FRAME1BUTTON1)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
                                         label='签到 状态 ......', name='staticText3', parent=self.panel1,
                                         pos=wx.Point(16, 104), size=wx.Size(352, 96), style=0)
        self.staticText3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
                                         False, u'Tahoma'))
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
                          id=wxID_FRAME1BUTTON1)

        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(self.opener)
        self.opener.addheaders = [('User-agent', 'IE')]

    def __init__(self, parent):
        self._init_ctrls(parent)

    def login(self, username, password):
        url = 'https://www.kuaipan.cn/index.php?ac=account&op=login'
        data = urllib.urlencode({'username': username, 'userpwd': password})
        req = urllib2.Request(url, data)

        try:
            fd = self.opener.open(req)

        except Exception, e:
            self.staticText3.SetLabel('网络连接错误！')
            return False
        if fd.url != "http://www.kuaipan.cn/home.htm":
            self.staticText3.SetLabel("用户名跟密码不匹配！")
            return False
        self.staticText3.SetLabel('%s 登陆成功' % username),
        return True

    def logout(self):
        url = 'http://www.kuaipan.cn/index.php?ac=account&op=logout'
        req = urllib2.Request(url)
        fd = self.opener.open(req)
        fd.close()

    def sign(self):

        url = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
        req = urllib2.Request(url)
        fd = self.opener.open(req)
        sign_js = json.loads(fd.read())

        # print sign_js

        tri = self.staticText3.GetLabel()

        if sign_js['state'] == -102:
            self.staticText3.SetLabel(tri + '\n' + "今天已签到了!")
        elif sign_js['state'] == 1:
            self.staticText3.SetLabel(tri + '\n' + "签到成功! \n获得积分：%d，总积分：%d；\n获得空间：%dM\n" % (
            sign_js['increase'], sign_js['status']['points'], sign_js['rewardsize']))
        else:
            self.staticText3.SetLabel(tri + '\n' + "签到失败！")
        fd.close()

    def OnButton1Button(self, event):
        self.staticText3.SetLabel('')
        namew = self.textCtrl1.GetValue()
        passw = self.textCtrl2.GetValue()
        if self.login(namew, passw) == True:
            self.sign()
        self.logout()
        # event.Skip()


class App(wx.App):
    def OnInit(self):
        self.main = create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    application = App(0)
    application.MainLoop()


if __name__ == '__main__':
    main()