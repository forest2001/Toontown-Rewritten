# 2013.08.22 22:14:05 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedObjectBase
from direct.showbase.DirectObject import DirectObject

class DistributedObjectBase(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObjectBase')

    def __init__(self, cr):
        self.cr = cr
        self.children = {}
        self.parentId = None
        self.zoneId = None
        return

    def getLocation(self):
        try:
            if self.parentId == 0 and self.zoneId == 0:
                return None
            if self.parentId == 4294967295L and self.zoneId == 4294967295L:
                return None
            return (self.parentId, self.zoneId)
        except AttributeError:
            return None

        return None

    def handleChildArrive(self, childObj, zoneId):
        pass

    def handleChildArriveZone(self, childObj, zoneId):
        pass

    def handleChildLeave(self, childObj, zoneId):
        pass

    def handleChildLeaveZone(self, childObj, zoneId):
        pass

    def handleQueryObjectChildrenLocalDone(self, context):
        pass

    def getParentObj(self):
        if self.parentId is None:
            return
        return self.cr.doId2do.get(self.parentId)

    def hasParentingRules(self):
        return self.dclass.getFieldByName('setParentingRules') != None
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedObjectBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:05 Pacific Daylight Time
