# 2013.08.22 22:16:56 Pacific Daylight Time
# Embedded file name: toontown.building.DistributedTrophyMgr
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedTrophyMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrophyMgr')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.trophyManager != None:
            base.cr.trophyManager.delete()
        base.cr.trophyManager = self
        DistributedObject.DistributedObject.generate(self)
        return

    def disable(self):
        base.cr.trophyManager = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        base.cr.trophyManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def d_requestTrophyScore(self):
        self.sendUpdate('requestTrophyScore', [])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\building\DistributedTrophyMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:56 Pacific Daylight Time
