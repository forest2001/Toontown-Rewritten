# 2013.08.22 22:24:41 Pacific Daylight Time
# Embedded file name: toontown.safezone.MMSafeZoneLoader
from pandac.PandaModules import *
import SafeZoneLoader
import MMPlayground
from toontown.toonbase import ToontownGlobals

class MMSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    __module__ = __name__

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = MMPlayground.MMPlayground
        self.musicFile = 'phase_6/audio/bgm/MM_nbrhood.mid'
        self.activityMusicFile = 'phase_6/audio/bgm/MM_SZ_activity.mid'
        self.dnaFile = 'phase_6/dna/minnies_melody_land_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_MM_sz.dna'

    def load(self):
        print 'loading MM safezone'
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.piano = self.geom.find('**/center_icon')
        if self.piano.isEmpty():
            self.notify.error('Piano not found')
        else:
            hq = self.geom.find('**/*toon_landmark_hqMM_DNARoot')
            hq.wrtReparentTo(self.piano)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.piano
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\MMSafeZoneLoader.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:41 Pacific Daylight Time
