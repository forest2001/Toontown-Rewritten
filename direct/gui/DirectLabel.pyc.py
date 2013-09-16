# 2013.08.22 22:14:16 Pacific Daylight Time
# Embedded file name: direct.gui.DirectLabel
__all__ = ['DirectLabel']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *

class DirectLabel(DirectFrame):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGItem, None),
         ('numStates', 1, None),
         ('state', self.inactiveInitState, None),
         ('activeState', 0, self.setActiveState))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(DirectLabel)
        return

    def setActiveState(self):
        self.guiItem.setState(self['activeState'])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectLabel.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:16 Pacific Daylight Time
