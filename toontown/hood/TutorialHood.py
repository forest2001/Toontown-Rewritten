# 2013.08.22 22:21:00 Pacific Daylight Time
# Embedded file name: toontown.hood.TutorialHood
from pandac.PandaModules import *
import ToonHood
from toontown.town import TutorialTownLoader
from toontown.toonbase.ToontownGlobals import *
import SkyUtil

class TutorialHood(ToonHood.ToonHood):
    __module__ = __name__

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = Tutorial
        self.townLoaderClass = TutorialTownLoader.TutorialTownLoader
        self.safeZoneLoaderClass = None
        self.storageDNAFile = None
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.titleColor = (1.0, 0.5, 0.4, 1.0)
        return

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('TutorialHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('TutorialHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\TutorialHood.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:00 Pacific Daylight Time
