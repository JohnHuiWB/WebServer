#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : interface.py
# @Author: JohnHuiWB
# @Date  : 2018/4/11 0011
# @Desc  :
# @Contact : huiwenbin199822@gmail.com
# @Software : PyCharm

import wx
import threading
import webbrowser
from server import Server

class WebServerInterface(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self):
        # ensure the parent's __init__ is called
        super(WebServerInterface, self).__init__(None, id=-1, size=(800, 500), title='Web Server')

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0, 0)

        stext_port = wx.StaticText(panel, label="Port:")
        sizer.Add(stext_port, pos=(0, 0), span=(0, 2), flag=wx.EXPAND|wx.ALL, border=5)

        self.text_port = wx.TextCtrl(panel)
        sizer.Add(self.text_port, pos=(0, 2), span=(0, 3), flag=wx.EXPAND|wx.ALL, border=5)

        button_set_port = wx.Button(panel, label="Set Port")
        sizer.Add(button_set_port, pos=(0, 15), flag=wx.EXPAND|wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self._set_port, button_set_port)

        stext_log = wx.StaticText(panel, label="Log:")
        sizer.Add(stext_log, pos=(1, 0), flag=wx.ALL, border=5)

        button_open = wx.Button(panel, label='open')
        sizer.Add(button_open, pos=(1, 15), flag=wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self._open, button_open)

        self.text_log = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        sizer.Add(self.text_log, pos=(2, 0), span=(15, 50), flag=wx.EXPAND|wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("UESTC 2016220203003 JohnHuiWB")

        self.Centre()

        self.s = None
        self.t = None
        self.port_num = None

    def _set_port(self, event):
        self.port_num = str(self.text_port.GetValue())
        if self.port_num.isdigit():
            if self.s: del self.s
            self.text_log.AppendText('Set port: ' + self.port_num + '\n')
            self.s = Server(int(self.port_num), self.text_log)
            self.t = threading.Thread(target=self.s.run, name='LoopThread')
            self.t.setDaemon(True)
            self.t.start()
            self.text_log.AppendText('Click \'Open\' or enter following URL in your browser:\n'\
                                     +'\t127.0.0.1:'+self.port_num+'/uestc.html\n')
        else:
            self.text_log.AppendText('Please enter a digit.\n')

    def _open(self, event):
        if self.s:
            webbrowser_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            self.text_log.AppendText('Open in a new browser. Path: ' + webbrowser_path + '\n')
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(webbrowser_path))
            webbrowser.get('chrome').open_new_tab('127.0.0.1:'+self.port_num+'/uestc.html')
        else:
            self.text_log.AppendText('Please set a port first.\n')


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    wsi = WebServerInterface()
    wsi.Show()
    app.MainLoop()
