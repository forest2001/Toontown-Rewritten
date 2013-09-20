# 2013.08.22 22:15:11 Pacific Daylight Time
# Embedded file name: otp.avatar.PlayerBase


class PlayerBase():
    __module__ = __name__

    def __init__(self):
        self.gmState = False

    def atLocation(self, locationId):
        return True

    def getLocation(self):
        return []

    def setAsGM(self, state):
        self.gmState = state

    def isGM(self):
        return self.gmState
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\avatar\PlayerBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:11 Pacific Daylight Time
