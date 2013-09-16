# 2013.08.22 22:14:12 Pacific Daylight Time
# Embedded file name: direct.gui.DirectButton
__all__ = ['DirectButton']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *

class DirectButton(DirectFrame):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGButton, None),
         ('numStates', 4, None),
         ('state', DGG.NORMAL, None),
         ('relief', DGG.RAISED, None),
         ('invertedFrames', (1,), None),
         ('command', None, None),
         ('extraArgs', [], None),
         ('commandButtons', (DGG.LMB,), self.setCommandButtons),
         ('rolloverSound', DGG.getDefaultRolloverSound(), self.setRolloverSound),
         ('clickSound', DGG.getDefaultClickSound(), self.setClickSound),
         ('pressEffect', 1, DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        pressEffectNP = None
        if self['pressEffect']:
            pressEffectNP = self.stateNodePath[1].attachNewNode('pressEffect', 1)
            self.stateNodePath[1] = pressEffectNP
        self.initialiseoptions(DirectButton)
        if pressEffectNP:
            bounds = self.getBounds()
            centerX = (bounds[0] + bounds[1]) / 2
            centerY = (bounds[2] + bounds[3]) / 2
            mat = Mat4.translateMat(-centerX, 0, -centerY) * Mat4.scaleMat(0.98) * Mat4.translateMat(centerX, 0, centerY)
            pressEffectNP.setMat(mat)
        return

    def setCommandButtons(self):
        if DGG.LMB in self['commandButtons']:
            self.guiItem.addClickButton(MouseButton.one())
            self.bind(DGG.B1CLICK, self.commandFunc)
        else:
            self.unbind(DGG.B1CLICK)
            self.guiItem.removeClickButton(MouseButton.one())
        if DGG.MMB in self['commandButtons']:
            self.guiItem.addClickButton(MouseButton.two())
            self.bind(DGG.B2CLICK, self.commandFunc)
        else:
            self.unbind(DGG.B2CLICK)
            self.guiItem.removeClickButton(MouseButton.two())
        if DGG.RMB in self['commandButtons']:
            self.guiItem.addClickButton(MouseButton.three())
            self.bind(DGG.B3CLICK, self.commandFunc)
        else:
            self.unbind(DGG.B3CLICK)
            self.guiItem.removeClickButton(MouseButton.three())

    def commandFunc(self, event):
        if self['command']:
            apply(self['command'], self['extraArgs'])

    def setClickSound(self):
        clickSound = self['clickSound']
        self.guiItem.clearSound(DGG.B1PRESS + self.guiId)
        self.guiItem.clearSound(DGG.B2PRESS + self.guiId)
        self.guiItem.clearSound(DGG.B3PRESS + self.guiId)
        if clickSound:
            if DGG.LMB in self['commandButtons']:
                self.guiItem.setSound(DGG.B1PRESS + self.guiId, clickSound)
            if DGG.MMB in self['commandButtons']:
                self.guiItem.setSound(DGG.B2PRESS + self.guiId, clickSound)
            if DGG.RMB in self['commandButtons']:
                self.guiItem.setSound(DGG.B3PRESS + self.guiId, clickSound)

    def setRolloverSound(self):
        rolloverSound = self['rolloverSound']
        if rolloverSound:
            self.guiItem.setSound(DGG.ENTER + self.guiId, rolloverSound)
        else:
            self.guiItem.clearSound(DGG.ENTER + self.guiId)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectButton.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:12 Pacific Daylight Time
