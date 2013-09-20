# 2013.08.22 22:21:02 Pacific Daylight Time
# Embedded file name: toontown.launcher.ToontownDownloadWatcher
from direct.directnotify import DirectNotifyGlobal
from otp.launcher.DownloadWatcher import DownloadWatcher
from toontown.toonbase import TTLocalizer

class ToontownDownloadWatcher(DownloadWatcher):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownDownloadWatcher')

    def __init__(self, phaseNames):
        DownloadWatcher.__init__(self, phaseNames)

    def update(self, phase, percent, reqByteRate, actualByteRate):
        DownloadWatcher.update(self, phase, percent, reqByteRate, actualByteRate)
        phaseName = self.phaseNames[phase]
        self.text['text'] = TTLocalizer.LoadingDownloadWatcherUpdate % phaseName
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\launcher\ToontownDownloadWatcher.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:02 Pacific Daylight Time
