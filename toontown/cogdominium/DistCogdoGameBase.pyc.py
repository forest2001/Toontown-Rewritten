# 2013.08.22 22:17:59 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.DistCogdoGameBase


class DistCogdoGameBase():
    __module__ = __name__

    def local2GameTime(self, timestamp):
        return timestamp - self._startTime

    def game2LocalTime(self, timestamp):
        return timestamp + self._startTime

    def getCurrentGameTime(self):
        return self.local2GameTime(globalClock.getFrameTime())
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\DistCogdoGameBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:59 Pacific Daylight Time
