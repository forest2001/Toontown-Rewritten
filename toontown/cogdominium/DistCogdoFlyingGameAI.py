from direct.directnotify import DirectNotifyGlobal
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI

class DistCogdoFlyingGameAI(DistCogdoGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoFlyingGameAI")

    def requestAction(self, todo0, todo1):
        pass

    def requestPickUp(self, todo0, todo1):
        pass

    def pickUp(self, todo0, todo1, todo2):
        pass

    def debuffPowerup(self, todo0, todo1, todo2):
        pass

    def doAction(self, todo0, todo1):
        pass

    def eagleExitCooldown(self, todo0, todo1):
        pass

    def toonSetAsEagleTarget(self, todo0, todo1, todo2):
        pass

    def toonClearAsEagleTarget(self, todo0, todo1, todo2):
        pass

    def toonDied(self, todo0, todo1):
        pass

    def toonSpawn(self, todo0, todo1):
        pass

    def toonSetBlades(self, todo0, todo1):
        pass

    def toonBladeLost(self, todo0):
        pass

