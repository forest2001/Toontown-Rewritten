# 2013.08.22 22:15:35 Pacific Daylight Time
# Embedded file name: otp.level.ZoneEntityBase
import Entity
import LevelConstants

class ZoneEntityBase(Entity.Entity):
    __module__ = __name__

    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)
        self.zoneId = None
        return

    def destroy(self):
        del self.zoneId
        Entity.Entity.destroy(self)

    def isUberZone(self):
        return self.entId == LevelConstants.UberZoneEntId

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def getZoneId(self):
        return self.zoneId

    def getZoneNum(self):
        return self.entId
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\ZoneEntityBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:35 Pacific Daylight Time
