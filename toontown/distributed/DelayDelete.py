# 2013.08.22 22:19:26 Pacific Daylight Time
# Embedded file name: toontown.distributed.DelayDelete


class DelayDelete():
    __module__ = __name__

    def __init__(self, distObj, name):
        self._distObj = distObj
        self._name = name
        self._token = self._distObj.acquireDelayDelete(name)

    def getObject(self):
        return self._distObj

    def getName(self):
        return self._name

    def destroy(self):
        token = self._token
        del self._token
        self._distObj.releaseDelayDelete(token)
        del self._distObj
        del self._name


def cleanupDelayDeletes(interval):
    if hasattr(interval, 'delayDelete'):
        delayDelete = interval.delayDelete
        del interval.delayDelete
        if type(delayDelete) == type([]):
            for i in delayDelete:
                i.destroy()

        else:
            delayDelete.destroy()
    if hasattr(interval, 'delayDeletes'):
        delayDeletes = interval.delayDeletes
        del interval.delayDeletes
        if type(delayDeletes) == type([]):
            for i in delayDeletes:
                i.destroy()

        else:
            delayDeletes.destroy()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\distributed\DelayDelete.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:26 Pacific Daylight Time
