# 2013.08.22 22:15:16 Pacific Daylight Time
# Embedded file name: otp.distributed.DistributedDistrict
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject

class DistributedDistrict(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedDistrict')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.name = 'NotGiven'
        self.available = 0
        self.avatarCount = 0
        self.newAvatarCount = 0

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.cr.activeDistrictMap[self.doId] = self
        messenger.send('shardInfoUpdated')

    def delete(self):
        if base.cr.distributedDistrict is self:
            base.cr.distributedDistrict = None
        if self.cr.activeDistrictMap.has_key(self.doId):
            del self.cr.activeDistrictMap[self.doId]
        DistributedObject.delete(self)
        messenger.send('shardInfoUpdated')
        return

    def setAvailable(self, available):
        self.available = available
        messenger.send('shardInfoUpdated')

    def setName(self, name):
        self.name = name
        messenger.send('shardInfoUpdated')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\distributed\DistributedDistrict.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:16 Pacific Daylight Time
