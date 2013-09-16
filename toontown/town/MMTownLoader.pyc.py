# 2013.08.22 22:26:48 Pacific Daylight Time
# Embedded file name: toontown.town.MMTownLoader
import TownLoader
import MMStreet
from toontown.suit import Suit

class MMTownLoader(TownLoader.TownLoader):
    __module__ = __name__

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = MMStreet.MMStreet
        self.musicFile = 'phase_6/audio/bgm/MM_SZ.mid'
        self.activityMusicFile = 'phase_6/audio/bgm/MM_SZ_activity.mid'
        self.townStorageDNAFile = 'phase_6/dna/storage_MM_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(2)
        dnaFile = 'phase_6/dna/minnies_melody_land_' + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(2)
        TownLoader.TownLoader.unload(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\town\MMTownLoader.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:48 Pacific Daylight Time
