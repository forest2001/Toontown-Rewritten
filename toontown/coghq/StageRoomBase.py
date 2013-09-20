# 2013.08.22 22:19:26 Pacific Daylight Time
# Embedded file name: toontown.coghq.StageRoomBase
from toontown.toonbase import ToontownGlobals

class StageRoomBase():
    __module__ = __name__

    def __init__(self):
        pass

    def setStageId(self, stageId):
        self.stageId = stageId
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(stageId)

    def setRoomId(self, roomId):
        self.roomId = roomId

    def getCogTrack(self):
        return self.cogTrack

    if __dev__:

        def getEntityTypeReg(self):
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\StageRoomBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:26 Pacific Daylight Time
