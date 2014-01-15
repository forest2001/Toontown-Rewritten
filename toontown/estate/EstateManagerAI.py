from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.ai.DatabaseObject import DatabaseObject
from toontown.estate.DistributedEstateAI import DistributedEstateAI

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.estateZones = {}

    def startAprilFools(self):
        pass

    def stopAprilFools(self):
        pass

    def getEstateZone(self, avId, name):
        self.setEstateZone(avId, name)

    def setEstateZone(self, avId, name):
        self.estateZones[avId] = self.air.allocateZone()
        print "allocated zoneId %d to %d" % ( self.estateZones[avId], avId )
        estate = DistributedEstateAI(self.air)
        estate.generateWithRequired(self.estateZones[avId])
        print "spawned estate"
        self.sendUpdateToAvatarId(avId, 'setEstateZone', [avId, self.estateZones[avId]])

    def setAvHouseId(self, todo0, todo1):
        pass

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitEstate(self):
        avId = self.air.getAvatarIdFromSender()
        self.air.deallocateZone(self.estateZones[avId])
        del self.estateZones[avId]

    def removeFriend(self, todo0, todo1):
        pass

