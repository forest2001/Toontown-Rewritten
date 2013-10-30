from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI

class DistributedBankAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBankAI")

    def avatarEnter(self):
        pass

    def freeAvatar(self):
        pass

    def setMovie(self, todo0, todo1, todo2):
        pass

    def transferMoney(self, todo0):
        pass

