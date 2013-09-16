# 2013.08.22 22:14:08 Pacific Daylight Time
# Embedded file name: direct.distributed.DoHierarchy
from direct.directnotify.DirectNotifyGlobal import directNotify

class DoHierarchy():
    __module__ = __name__
    notify = directNotify.newCategory('DoHierarchy')

    def __init__(self):
        self._table = {}
        self._allDoIds = set()

    def isEmpty(self):
        return len(self._table) == 0 and len(self._allDoIds) == 0

    def __len__(self):
        return len(self._allDoIds)

    def clear(self):
        self._table = {}
        self._allDoIds = set()

    def getDoIds(self, getDo, parentId, zoneId = None, classType = None):
        parent = self._table.get(parentId)
        if parent is None:
            return []
        if zoneId is None:
            r = []
            for zone in parent.values():
                for obj in zone:
                    r.append(obj)

        else:
            r = parent.get(zoneId, [])
        if classType is not None:
            a = []
            for doId in r:
                obj = getDo(doId)
                if isinstance(obj, classType):
                    a.append(doId)

            r = a
        return r

    def storeObjectLocation(self, do, parentId, zoneId):
        doId = do.doId
        if doId in self._allDoIds:
            self.notify.error("storeObjectLocation(%s %s) already in _allDoIds; duplicate generate()? or didn't clean up previous instance of DO?" % (do.__class__.__name__, do.doId))
        parentZoneDict = self._table.setdefault(parentId, {})
        zoneDoSet = parentZoneDict.setdefault(zoneId, set())
        zoneDoSet.add(doId)
        self._allDoIds.add(doId)
        self.notify.debug('storeObjectLocation: %s(%s) @ (%s, %s)' % (do.__class__.__name__,
         doId,
         parentId,
         zoneId))

    def deleteObjectLocation(self, do, parentId, zoneId):
        doId = do.doId
        if doId not in self._allDoIds:
            self.notify.error('deleteObjectLocation(%s %s) not in _allDoIds; duplicate delete()? or invalid previous location on a new object?' % (do.__class__.__name__, do.doId))
        if doId not in self._allDoIds:
            return
        parentZoneDict = self._table.get(parentId)
        if parentZoneDict is not None:
            zoneDoSet = parentZoneDict.get(zoneId)
            if zoneDoSet is not None:
                if doId in zoneDoSet:
                    zoneDoSet.remove(doId)
                    self._allDoIds.remove(doId)
                    self.notify.debug('deleteObjectLocation: %s(%s) @ (%s, %s)' % (do.__class__.__name__,
                     doId,
                     parentId,
                     zoneId))
                    if len(zoneDoSet) == 0:
                        del parentZoneDict[zoneId]
                        if len(parentZoneDict) == 0:
                            del self._table[parentId]
                else:
                    self.notify.error('deleteObjectLocation: objId: %s not found' % doId)
            else:
                self.notify.error('deleteObjectLocation: zoneId: %s not found' % zoneId)
        else:
            self.notify.error('deleteObjectLocation: parentId: %s not found' % parentId)
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DoHierarchy.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:08 Pacific Daylight Time
