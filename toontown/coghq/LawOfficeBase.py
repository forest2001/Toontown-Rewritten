# 2013.08.22 22:19:16 Pacific Daylight Time
# Embedded file name: toontown.coghq.LawOfficeBase
import FactorySpecs
from otp.level import LevelSpec
from toontown.toonbase import ToontownGlobals

class LawOfficeBase():
    __module__ = __name__

    def __init__(self):
        pass

    def setLawOfficeId(self, factoryId):
        self.lawOfficeId = factoryId
        self.factoryType = ToontownGlobals.factoryId2factoryType[factoryId]
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(factoryId)

    def getCogTrack(self):
        return self.cogTrack

    def getFactoryType(self):
        return self.factoryType

    if __dev__:

        def getEntityTypeReg(self):
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\LawOfficeBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:16 Pacific Daylight Time
