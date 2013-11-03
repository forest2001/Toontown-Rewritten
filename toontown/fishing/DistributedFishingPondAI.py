from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedFishingPondAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingPondAI")
	
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.area = None
        self.targets = {}
        self.spots = {}

    def hitTarget(self, target):
        avId = self.air.getAvatarIdFromSender()
        if self.targets[target] == None:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to hit nonexistent fishing target!')
            return
        for spot in self.spots:
            if self.spots[spot].avId == avId:
                self.spots[spot].rewardIfValid(target)
                return
        self.air.writeServerEvent('suspicious', avId, 'Toon tried to catch fish while not fishing!')
    def addTarget(self, target):
         self.targets[target.doId] = target

    def addSpot(self, spot):
         self.spots[spot.doId] = spot

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area
