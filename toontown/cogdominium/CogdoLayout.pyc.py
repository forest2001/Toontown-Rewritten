# 2013.08.22 22:17:45 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.CogdoLayout
from direct.directnotify import DirectNotifyGlobal

class CogdoLayout():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CogdoLayout')

    def __init__(self, numFloors):
        self._numFloors = numFloors

    def getNumGameFloors(self):
        return self._numFloors

    def hasBossBattle(self):
        return self._numFloors >= 1

    def getNumFloors(self):
        if self.hasBossBattle():
            return self._numFloors + 1
        else:
            return self._numFloors

    def getBossBattleFloor(self):
        if not self.hasBossBattle():
            self.notify.error('getBossBattleFloor(): cogdo has no boss battle')
        return self.getNumFloors() - 1
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\CogdoLayout.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:45 Pacific Daylight Time
