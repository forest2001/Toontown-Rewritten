# 2013.08.22 22:20:55 Pacific Daylight Time
# Embedded file name: toontown.hood.LawbotHQ
import CogHood
from toontown.toonbase import ToontownGlobals
from toontown.coghq import LawbotCogHQLoader

class LawbotHQ(CogHood.CogHood):
    __module__ = __name__

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        CogHood.CogHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.LawbotHQ
        self.cogHQLoaderClass = LawbotCogHQLoader.LawbotCogHQLoader
        self.storageDNAFile = None
        self.skyFile = 'phase_9/models/cogHQ/cog_sky'
        self.titleColor = (0.5, 0.5, 0.5, 1.0)
        return

    def load(self):
        CogHood.CogHood.load(self)
        self.sky.hide()
        self.parentFSM.getStateNamed('LawbotHQ').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('LawbotHQ').removeChild(self.fsm)
        del self.cogHQLoaderClass
        CogHood.CogHood.unload(self)

    def enter(self, *args):
        CogHood.CogHood.enter(self, *args)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.LawbotHQCameraNear, ToontownGlobals.LawbotHQCameraFar)

    def exit(self):
        localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        CogHood.CogHood.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\LawbotHQ.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:55 Pacific Daylight Time
