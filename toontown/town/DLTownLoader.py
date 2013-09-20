# 2013.08.22 22:26:48 Pacific Daylight Time
# Embedded file name: toontown.town.DLTownLoader
import TownLoader
import DLStreet
from toontown.suit import Suit

class DLTownLoader(TownLoader.TownLoader):
    __module__ = __name__

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DLStreet.DLStreet
        self.musicFile = 'phase_8/audio/bgm/DL_SZ.mid'
        self.activityMusicFile = 'phase_8/audio/bgm/DL_SZ_activity.mid'
        self.townStorageDNAFile = 'phase_8/dna/storage_DL_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(3)
        dnaFile = 'phase_8/dna/donalds_dreamland_' + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(3)
        TownLoader.TownLoader.unload(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\town\DLTownLoader.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:48 Pacific Daylight Time
