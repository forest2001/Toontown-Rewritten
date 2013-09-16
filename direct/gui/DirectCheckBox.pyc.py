# 2013.08.22 22:14:12 Pacific Daylight Time
# Embedded file name: direct.gui.DirectCheckBox
from direct.gui.DirectGui import *
from pandac.PandaModules import *

class DirectCheckBox(DirectButton):
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
         ('pressEffect', 1, DGG.INITOPT),
         ('uncheckedImage', None, None),
         ('checkedImage', None, None),
         ('isChecked', False, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(DirectCheckBox)
        return

    def commandFunc(self, event):
        self['isChecked'] = not self['isChecked']
        if self['isChecked']:
            self['image'] = self['checkedImage']
        else:
            self['image'] = self['uncheckedImage']
        self.setImage()
        if self['command']:
            apply(self['command'], [self['isChecked']] + self['extraArgs'])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectCheckBox.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:12 Pacific Daylight Time
