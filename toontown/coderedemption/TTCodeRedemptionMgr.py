# 2013.08.22 22:17:31 Pacific Daylight Time
# Embedded file name: toontown.coderedemption.TTCodeRedemptionMgr
from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify

class TTCodeRedemptionMgr(DistributedObject):
    __module__ = __name__
    neverDisable = 1
    notify = directNotify.newCategory('TTCodeRedemptionMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        base.codeRedemptionMgr = self
        self._contextGen = SerialMaskedGen(4294967295L)
        self._context2callback = {}

    def delete(self):
        if hasattr(base, 'codeRedemptionMgr'):
            if base.codeRedemptionMgr is self:
                del base.codeRedemptionMgr
        self._context2callback = None
        self._contextGen = None
        DistributedObject.delete(self)
        return

    def redeemCode(self, code, callback):
        context = self._contextGen.next()
        self._context2callback[context] = callback
        self.notify.debug('redeemCode(%s, %s)' % (context, code))
        self.sendUpdate('redeemCode', [context, code])

    def redeemCodeResult(self, context, result, awardMgrResult):
        self.notify.debug('redeemCodeResult(%s, %s, %s)' % (context, result, awardMgrResult))
        callback = self._context2callback.pop(context)
        callback(result, awardMgrResult)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coderedemption\TTCodeRedemptionMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:31 Pacific Daylight Time
