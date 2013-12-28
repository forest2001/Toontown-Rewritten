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
    if getattr(toon, 'laffMeter', None):
        toon.laffMeter.color = toon.style.getWhiteColor()
    seq = Sequence(Wait(0.5), Func(dustCloud.reparentTo, toon), dustCloud.track, Func(dustCloud.destroy))
    seq.append(Func(messenger.send, 'polarbear-transformed'))
    if getattr(toon, 'laffMeter', None):
        seq.append(Func(toon.laffMeter.adjustFace, toon.hp, toon.maxHp))
    return seq
    
class DistributedPolarBearMgr(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPolarBearMgr')
    ActivateEvent = 'DistributedPolarBearMgr-activate'
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        
    def announceGenerate(self):
        DistributedPolarBearMgr.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)
        self.acceptOnce(DistributedPolarBearMgr.ActivateEvent, self.d_requestPolarBearTransformation)
        self.dustCloudIval = None
        return
        
    def delete(self):
        if self.dustCloudIval:
            self.dustCloudIval.finish()
        del self.dustCloudIval
        self.ignore(DistributedPolarBearMgr.ActivateEvent)
        DistributedObject.DistributedObject.delete(self)
        
    def d_requestPolarBearTransformation(self):
        self.sendUpdate('requestPolarBearTransformation', [])
        
    def doPolarBearTransformation(self, avId):
        DistributedPolarBearMgr.notify.debug('doPolarBearTransformation')
        toon = self.cr.doId2do.get(avId)
        if not toon:
            DistributedPolarBearMgr.notify.warning("couldn't find Toon %s" % avId)
            return
        if toon.style.getAnimal() != 'bear':
            DistributedPolarBearMgr.notify.warning('not a bear: %s' % avId)
            return
        self.dustCloudIval = getDustCloudIval(toon)
        self.dustCloudIval.start()
