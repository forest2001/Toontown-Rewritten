# 2013.08.22 22:14:17 Pacific Daylight Time
# Embedded file name: direct.gui.DirectScrollBar
__all__ = ['DirectScrollBar']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *
from DirectButton import *

class DirectScrollBar(DirectFrame):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGSliderBar, None),
         ('state', DGG.NORMAL, None),
         ('frameColor', (0.6, 0.6, 0.6, 1), None),
         ('range', (0, 1), self.setRange),
         ('value', 0, self.__setValue),
         ('scrollSize', 0.01, self.setScrollSize),
         ('pageSize', 0.1, self.setPageSize),
         ('orientation', DGG.HORIZONTAL, self.setOrientation),
         ('manageButtons', 1, self.setManageButtons),
         ('resizeThumb', 1, self.setResizeThumb),
         ('command', None, None),
         ('extraArgs', [], None))
        if kw.get('orientation') in (DGG.VERTICAL, DGG.VERTICAL_INVERTED):
            optiondefs += (('frameSize', (-0.04,
               0.04,
               -0.5,
               0.5), None),)
        else:
            optiondefs += (('frameSize', (-0.5,
               0.5,
               -0.04,
               0.04), None),)
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.thumb = self.createcomponent('thumb', (), None, DirectButton, (self,), borderWidth=self['borderWidth'])
        self.incButton = self.createcomponent('incButton', (), None, DirectButton, (self,), borderWidth=self['borderWidth'])
        self.decButton = self.createcomponent('decButton', (), None, DirectButton, (self,), borderWidth=self['borderWidth'])
        if self.decButton['frameSize'] == None and self.decButton.bounds == [0.0,
         0.0,
         0.0,
         0.0]:
            f = self['frameSize']
            if self['orientation'] == DGG.HORIZONTAL:
                self.decButton['frameSize'] = (f[0] * 0.05,
                 f[1] * 0.05,
                 f[2],
                 f[3])
            else:
                self.decButton['frameSize'] = (f[0],
                 f[1],
                 f[2] * 0.05,
                 f[3] * 0.05)
        if self.incButton['frameSize'] == None and self.incButton.bounds == [0.0,
         0.0,
         0.0,
         0.0]:
            f = self['frameSize']
            if self['orientation'] == DGG.HORIZONTAL:
                self.incButton['frameSize'] = (f[0] * 0.05,
                 f[1] * 0.05,
                 f[2],
                 f[3])
            else:
                self.incButton['frameSize'] = (f[0],
                 f[1],
                 f[2] * 0.05,
                 f[3] * 0.05)
        self.guiItem.setThumbButton(self.thumb.guiItem)
        self.guiItem.setLeftButton(self.decButton.guiItem)
        self.guiItem.setRightButton(self.incButton.guiItem)
        self.bind(DGG.ADJUST, self.commandFunc)
        self.initialiseoptions(DirectScrollBar)
        return

    def setRange(self):
        v = self['value']
        r = self['range']
        self.guiItem.setRange(r[0], r[1])
        self['value'] = v

    def __setValue(self):
        self.guiItem.setValue(self['value'])

    def setValue(self, value):
        self['value'] = value

    def getValue(self):
        return self.guiItem.getValue()

    def getRatio(self):
        return self.guiItem.getRatio()

    def setScrollSize(self):
        self.guiItem.setScrollSize(self['scrollSize'])

    def setPageSize(self):
        self.guiItem.setPageSize(self['pageSize'])

    def scrollStep(self, stepCount):
        self['value'] = self.guiItem.getValue() + self.guiItem.getScrollSize() * stepCount

    def scrollPage(self, pageCount):
        self['value'] = self.guiItem.getValue() + self.guiItem.getPageSize() * pageCount

    def setOrientation(self):
        if self['orientation'] == DGG.HORIZONTAL:
            self.guiItem.setAxis(Vec3(1, 0, 0))
        elif self['orientation'] == DGG.VERTICAL:
            self.guiItem.setAxis(Vec3(0, 0, -1))
        elif self['orientation'] == DGG.VERTICAL_INVERTED:
            self.guiItem.setAxis(Vec3(0, 0, 1))
        else:
            raise ValueError, 'Invalid value for orientation: %s' % self['orientation']

    def setManageButtons(self):
        self.guiItem.setManagePieces(self['manageButtons'])

    def setResizeThumb(self):
        self.guiItem.setResizeThumb(self['resizeThumb'])

    def destroy(self):
        self.thumb.destroy()
        del self.thumb
        self.incButton.destroy()
        del self.incButton
        self.decButton.destroy()
        del self.decButton
        DirectFrame.destroy(self)

    def commandFunc(self):
        self._optionInfo['value'][DGG._OPT_VALUE] = self.guiItem.getValue()
        if self['command']:
            apply(self['command'], self['extraArgs'])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectScrollBar.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:17 Pacific Daylight Time
