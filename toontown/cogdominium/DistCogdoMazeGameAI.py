from direct.directnotify import DirectNotifyGlobal
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI

class DistCogdoMazeGameAI(DistCogdoGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoMazeGameAI")

    def requestAction(self, todo0, todo1):
        pass

    def doAction(self, todo0, todo1, todo2):
        pass

    def setNumSuits(self, todo0):
        pass

    def requestUseGag(self, todo0, todo1, todo2, todo3):
        pass

    def toonUsedGag(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def requestSuitHitByGag(self, todo0, todo1):
        pass

    def suitHitByGag(self, todo0, todo1, todo2):
        pass

    def requestHitBySuit(self, todo0, todo1, todo2):
        pass

    def toonHitBySuit(self, todo0, todo1, todo2, todo3):
        pass

    def requestHitByDrop(self):
        pass

    def toonHitByDrop(self, todo0):
        pass

    def requestPickUp(self, todo0):
        pass

    def pickUp(self, todo0, todo1, todo2):
        pass

    def requestGag(self, todo0):
        pass

    def hasGag(self, todo0, todo1):
        pass

