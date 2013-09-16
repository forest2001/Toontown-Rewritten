# 2013.08.22 22:26:23 Pacific Daylight Time
# Embedded file name: toontown.toon.ToonDetail
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.avatar import AvatarDetail
from toontown.toon import DistributedToon

class ToonDetail(AvatarDetail.AvatarDetail):
    __module__ = __name__
    notify = directNotify.newCategory('ToonDetail')

    def getDClass(self):
        return 'DistributedToon'

    def createHolder(self):
        toon = DistributedToon.DistributedToon(base.cr, bFake=True)
        toon.forceAllowDelayDelete()
        return toon
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\toon\ToonDetail.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:23 Pacific Daylight Time
