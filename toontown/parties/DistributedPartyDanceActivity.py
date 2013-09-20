# 2013.08.22 22:23:21 Pacific Daylight Time
# Embedded file name: toontown.parties.DistributedPartyDanceActivity
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyDanceActivityBase import DistributedPartyDanceActivityBase
from toontown.toonbase import TTLocalizer

class DistributedPartyDanceActivity(DistributedPartyDanceActivityBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPartyDanceActivity')

    def __init__(self, cr):
        DistributedPartyDanceActivityBase.__init__(self, cr, PartyGlobals.ActivityIds.PartyDance, PartyGlobals.DancePatternToAnims)

    def getInstructions(self):
        return TTLocalizer.PartyDanceActivityInstructions

    def getTitle(self):
        return TTLocalizer.PartyDanceActivityTitle

    def load(self):
        DistributedPartyDanceActivityBase.load(self)
        parentGroup = self.danceFloor.find('**/discoBall_mesh')
        correctBall = self.danceFloor.find('**/discoBall_10')
        origBall = self.danceFloor.find('**/discoBall_mesh_orig')
        if not correctBall.isEmpty():
            numChildren = parentGroup.getNumChildren()
            for i in xrange(numChildren):
                child = parentGroup.getChild(i)
                if child != correctBall:
                    child.hide()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\DistributedPartyDanceActivity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:21 Pacific Daylight Time
