# 2013.08.22 22:19:26 Pacific Daylight Time
# Embedded file name: toontown.distributed.DelayDeletable
from direct.distributed.DistributedObject import ESGenerating, ESGenerated, ESNum2Str

class DelayDeletable():
    __module__ = __name__
    DelayDeleteSerialGen = SerialNumGen()

    def delayDelete(self):
        pass

    def acquireDelayDelete(self, name):
        global ESGenerating
        global ESGenerated
        if not self._delayDeleteForceAllow and self.activeState not in (ESGenerating, ESGenerated):
            self.notify.error('cannot acquire DelayDelete "%s" on %s because it is in state %s' % (name, self.__class__.__name__, ESNum2Str[self.activeState]))
        if self.getDelayDeleteCount() == 0:
            self.cr._addDelayDeletedDO(self)
        token = DelayDeletable.DelayDeleteSerialGen.next()
        self._token2delayDeleteName[token] = name
        return token

    def releaseDelayDelete(self, token):
        name = self._token2delayDeleteName.pop(token)
        if len(self._token2delayDeleteName) == 0:
            self.cr._removeDelayDeletedDO(self)
            if self._delayDeleted:
                self.disableAnnounceAndDelete()

    def getDelayDeleteNames(self):
        return self._token2delayDeleteName.values()

    def forceAllowDelayDelete(self):
        self._delayDeleteForceAllow = True
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\distributed\DelayDeletable.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:26 Pacific Daylight Time
