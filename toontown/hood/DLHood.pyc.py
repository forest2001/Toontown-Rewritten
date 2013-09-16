# 2013.08.22 22:20:51 Pacific Daylight Time
# Embedded file name: toontown.hood.DLHood
from pandac.PandaModules import *
import ToonHood
from toontown.town import DLTownLoader
from toontown.safezone import DLSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class DLHood(ToonHood.ToonHood):
    __module__ = __name__

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = DonaldsDreamland
        self.townLoaderClass = DLTownLoader.DLTownLoader
        self.safeZoneLoaderClass = DLSafeZoneLoader.DLSafeZoneLoader
        self.storageDNAFile = 'phase_8/dna/storage_DL.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DL.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DL.dna'],
         HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_DL.dna'],
         SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_DL.dna']}
        self.skyFile = 'phase_8/models/props/DL_sky'
        self.titleColor = (1.0, 0.9, 0.5, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('DLHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('DLHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\DLHood.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:51 Pacific Daylight Time
