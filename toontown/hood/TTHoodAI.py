from toontown.toonbase import ToontownGlobals
from toontown.toon.DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from toontown.toon.ToonDNA import ToonDNA
from HoodAI import HoodAI

class TTHoodAI(HoodAI):
    SAFEZONE = ToontownGlobals.ToontownCentral

    def __init__(self, air):
        HoodAI.__init__(self, air)

        self.createTrolley()

        self.createFlippy()

    def createFlippy(self):
        npc = DistributedNPCToonBaseAI(self.air, 9001)
        dna = ToonDNA()
        dna.newToonFromProperties('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 3, 3, 3, 3, 7, 2)
        npc.setName('Flippy')
        npc.setDNAString(dna.makeNetString())
        npc.setHp(15)
        npc.setMaxHp(15)
        npc.setPositionIndex(12)
        npc.generateWithRequired(self.SAFEZONE)
