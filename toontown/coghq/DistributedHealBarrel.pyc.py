# 2013.08.22 22:18:40 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedHealBarrel
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal
import DistributedBarrelBase

class DistributedHealBarrel(DistributedBarrelBase.DistributedBarrelBase):
    __module__ = __name__

    def __init__(self, cr):
        DistributedBarrelBase.DistributedBarrelBase.__init__(self, cr)
        self.numGags = 0
        self.gagScale = 0.6

    def disable(self):
        DistributedBarrelBase.DistributedBarrelBase.disable(self)
        self.ignoreAll()

    def delete(self):
        self.gagModel.removeNode()
        del self.gagModel
        DistributedBarrelBase.DistributedBarrelBase.delete(self)

    def applyLabel(self):
        self.gagModel = loader.loadModel('phase_4/models/props/icecream')
        self.gagModel.reparentTo(self.gagNode)
        self.gagModel.find('**/p1_2').clearBillboard()
        self.gagModel.setScale(self.gagScale)
        self.gagModel.setPos(0, -0.1, -0.1 - self.gagScale)

    def setGrab(self, avId):
        DistributedBarrelBase.DistributedBarrelBase.setGrab(self, avId)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedHealBarrel.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:40 Pacific Daylight Time
