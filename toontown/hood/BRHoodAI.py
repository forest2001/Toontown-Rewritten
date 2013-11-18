from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class BRHoodAI(HoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createSafeZone(self):
        HoodAI.createSafeZone(self)

        self.createHQ(3508, 8)
