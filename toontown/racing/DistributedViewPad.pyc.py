# 2013.08.22 22:24:13 Pacific Daylight Time
# Embedded file name: toontown.racing.DistributedViewPad
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task import Task
from pandac.PandaModules import *
from toontown.racing.DistributedKartPad import DistributedKartPad
from toontown.racing.KartShopGlobals import KartGlobals
if __debug__:
    import pdb

class DistributedViewPad(DistributedKartPad):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedViewPad')
    id = 0

    def __init__(self, cr):
        DistributedKartPad.__init__(self, cr)
        self.id = DistributedViewPad.id
        DistributedViewPad.id += 1

    def setLastEntered(self, timeStamp):
        self.timeStamp = timeStamp

    def getTimestamp(self, avId):
        return self.timeStamp

    def addStartingBlock(self, block):
        block.cameraPos = Point3(0, 23, 7)
        block.cameraHpr = Point3(180, -10, 0)
        DistributedKartPad.addStartingBlock(self, block)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\DistributedViewPad.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:13 Pacific Daylight Time
