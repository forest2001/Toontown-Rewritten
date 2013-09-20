# 2013.08.22 22:24:54 Pacific Daylight Time
# Embedded file name: toontown.shtiker.InGameNewsFrame
import datetime
from toontown.shtiker import HtmlView

class InGameNewsFrame(HtmlView.HtmlView):
    __module__ = __name__
    TaskName = 'HtmlViewUpdateTask'

    def __init__(self, parent = aspect2d):
        HtmlView.HtmlView.__init__(self, parent)
        self.initialLoadDone = False
        self.accept('newsSnapshot', self.doSnapshot)

    def activate(self):
        self.quad.show()
        self.calcMouseLimits()
        if not self.initialLoadDone:
            inGameNewsUrl = self.getInGameNewsUrl()
            self.webView.loadURL2(inGameNewsUrl)
            self.initialLoadDone = True
        taskMgr.add(self.update, self.TaskName)

    def deactivate(self):
        self.quad.hide()
        taskMgr.remove(self.TaskName)

    def unload(self):
        self.deactivate()
        HtmlView.HtmlView.unload(self)
        self.ignore('newsSnapshot')

    def doSnapshot(self):
        curtime = datetime.datetime.now()
        filename = 'news_snapshot_' + curtime.isoformat()
        filename = filename.replace(':', '-')
        filename = filename.replace('.', '-')
        pngfilename = filename + '.png'
        self.writeTex(pngfilename)
        jpgfilename = filename + '.jpg'
        self.writeTex(jpgfilename)
        return jpgfilename
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\shtiker\InGameNewsFrame.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:55 Pacific Daylight Time
