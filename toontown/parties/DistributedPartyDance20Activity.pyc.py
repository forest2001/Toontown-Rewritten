# 2013.08.22 22:23:21 Pacific Daylight Time
# Embedded file name: toontown.parties.DistributedPartyDance20Activity
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyDanceActivityBase import DistributedPartyDanceActivityBase
from toontown.toonbase import TTLocalizer

class DistributedPartyDance20Activity(DistributedPartyDanceActivityBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPartyDanceActivity')

    def __init__(self, cr):
        DistributedPartyDanceActivityBase.__init__(self, cr, PartyGlobals.ActivityIds.PartyDance20, PartyGlobals.DancePatternToAnims20)

    def getInstructions(self):
        return TTLocalizer.PartyDanceActivity20Instructions

    def getTitle(self):
        return TTLocalizer.PartyDanceActivity20Title

    def load(self):
        DistributedPartyDanceActivityBase.load(self)
        parentGroup = self.danceFloor.find('**/discoBall_mesh')
        correctBall = self.danceFloor.find('**/discoBall_20')
        if not correctBall.isEmpty():
            numChildren = parentGroup.getNumChildren()
            for i in xrange(numChildren):
                child = parentGroup.getChild(i)
                if child != correctBall:
                    child.hide()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\DistributedPartyDance20Activity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:21 Pacific Daylight Time
