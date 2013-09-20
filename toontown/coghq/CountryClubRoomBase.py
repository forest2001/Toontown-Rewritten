# 2013.08.22 22:18:23 Pacific Daylight Time
# Embedded file name: toontown.coghq.CountryClubRoomBase
from toontown.toonbase import ToontownGlobals

class CountryClubRoomBase():
    __module__ = __name__

    def __init__(self):
        pass

    def setCountryClubId(self, countryClubId):
        self.countryClubId = countryClubId
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(countryClubId)

    def setRoomId(self, roomId):
        self.roomId = roomId

    def getCogTrack(self):
        return self.cogTrack

    if __dev__:

        def getCountryClubEntityTypeReg(self):
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\CountryClubRoomBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:23 Pacific Daylight Time
