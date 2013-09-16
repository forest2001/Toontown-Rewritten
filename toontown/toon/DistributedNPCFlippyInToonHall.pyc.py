# 2013.08.22 22:25:42 Pacific Daylight Time
# Embedded file name: toontown.toon.DistributedNPCFlippyInToonHall
from pandac.PandaModules import *
from DistributedNPCToon import *

class DistributedNPCFlippyInToonHall(DistributedNPCToon):
    __module__ = __name__

    def __init__(self, cr):
        DistributedNPCToon.__init__(self, cr)

    def getCollSphereRadius(self):
        return 4

    def initPos(self):
        self.clearMat()
        self.setScale(1.25)

    def handleCollisionSphereEnter(self, collEntry):
        if self.allowedToTalk():
            base.cr.playGame.getPlace().fsm.request('quest', [self])
            self.sendUpdate('avatarEnter', [])
            self.nametag3d.setDepthTest(0)
            self.nametag3d.setBin('fixed', 0)
            self.lookAt(base.localAvatar)
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='quests', doneFunc=self.handleOkTeaser)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\toon\DistributedNPCFlippyInToonHall.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:42 Pacific Daylight Time
