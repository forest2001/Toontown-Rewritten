# 2013.08.22 22:20:50 Pacific Daylight Time
# Embedded file name: toontown.hood.BRHood
from pandac.PandaModules import *
import ToonHood
from toontown.town import BRTownLoader
from toontown.safezone import BRSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class BRHood(ToonHood.ToonHood):
    __module__ = __name__

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = TheBrrrgh
        self.townLoaderClass = BRTownLoader.BRTownLoader
        self.safeZoneLoaderClass = BRSafeZoneLoader.BRSafeZoneLoader
        self.storageDNAFile = 'phase_8/dna/storage_BR.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_8/dna/winter_storage_BR.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_BR.dna'],
         HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_BR.dna'],
         SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_BR.dna']}
        self.skyFile = 'phase_3.5/models/props/BR_sky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (0.3, 0.6, 1.0, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('BRHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('BRHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\BRHood.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:50 Pacific Daylight Time
