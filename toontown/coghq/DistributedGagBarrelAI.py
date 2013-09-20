# 2013.08.22 22:18:36 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedGagBarrelAI
from toontown.toonbase.ToontownBattleGlobals import *
import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

class DistributedGagBarrelAI(DistributedBarrelBaseAI.DistributedBarrelBaseAI):
    __module__ = __name__

    def __init__(self, level, entId):
        x = y = z = h = 0
        self.gagLevelMax = 0
        DistributedBarrelBaseAI.DistributedBarrelBaseAI.__init__(self, level, entId)

    def d_setGrab(self, avId):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do.get(avId)
        if av:
            if not av.hasTrackAccess(self.getGagTrack()):
                return
            track = self.getGagTrack()
            level = self.getGagLevel()
            maxGags = av.getMaxCarry()
            av.inventory.calcTotalProps()
            numGags = av.inventory.totalProps
            numReward = min(self.getRewardPerGrab(), maxGags - numGags)
            while numReward > 0 and level >= 0:
                result = av.inventory.addItem(track, level)
                if result <= 0:
                    level -= 1
                else:
                    numReward -= 1

            av.d_setInventory(av.inventory.makeNetString())
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedGagBarrelAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:36 Pacific Daylight Time
