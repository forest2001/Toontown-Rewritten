from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
import PhoneGlobals

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")
    

    def setInitialScale(self, todo0, todo1, todo2):
        pass
        
    def getInitialScale(self):
        return (1, 1, 1)

    def setNewScale(self, todo0, todo1, todo2):
        pass

    def avatarEnter(self):
        pass

    def avatarExit(self):
        pass

    def freeAvatar(self):
        pass

    def setLimits(self, todo0):
        pass

    def setMovie(self, todo0, todo1, todo2):
        pass

    def requestPurchaseMessage(self, todo0, todo1, todo2):
        pass

    def requestPurchaseResponse(self, todo0, todo1):
        pass

    def requestGiftPurchaseMessage(self, todo0, todo1, todo2, todo3):
        pass

    def requestGiftPurchaseResponse(self, todo0, todo1):
        pass

