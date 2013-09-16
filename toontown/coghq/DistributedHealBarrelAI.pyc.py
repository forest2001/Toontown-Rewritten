# 2013.08.22 22:18:40 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedHealBarrelAI
import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

class DistributedHealBarrelAI(DistributedBarrelBaseAI.DistributedBarrelBaseAI):
    __module__ = __name__

    def __init__(self, level, entId):
        x = y = z = h = 0
        DistributedBarrelBaseAI.DistributedBarrelBaseAI.__init__(self, level, entId)

    def d_setGrab(self, avId):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do.get(avId)
        if av:
            av.toonUp(self.getRewardPerGrab())
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedHealBarrelAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:40 Pacific Daylight Time
