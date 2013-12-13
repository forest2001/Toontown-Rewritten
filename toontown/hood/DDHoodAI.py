from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.toon import NPCToons
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.town.DDStreetAI import DDStreetAI

class DDHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDock

    def createSafeZone(self):
        HoodAI.createSafeZone(self)

        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, 'phase_6/dna/donalds_dock_sz.dna')

        self.createPond(self.dnaData)

        NPCToons.createNPC(self.air, 1008, NPCToons.NPCToonDict.get(1008), 1000, posIndex=0)

        self.createHQ(1507, 7)

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)

    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = DDStreetAI(self.air, branch)
            self.streets[branch] = street
