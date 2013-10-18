from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class TTHoodAI(HoodAI):
    SAFEZONE = ToontownGlobals.ToontownCentral

    def __init__(self, air):
        HoodAI.__init__(self, air)

        self.createTrolley()
