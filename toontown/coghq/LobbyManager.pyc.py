# 2013.08.22 22:19:16 Pacific Daylight Time
# Embedded file name: toontown.coghq.LobbyManager
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class LobbyManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LobbyManager')
    SetFactoryZoneMsg = 'setFactoryZone'

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        self.notify.debug('generate')
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        self.notify.debug('disable')
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)

    def getSuitDoorOrigin(self):
        return 1

    def getBossLevel(self):
        return 0
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\LobbyManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:16 Pacific Daylight Time
