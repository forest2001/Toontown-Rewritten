# 2013.08.22 22:19:03 Pacific Daylight Time
# Embedded file name: toontown.coghq.GoonClipPlane
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.level import BasicEntities

class GoonClipPlane(BasicEntities.NodePathEntity):
    __module__ = __name__

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.zoneNum = self.getZoneEntity().getZoneNum()
        self.initPlane()
        self.registerWithFactory()

    def destroy(self):
        self.unregisterWithFactory()
        BasicEntities.NodePathEntity.destroy(self)
        self.removeNode()

    def registerWithFactory(self):
        clipList = self.level.goonClipPlanes.get(self.zoneNum)
        if clipList:
            if self.entId not in clipList:
                clipList.append(self.entId)
        else:
            self.level.goonClipPlanes[self.zoneNum] = [self.entId]

    def unregisterWithFactory(self):
        clipList = self.level.goonClipPlanes.get(self.zoneNum)
        if clipList:
            if self.entId in clipList:
                clipList.remove(self.entId)

    def initPlane(self):
        self.coneClip = PlaneNode('coneClip')
        self.coneClip.setPlane(Plane(Vec3(1, 0, 0), Point3(0, 0, 0)))
        self.coneClipPath = self.attachNewNode(self.coneClip)

    def getPlane(self):
        return self.coneClipPath
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\GoonClipPlane.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:03 Pacific Daylight Time
