# 2013.08.22 22:14:17 Pacific Daylight Time
# Embedded file name: direct.gui.DirectScrolledFrame
__all__ = ['DirectScrolledFrame']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *
from DirectScrollBar import *

class DirectScrolledFrame(DirectFrame):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGScrollFrame, None),
         ('frameSize', (-0.5,
           0.5,
           -0.5,
           0.5), None),
         ('canvasSize', (-1, 1, -1, 1), self.setCanvasSize),
         ('manageScrollBars', 1, self.setManageScrollBars),
         ('autoHideScrollBars', 1, self.setAutoHideScrollBars),
         ('scrollBarWidth', 0.08, None),
         ('borderWidth', (0.01, 0.01), self.setBorderWidth))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        w = self['scrollBarWidth']
        self.verticalScroll = self.createcomponent('verticalScroll', (), None, DirectScrollBar, (self,), borderWidth=self['borderWidth'], frameSize=(-w / 2.0,
         w / 2.0,
         -1,
         1), orientation=DGG.VERTICAL)
        self.horizontalScroll = self.createcomponent('horizontalScroll', (), None, DirectScrollBar, (self,), borderWidth=self['borderWidth'], frameSize=(-1,
         1,
         -w / 2.0,
         w / 2.0), orientation=DGG.HORIZONTAL)
        self.guiItem.setVerticalSlider(self.verticalScroll.guiItem)
        self.guiItem.setHorizontalSlider(self.horizontalScroll.guiItem)
        self.canvas = NodePath(self.guiItem.getCanvasNode())
        self.initialiseoptions(DirectScrolledFrame)
        return

    def setCanvasSize(self):
        f = self['canvasSize']
        self.guiItem.setVirtualFrame(f[0], f[1], f[2], f[3])

    def getCanvas(self):
        return self.canvas

    def setManageScrollBars(self):
        self.guiItem.setManagePieces(self['manageScrollBars'])

    def setAutoHideScrollBars(self):
        self.guiItem.setAutoHide(self['autoHideScrollBars'])

    def commandFunc(self):
        if self['command']:
            apply(self['command'], self['extraArgs'])

    def destroy(self):
        for child in self.canvas.getChildren():
            childGui = self.guiDict.get(child.getName())
            if childGui:
                childGui.destroy()
            else:
                parts = child.getName().split('-')
                simpleChildGui = self.guiDict.get(parts[-1])
                if simpleChildGui:
                    simpleChildGui.destroy()

        self.verticalScroll.destroy()
        self.horizontalScroll.destroy()
        del self.verticalScroll
        del self.horizontalScroll
        DirectFrame.destroy(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectScrolledFrame.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:17 Pacific Daylight Time
