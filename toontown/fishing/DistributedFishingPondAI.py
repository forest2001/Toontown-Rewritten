from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals
from toontown.dna.DNASpawnerAI import *
from toontown.dna.DNAProp import DNAProp
from toontown.dna.DNAGroup import DNAGroup
from toontown.hood import ZoneUtil
from toontown.toon import NPCToons

class DistributedFishingPondAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingPondAI")
	
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.area = None
        self.targets = {}
        self.spots = {}
        self.bingoMgr = None

    def hitTarget(self, target):
        avId = self.air.getAvatarIdFromSender()
        if self.targets.get(target) == None:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to hit nonexistent fishing target!')
            return
        spot = self.hasToon(avId)
        if spot:
            spot.rewardIfValid(target)
            return
        self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to catch fish while not fishing!')
    def addTarget(self, target):
         self.targets[target.doId] = target

    def addSpot(self, spot):
         self.spots[spot.doId] = spot

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area
        
    def hasToon(self, avId):
        for spot in self.spots:
            if self.spots[spot].avId == avId:
                return self.spots[spot]
        return
        
@dnaSpawn(DNAGroup, 'fishing_pond')
def spawn(air, zone, element, match):
    if zone % 1000 != 0:
        # This should hopefully create the Fishermen NPCs on streets.
        NPCToons.createNpcsInZone(air, zone)
    pond = DistributedFishingPondAI(air)
    area = ZoneUtil.getBranchZone(zone)
    pond.setArea(area)
    pond.generateWithRequired(zone)
    bingoMgr = DistributedPondBingoManagerAI(air)
    bingoMgr.setPondDoId(pond.getDoId())
    bingoMgr.generateWithRequired(zone)
    pond.bingoMgr = bingoMgr
    pond.bingoMgr.createGame()
    simbase.air.fishManager.ponds[zone] = pond
    
    for i in range(FishingTargetGlobals.getNumTargets(area)):
                target = DistributedFishingTargetAI(simbase.air)
                target.setPondDoId(pond.getDoId())
                target.generateWithRequired(zone)
    for child in element.children:
        if isinstance(child, DNAProp) and 'fishing_spot' in child.code:
            spot = DistributedFishingSpotAI(air)
            spot.setPondDoId(pond.getDoId())
            x, y, z = child.getPos()
            h, p, r = child.getHpr()
            spot.setPosHpr(x, y, z, h, p, r)
            spot.generateWithRequired(zone)