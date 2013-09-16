# 2013.08.22 22:15:33 Pacific Daylight Time
# Embedded file name: otp.level.LevelMgrBase
import Entity

class LevelMgrBase(Entity.Entity):
    __module__ = __name__

    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)

    def destroy(self):
        Entity.Entity.destroy(self)
        self.ignoreAll()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\LevelMgrBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:33 Pacific Daylight Time
