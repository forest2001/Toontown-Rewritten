# 2013.08.22 22:21:41 Pacific Daylight Time
# Embedded file name: toontown.minigame.DistributedTagTreasure
from toontown.safezone import DistributedTreasure

class DistributedTagTreasure(DistributedTreasure.DistributedTreasure):
    __module__ = __name__

    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/icecream'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'
        self.accept('minigameOffstage', self.handleMinigameOffstage)

    def handleEnterSphere(self, collEntry):
        if not base.localAvatar.isIt:
            self.d_requestGrab()
        return None

    def handleMinigameOffstage(self):
        self.nodePath.reparentTo(hidden)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\DistributedTagTreasure.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:41 Pacific Daylight Time
