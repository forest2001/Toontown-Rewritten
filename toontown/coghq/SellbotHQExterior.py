# 2013.08.22 22:19:20 Pacific Daylight Time
# Embedded file name: toontown.coghq.SellbotHQExterior
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQExterior

class SellbotHQExterior(CogHQExterior.CogHQExterior):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQExterior')

    def enter(self, requestStatus):
        CogHQExterior.CogHQExterior.enter(self, requestStatus)
        self.loader.hood.startSky()

    def exit(self):
        self.loader.hood.stopSky()
        CogHQExterior.CogHQExterior.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\SellbotHQExterior.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:20 Pacific Daylight Time
