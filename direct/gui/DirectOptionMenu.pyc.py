# 2013.08.22 22:14:16 Pacific Daylight Time
# Embedded file name: direct.gui.DirectOptionMenu
__all__ = ['DirectOptionMenu']
import types
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectButton import *
from DirectLabel import *
from DirectFrame import *

class DirectOptionMenu(DirectButton):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('items', [], self.setItems),
         ('initialitem', None, DGG.INITOPT),
         ('popupMarkerBorder', (0.1, 0.1), None),
         ('highlightColor', (0.5, 0.5, 0.5, 1), None),
         ('highlightScale', (1, 1), None),
         ('text_align', TextNode.ALeft, None),
         ('pressEffect', 0, DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initFrameSize = self['frameSize']
        self.popupMarker = self.createcomponent('popupMarker', (), None, DirectFrame, (self,), frameSize=(-0.5,
         0.5,
         -0.2,
         0.2), scale=0.4, relief=DGG.RAISED)
        self.popupMarker.bind(DGG.B1PRESS, self.showPopupMenu)
        self.popupMarker.bind(DGG.B1RELEASE, self.selectHighlightedIndex)
        self.popupMarker.guiItem.setSound(DGG.B1PRESS + self.popupMarker.guiId, self['clickSound'])
        self.popupMenu = None
        self.selectedIndex = None
        self.highlightedIndex = None
        self.cancelFrame = self.createcomponent('cancelframe', (), None, DirectFrame, (self,), frameSize=(-1, 1, -1, 1), relief=None, state='normal')
        self.cancelFrame.setBin('gui-popup', 0)
        self.cancelFrame.bind(DGG.B1PRESS, self.hidePopupMenu)
        self.bind(DGG.B1PRESS, self.showPopupMenu)
        self.bind(DGG.B1RELEASE, self.selectHighlightedIndex)
        self.initialiseoptions(DirectOptionMenu)
        self.resetFrameSize()
        return

    def setItems(self):
        if self.popupMenu != None:
            self.destroycomponent('popupMenu')
        self.popupMenu = self.createcomponent('popupMenu', (), None, DirectFrame, (self,), relief='raised')
        self.popupMenu.setBin('gui-popup', 0)
        if not self['items']:
            return
        itemIndex = 0
        self.minX = self.maxX = self.minZ = self.maxZ = None
        for item in self['items']:
            c = self.createcomponent('item%d' % itemIndex, (), 'item', DirectButton, (self.popupMenu,), text=item, text_align=TextNode.ALeft, command=lambda i = itemIndex: self.set(i))
            bounds = c.getBounds()
            if self.minX == None:
                self.minX = bounds[0]
            elif bounds[0] < self.minX:
                self.minX = bounds[0]
            if self.maxX == None:
                self.maxX = bounds[1]
            elif bounds[1] > self.maxX:
                self.maxX = bounds[1]
            if self.minZ == None:
                self.minZ = bounds[2]
            elif bounds[2] < self.minZ:
                self.minZ = bounds[2]
            if self.maxZ == None:
                self.maxZ = bounds[3]
            elif bounds[3] > self.maxZ:
                self.maxZ = bounds[3]
            itemIndex += 1

        self.maxWidth = self.maxX - self.minX
        self.maxHeight = self.maxZ - self.minZ
        for i in range(itemIndex):
            item = self.component('item%d' % i)
            item['frameSize'] = (self.minX,
             self.maxX,
             self.minZ,
             self.maxZ)
            item.setPos(-self.minX, 0, -self.maxZ - i * self.maxHeight)
            item.bind(DGG.B1RELEASE, self.hidePopupMenu)
            item.bind(DGG.WITHIN, lambda x, i = i, item = item: self._highlightItem(item, i))
            fc = item['frameColor']
            item.bind(DGG.WITHOUT, lambda x, item = item, fc = fc: self._unhighlightItem(item, fc))

        f = self.component('popupMenu')
        f['frameSize'] = (0,
         self.maxWidth,
         -self.maxHeight * itemIndex,
         0)
        if self['initialitem']:
            self.set(self['initialitem'], fCommand=0)
        else:
            self.set(0, fCommand=0)
        pm = self.popupMarker
        pmw = pm.getWidth() * pm.getScale()[0] + 2 * self['popupMarkerBorder'][0]
        if self.initFrameSize:
            bounds = list(self.initFrameSize)
        else:
            bounds = [self.minX,
             self.maxX,
             self.minZ,
             self.maxZ]
        pm.setPos(bounds[1] + pmw / 2.0, 0, bounds[2] + (bounds[3] - bounds[2]) / 2.0)
        bounds[1] += pmw
        self['frameSize'] = (bounds[0],
         bounds[1],
         bounds[2],
         bounds[3])
        self.hidePopupMenu()
        return

    def showPopupMenu(self, event = None):
        self.popupMenu.show()
        self.popupMenu.setScale(self, VBase3(1))
        b = self.getBounds()
        fb = self.popupMenu.getBounds()
        xPos = (b[1] - b[0]) / 2.0 - fb[0]
        self.popupMenu.setX(self, xPos)
        self.popupMenu.setZ(self, self.minZ + (self.selectedIndex + 1) * self.maxHeight)
        pos = self.popupMenu.getPos(render2d)
        scale = self.popupMenu.getScale(render2d)
        maxX = pos[0] + fb[1] * scale[0]
        if maxX > 1.0:
            self.popupMenu.setX(render2d, pos[0] + (1.0 - maxX))
        minZ = pos[2] + fb[2] * scale[2]
        maxZ = pos[2] + fb[3] * scale[2]
        if minZ < -1.0:
            self.popupMenu.setZ(render2d, pos[2] + (-1.0 - minZ))
        elif maxZ > 1.0:
            self.popupMenu.setZ(render2d, pos[2] + (1.0 - maxZ))
        self.cancelFrame.show()
        self.cancelFrame.setPos(render2d, 0, 0, 0)
        self.cancelFrame.setScale(render2d, 1, 1, 1)

    def hidePopupMenu(self, event = None):
        self.popupMenu.hide()
        self.cancelFrame.hide()

    def _highlightItem(self, item, index):
        item['frameColor'] = self['highlightColor']
        item['frameSize'] = (self['highlightScale'][0] * self.minX,
         self['highlightScale'][0] * self.maxX,
         self['highlightScale'][1] * self.minZ,
         self['highlightScale'][1] * self.maxZ)
        item['text_scale'] = self['highlightScale']
        self.highlightedIndex = index

    def _unhighlightItem(self, item, frameColor):
        item['frameColor'] = frameColor
        item['frameSize'] = (self.minX,
         self.maxX,
         self.minZ,
         self.maxZ)
        item['text_scale'] = (1, 1)
        self.highlightedIndex = None
        return

    def selectHighlightedIndex(self, event = None):
        if self.highlightedIndex is not None:
            self.set(self.highlightedIndex)
            self.hidePopupMenu()
        return

    def index(self, index):
        intIndex = None
        if isinstance(index, types.IntType):
            intIndex = index
        elif index in self['items']:
            i = 0
            for item in self['items']:
                if item == index:
                    intIndex = i
                    break
                i += 1

        return intIndex

    def set(self, index, fCommand = 1):
        newIndex = self.index(index)
        if newIndex is not None:
            self.selectedIndex = newIndex
            item = self['items'][self.selectedIndex]
            self['text'] = item
            if fCommand and self['command']:
                apply(self['command'], [item] + self['extraArgs'])
        return

    def get(self):
        return self['items'][self.selectedIndex]

    def commandFunc(self, event):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectOptionMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:17 Pacific Daylight Time
