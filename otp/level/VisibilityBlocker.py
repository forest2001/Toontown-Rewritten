# 2013.08.22 22:15:35 Pacific Daylight Time
# Embedded file name: otp.level.VisibilityBlocker
import Entity

class VisibilityBlocker():
    __module__ = __name__

    def __init__(self):
        self.__nextSetZoneDoneEvent = None
        return

    def destroy(self):
        self.cancelUnblockVis()

    def requestUnblockVis(self):
        if self.__nextSetZoneDoneEvent is None:
            self.__nextSetZoneDoneEvent = self.level.cr.getNextSetZoneDoneEvent()
            self.acceptOnce(self.__nextSetZoneDoneEvent, self.okToUnblockVis)
            self.level.forceSetZoneThisFrame()
        return

    def cancelUnblockVis(self):
        if self.__nextSetZoneDoneEvent is not None:
            self.ignore(self.__nextSetZoneDoneEvent)
            self.__nextSetZoneDoneEvent = None
        return

    def isWaitingForUnblockVis(self):
        return self.__nextSetZoneDoneEvent is not None

    def okToUnblockVis(self):
        self.cancelUnblockVis()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\VisibilityBlocker.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:35 Pacific Daylight Time
