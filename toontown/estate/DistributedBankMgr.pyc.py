# 2013.08.22 22:20:00 Pacific Daylight Time
# Embedded file name: toontown.estate.DistributedBankMgr
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedBankMgr(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBankMgr')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.bankManager != None:
            base.cr.bankManager.delete()
        base.cr.bankManager = self
        DistributedObject.DistributedObject.generate(self)
        return

    def disable(self):
        base.cr.bankManager = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        base.cr.bankManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def d_transferMoney(self, amount):
        self.sendUpdate('transferMoney', [amount])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\estate\DistributedBankMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:00 Pacific Daylight Time
