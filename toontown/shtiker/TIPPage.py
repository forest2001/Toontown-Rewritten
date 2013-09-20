# 2013.08.22 22:25:07 Pacific Daylight Time
# Embedded file name: toontown.shtiker.TIPPage
from pandac.PandaModules import *
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class TIPPage(ShtikerPage.ShtikerPage):
    __module__ = __name__

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)

    def load(self):
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.TIPPageTitle, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        return

    def unload(self):
        del self.title
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        ShtikerPage.ShtikerPage.unload(self)

    def updatePage(self):
        pass

    def enter(self):
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\shtiker\TIPPage.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:07 Pacific Daylight Time
