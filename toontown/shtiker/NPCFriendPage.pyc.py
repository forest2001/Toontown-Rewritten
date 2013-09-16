# 2013.08.22 22:25:00 Pacific Daylight Time
# Embedded file name: toontown.shtiker.NPCFriendPage
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toon import NPCFriendPanel
from toontown.toonbase import TTLocalizer

class NPCFriendPage(ShtikerPage.ShtikerPage):
    __module__ = __name__

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.NPCFriendPageTitle, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        self.friendPanel = NPCFriendPanel.NPCFriendPanel(parent=self)
        self.friendPanel.setScale(0.1225)
        self.friendPanel.setZ(-0.03)
        return

    def unload(self):
        ShtikerPage.ShtikerPage.unload(self)
        del self.title
        del self.friendPanel

    def updatePage(self):
        self.friendPanel.update(base.localAvatar.NPCFriendsDict, fCallable=0)

    def enter(self):
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\shtiker\NPCFriendPage.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:00 Pacific Daylight Time
