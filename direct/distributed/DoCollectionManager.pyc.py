# 2013.08.22 22:14:07 Pacific Daylight Time
# Embedded file name: direct.distributed.DoCollectionManager
from direct.distributed import DoHierarchy
import re
BAD_DO_ID = BAD_ZONE_ID = 0
BAD_CHANNEL_ID = 0

class DoCollectionManager():
    __module__ = __name__

    def __init__(self):
        self.doId2do = {}
        if self.hasOwnerView():
            self.doId2ownerView = {}
        self._doHierarchy = DoHierarchy.DoHierarchy()

    def getDo(self, doId):
        return self.doId2do.get(doId)

    def getGameDoId(self):
        return self.GameGlobalsId

    def callbackWithDo(self, doId, callback):
        do = self.doId2do.get(doId)
        if do is not None:
            callback(do)
        else:
            relatedObjectMgr(doId, allCallback=callback)
        return

    def getOwnerView(self, doId):
        return self.doId2ownerView.get(doId)

    def callbackWithOwnerView(self, doId, callback):
        do = self.doId2ownerView.get(doId)
        if do is not None:
            callback(do)
        return

    def getDoTable(self, ownerView):
        if ownerView:
            return self.doId2ownerView
        else:
            return self.doId2do

    def doFind(self, str):
        for value in self.doId2do.values():
            if repr(value).find(str) >= 0:
                return value

    def doFindAll(self, str):
        matches = []
        for value in self.doId2do.values():
            if repr(value).find(str) >= 0:
                matches.append(value)

        return matches

    def doFindAllMatching(self, str):
        matches = []
        for value in self.doId2do.values():
            if re.search(str, repr(value)):
                matches.append(value)

        return matches

    def doFindAllOfType(self, query):
        matches = []
        for value in self.doId2do.values():
            if query in str(value.__class__):
                matches.append(value)

        return (matches, len(matches))

    def doFindAllInstances(self, cls):
        matches = []
        for value in self.doId2do.values():
            if isinstance(value, cls):
                matches.append(value)

        return matches

    def _getDistanceFromLA(self, do):
        if hasattr(do, 'getPos'):
            return do.getPos(localAvatar).length()
        return None

    def _compareDistance(self, do1, do2):
        dist1 = self._getDistanceFromLA(do1)
        dist2 = self._getDistanceFromLA(do2)
        if dist1 is None and dist2 is None:
            return 0
        if dist1 is None:
            return 1
        if dist2 is None:
            return -1
        if dist1 < dist2:
            return -1
        return 1

    def dosByDistance(self):
        objs = self.doId2do.values()
        objs.sort(cmp=self._compareDistance)
        return objs

    def doByDistance(self):
        objs = self.dosByDistance()
        for obj in objs:
            print '%s\t%s\t%s' % (obj.doId, self._getDistanceFromLA(obj), obj.dclass.getName())

    def _printObjects(self, table):
        class2count = {}
        for obj in self.getDoTable(ownerView=False).values():
            className = obj.__class__.__name__
            class2count.setdefault(className, 0)
            class2count[className] += 1

        count2classes = invertDictLossless(class2count)
        counts = count2classes.keys()
        counts.sort()
        counts.reverse()
        for count in counts:
            count2classes[count].sort()
            for name in count2classes[count]:
                print '%s %s' % (count, name)

        print ''

    def _returnObjects(self, table):
        class2count = {}
        stringToReturn = ''
        for obj in self.getDoTable(ownerView=False).values():
            className = obj.__class__.__name__
            class2count.setdefault(className, 0)
            class2count[className] += 1

        count2classes = invertDictLossless(class2count)
        counts = count2classes.keys()
        counts.sort()
        counts.reverse()
        for count in counts:
            count2classes[count].sort()
            for name in count2classes[count]:
                stringToReturn = '%s%s %s\n' % (stringToReturn, count, name)

        return stringToReturn

    def webPrintObjectCount(self):
        strToReturn = '==== OBJECT COUNT ====\n'
        if self.hasOwnerView():
            strToReturn = '%s == doId2do\n' % strToReturn
        strToReturn = '%s%s' % (strToReturn, self._returnObjects(self.getDoTable(ownerView=False)))
        if self.hasOwnerView():
            strToReturn = '%s\n== doId2ownerView\n' % strToReturn
            strToReturn = '%s%s' % (strToReturn, self._returnObjects(self.getDoTable(ownerView=False)))
        return strToReturn

    def printObjectCount(self):
        print '==== OBJECT COUNT ===='
        if self.hasOwnerView():
            print '== doId2do'
        self._printObjects(self.getDoTable(ownerView=False))
        if self.hasOwnerView():
            print '== doId2ownerView'
            self._printObjects(self.getDoTable(ownerView=True))

    def getDoList(self, parentId, zoneId = None, classType = None):
        return [ self.doId2do.get(i) for i in self.getDoIdList(parentId, zoneId, classType) ]

    def getDoIdList(self, parentId, zoneId = None, classType = None):
        return self._doHierarchy.getDoIds(self.getDo, parentId, zoneId, classType)

    def hasOwnerViewDoId(self, doId):
        return doId in self.doId2ownerView

    def getOwnerViewDoList(self, classType):
        l = []
        for obj in self.doId2ownerView.values():
            if isinstance(obj, classType):
                l.append(obj)

        return l

    def getOwnerViewDoIdList(self, classType):
        l = []
        for doId, obj in self.doId2ownerView.items():
            if isinstance(obj, classType):
                l.append(doId)

        return l

    def countObjects(self, classType):
        count = 0
        for dobj in self.doId2do.values():
            if isinstance(dobj, classType):
                count += 1

        return count

    def getAllOfType(self, type):
        result = []
        for obj in self.doId2do.values():
            if isinstance(obj, type):
                result.append(obj)

        return result

    def findAnyOfType(self, type):
        for obj in self.doId2do.values():
            if isinstance(obj, type):
                return obj

        return None

    def deleteDistributedObjects(self):
        for doId in self.doId2do.keys():
            do = self.doId2do[doId]
            self.deleteDistObject(do)

        self.deleteObjects()
        if not self._doHierarchy.isEmpty():
            self.notify.warning('_doHierarchy table not empty: %s' % self._doHierarchy)
            self._doHierarchy.clear()

    def handleObjectLocation(self, di):
        doId = di.getUint32()
        parentId = di.getUint32()
        zoneId = di.getUint32()
        obj = self.doId2do.get(doId)
        if obj is not None:
            self.notify.debug('handleObjectLocation: doId: %s parentId: %s zoneId: %s' % (doId, parentId, zoneId))
            obj.setLocation(parentId, zoneId)
        else:
            self.notify.warning('handleObjectLocation: Asked to update non-existent obj: %s' % doId)
        return

    def handleSetLocation(self, di):
        parentId = di.getUint32()
        zoneId = di.getUint32()
        distObj = self.doId2do.get(self.getMsgChannel())
        if distObj is not None:
            distObj.setLocation(parentId, zoneId)
        else:
            self.notify.warning('handleSetLocation: object %s not present' % self.getMsgChannel())
        return

    @exceptionLogged()
    def storeObjectLocation(self, object, parentId, zoneId):
        oldParentId = object.parentId
        oldZoneId = object.zoneId
        if oldParentId != parentId:
            oldParentObj = self.doId2do.get(oldParentId)
            if oldParentObj is not None:
                oldParentObj.handleChildLeave(object, oldZoneId)
            self.deleteObjectLocation(object, oldParentId, oldZoneId)
        elif oldZoneId != zoneId:
            oldParentObj = self.doId2do.get(oldParentId)
            if oldParentObj is not None:
                oldParentObj.handleChildLeaveZone(object, oldZoneId)
            self.deleteObjectLocation(object, oldParentId, oldZoneId)
        else:
            return
        if parentId is None or zoneId is None or parentId == zoneId == 0:
            object.parentId = None
            object.zoneId = None
        else:
            self._doHierarchy.storeObjectLocation(object, parentId, zoneId)
            object.parentId = parentId
            object.zoneId = zoneId
        if oldParentId != parentId:
            parentObj = self.doId2do.get(parentId)
            if parentObj is not None:
                parentObj.handleChildArrive(object, zoneId)
            elif parentId not in (None, 0, self.getGameDoId()):
                self.notify.warning('storeObjectLocation(%s): parent %s not present' % (object.doId, parentId))
        elif oldZoneId != zoneId:
            parentObj = self.doId2do.get(parentId)
            if parentObj is not None:
                parentObj.handleChildArriveZone(object, zoneId)
            elif parentId not in (None, 0, self.getGameDoId()):
                self.notify.warning('storeObjectLocation(%s): parent %s not present' % (object.doId, parentId))
        return

    def deleteObjectLocation(self, object, parentId, zoneId):
        if parentId is None or zoneId is None or parentId == zoneId == 0:
            return
        self._doHierarchy.deleteObjectLocation(object, parentId, zoneId)
        return

    def addDOToTables(self, do, location = None, ownerView = False):
        if not ownerView:
            if location is None:
                location = (do.parentId, do.zoneId)
        doTable = self.getDoTable(ownerView)
        if do.doId in doTable:
            if ownerView:
                tableName = 'doId2ownerView'
            else:
                tableName = 'doId2do'
            self.notify.error('doId %s already in %s [%s stomping %s]' % (do.doId,
             tableName,
             do.__class__.__name__,
             doTable[do.doId].__class__.__name__))
        doTable[do.doId] = do
        if not ownerView:
            if self.isValidLocationTuple(location):
                self.storeObjectLocation(do, location[0], location[1])
        return

    def isValidLocationTuple(self, location):
        return location is not None and location != (4294967295L, 4294967295L) and location != (0, 0)

    def removeDOFromTables(self, do):
        location = do.getLocation()
        if location:
            oldParentId, oldZoneId = location
            oldParentObj = self.doId2do.get(oldParentId)
            if oldParentObj:
                oldParentObj.handleChildLeave(do, oldZoneId)
        self.deleteObjectLocation(do, do.parentId, do.zoneId)
        if do.doId in self.doId2do:
            del self.doId2do[do.doId]

    def getObjectsInZone(self, parentId, zoneId):
        doDict = {}
        for doId in self.getDoIdList(parentId, zoneId):
            doDict[doId] = self.getDo(doId)

        return doDict

    def getObjectsOfClassInZone(self, parentId, zoneId, objClass):
        doDict = {}
        for doId in self.getDoIdList(parentId, zoneId, objClass):
            doDict[doId] = self.getDo(doId)

        return doDict
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DoCollectionManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:08 Pacific Daylight Time
