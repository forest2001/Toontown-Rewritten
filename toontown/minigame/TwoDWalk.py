# 2013.08.22 22:23:08 Pacific Daylight Time
# Embedded file name: toontown.minigame.TwoDWalk
from OrthoWalk import *

class TwoDWalk(OrthoWalk):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDWalk')
    BROADCAST_POS_TASK = 'TwoDWalkBroadcastPos'

    def doBroadcast(self, task):
        dt = globalClock.getDt()
        self.timeSinceLastPosBroadcast += dt
        if self.timeSinceLastPosBroadcast >= self.broadcastPeriod:
            self.timeSinceLastPosBroadcast = 0
            self.lt.cnode.broadcastPosHprFull()
        return Task.cont
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\TwoDWalk.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:08 Pacific Daylight Time
