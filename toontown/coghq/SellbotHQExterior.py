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
