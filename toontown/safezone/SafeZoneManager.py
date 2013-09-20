# 2013.08.22 22:24:44 Pacific Daylight Time
# Embedded file name: toontown.safezone.SafeZoneManager
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class SafeZoneManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('SafeZoneManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('enterSafeZone', self.d_enterSafeZone)
        self.accept('exitSafeZone', self.d_exitSafeZone)

    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)

    def d_enterSafeZone(self):
        self.sendUpdate('enterSafeZone', [])

    def d_exitSafeZone(self):
        self.sendUpdate('exitSafeZone', [])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\SafeZoneManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:44 Pacific Daylight Time
