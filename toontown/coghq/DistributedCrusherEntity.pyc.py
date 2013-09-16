# 2013.08.22 22:18:33 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedCrusherEntity
from otp.level import BasicEntities
from direct.directnotify import DirectNotifyGlobal

class DistributedCrusherEntity(BasicEntities.DistributedNodePathEntity):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrusherEntity')

    def __init__(self, cr):
        BasicEntities.DistributedNodePathEntity.__init__(self, cr)

    def announceGenerate(self):
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)
        self.crushMsg = self.getUniqueName('crushMsg')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedCrusherEntity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:33 Pacific Daylight Time
