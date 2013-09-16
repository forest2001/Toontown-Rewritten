# 2013.08.22 22:24:59 Pacific Daylight Time
# Embedded file name: toontown.shtiker.NewbiePurchaseManagerAI
import PurchaseManagerAI

class NewbiePurchaseManagerAI(PurchaseManagerAI.PurchaseManagerAI):
    __module__ = __name__

    def __init__(self, air, newbieId, playerArray, mpArray, previousMinigameId, trolleyZone):
        self.ownedNewbieId = newbieId
        newbieList = []
        PurchaseManagerAI.PurchaseManagerAI.__init__(self, air, playerArray, mpArray, previousMinigameId, trolleyZone, newbieList)

    def startCountdown(self):
        pass

    def getOwnedNewbieId(self):
        return self.ownedNewbieId

    def getInvolvedPlayerIds(self):
        return [self.ownedNewbieId]

    def handlePlayerLeaving(self, avId):
        toon = self.air.doId2do.get(avId)
        if toon:
            self.air.questManager.toonRodeTrolleyFirstTime(toon)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\shtiker\NewbiePurchaseManagerAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:00 Pacific Daylight Time
