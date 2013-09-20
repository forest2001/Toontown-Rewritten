# 2013.08.22 22:26:53 Pacific Daylight Time
# Embedded file name: toontown.town.TTTownLoader
import TownLoader
import TTStreet
from toontown.suit import Suit

class TTTownLoader(TownLoader.TownLoader):
    __module__ = __name__

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = TTStreet.TTStreet
        self.musicFile = 'phase_3.5/audio/bgm/TC_SZ.mid'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        self.townStorageDNAFile = 'phase_5/dna/storage_TT_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(1)
        dnaFile = 'phase_5/dna/toontown_central_' + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(1)
        TownLoader.TownLoader.unload(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\town\TTTownLoader.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:53 Pacific Daylight Time
