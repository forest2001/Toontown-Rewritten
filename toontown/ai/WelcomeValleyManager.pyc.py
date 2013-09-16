# 2013.08.22 22:16:07 Pacific Daylight Time
# Embedded file name: toontown.ai.WelcomeValleyManager
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from direct.showbase import PythonUtil

class WelcomeValleyManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('WelcomeValleyManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.welcomeValleyManager != None:
            base.cr.welcomeValleyManager.delete()
        base.cr.welcomeValleyManager = self
        DistributedObject.DistributedObject.generate(self)
        return

    def disable(self):
        self.ignore(ToontownGlobals.SynchronizeHotkey)
        base.cr.welcomeValleyManager = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        self.ignore(ToontownGlobals.SynchronizeHotkey)
        base.cr.welcomeValleyManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def requestZoneId(self, origZoneId, callback):
        context = self.getCallbackContext(callback)
        self.sendUpdate('requestZoneIdMessage', [origZoneId, context])

    def requestZoneIdResponse(self, zoneId, context):
        self.doCallbackContext(context, [zoneId])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\WelcomeValleyManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:07 Pacific Daylight Time
