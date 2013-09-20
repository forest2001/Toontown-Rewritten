# 2013.08.22 22:16:00 Pacific Daylight Time
# Embedded file name: toontown.ai.DistributedBlackCatMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.effects import DustCloud

def getDustCloudIval(toon):
    dustCloud = DustCloud.DustCloud(fBillboard=0)
    dustCloud.setBillboardAxis(2.0)
    dustCloud.setZ(3)
    dustCloud.setScale(0.4)
    dustCloud.createTrack()
    toon.laffMeter.color = toon.style.getBlackColor()
    return Sequence(Wait(0.5), Func(dustCloud.reparentTo, toon), dustCloud.track, Func(dustCloud.detachNode), Func(toon.laffMeter.adjustFace, toon.hp, toon.maxHp))


class DistributedBlackCatMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackCatMgr')
    ActivateEvent = 'DistributedBlackCatMgr-activate'

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def setAvId(self, avId):
        self.avId = avId

    def announceGenerate(self):
        DistributedBlackCatMgr.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)
        self.acceptOnce(DistributedBlackCatMgr.ActivateEvent, self.doBlackCatTransformation)
        self.dustCloudIval = None
        return

    def delete(self):
        if self.dustCloudIval:
            self.dustCloudIval.finish()
        del self.dustCloudIval
        self.ignore(DistributedBlackCatMgr.ActivateEvent)
        DistributedObject.DistributedObject.delete(self)

    def doBlackCatTransformation(self):
        DistributedBlackCatMgr.notify.debug('doBlackCatTransformation')
        toon = base.cr.doId2do[self.avId]
        if not toon:
            DistributedBlackCatMgr.notify.warning("couldn't find Toon %s" % self.avId)
            return
        if toon.style.getAnimal() != 'cat':
            DistributedBlackCatMgr.notify.warning('not a cat: %s' % self.avId)
            return
        self.sendUpdate('doBlackCatTransformation', [])
        self.dustCloudIval = getDustCloudIval(toon)
        self.dustCloudIval.start()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\DistributedBlackCatMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:00 Pacific Daylight Time
