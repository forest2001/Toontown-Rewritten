from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons

class BRHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createZone(self):
        SZHoodAI.createZone(self)

        self.spawnObjects()
