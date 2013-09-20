# 2013.08.22 22:19:30 Pacific Daylight Time
# Embedded file name: toontown.distributed.ToontownDistrict
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.distributed import DistributedDistrict

class ToontownDistrict(DistributedDistrict.DistributedDistrict):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownDistrict')

    def __init__(self, cr):
        DistributedDistrict.DistributedDistrict.__init__(self, cr)
        self.avatarCount = 0
        self.newAvatarCount = 0

    def allowAHNNLog(self, allow):
        self.allowAHNN = allow

    def getAllowAHNNLog(self):
        return self.allowAHNN
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\distributed\ToontownDistrict.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:30 Pacific Daylight Time
