# 2013.08.22 22:14:50 Pacific Daylight Time
# Embedded file name: direct.showbase.WxGlobal
import wx
from direct.task.Task import Task

def wxLoop(self):
    while base.wxApp.Pending():
        base.wxApp.Dispatch()

    return Task.cont


def spawnWxLoop():
    if not getattr(base, 'wxApp', None):
        base.wxApp = wx.App(False)
    taskMgr.add(wxLoop, 'wxLoop')
    return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\WxGlobal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:50 Pacific Daylight Time
