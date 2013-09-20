# 2013.08.22 22:24:38 Pacific Daylight Time
# Embedded file name: toontown.safezone.DLSafeZoneLoader
from pandac.PandaModules import *
import SafeZoneLoader
import DLPlayground

class DLSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    __module__ = __name__

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = DLPlayground.DLPlayground
        self.musicFile = 'phase_8/audio/bgm/DL_nbrhood.mid'
        self.activityMusicFile = 'phase_8/audio/bgm/DL_SZ_activity.mid'
        self.dnaFile = 'phase_8/dna/donalds_dreamland_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_8/dna/storage_DL_sz.dna'
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\DLSafeZoneLoader.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:38 Pacific Daylight Time
