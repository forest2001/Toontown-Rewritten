from toontown.safezone import DistributedTreasureAI
from toontown.safezone import TreasureGlobals

class DistributedCashbotBossTreasureAI(DistributedTreasureAI.DistributedTreasureAI):

    def __init__(self, air, boss, goon, style, fx, fy, fz):
        pos = goon.getPos()
        type = TreasureGlobals.SafeZoneTreasureSpawns[style][0]
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, boss, type, pos[0], pos[1], 0)
        self.goonId = goon.doId
        self.style = style
        self.finalPosition = (fx, fy, fz)
        
    def validAvatar(self, av):
        # Avatars can only heal if they are missing some health, but aren't sad.
        if av.getHp() < av.getMaxHp() and av.getHp() > 0:
            av.toonUp(self.healAmount)
            return True
        else:
            return False

    def getGoonId(self):
        return self.goonId

    def setGoonId(self, goonId):
        self.goonId = goonId

    def b_setGoonId(self, goonId):
        self.setGoonId(goonId)
        self.d_setGoonId(goonId)

    def d_setGoonId(self, goonId):
        self.sendUpdate('setGoonId', [goonId])

    def getStyle(self):
        return self.style

    def setStyle(self, hoodId):
        self.style = hoodId

    def b_setStyle(self, hoodId):
        self.setStyle(hoodId)
        self.d_setStyle(hoodId)

    def d_setStyle(self, hoodId):
        self.sendUpdate('setStyle', [hoodId])

    def getFinalPosition(self):
        return self.finalPosition

    def setFinalPosition(self, x, y, z):
        self.finalPosition = (x, y, z)

    def b_setFinalPosition(self, x, y, z):
        self.setFinalPosition(x, y, z)
        self.d_setFinalPosition(x, y, z)

    def d_setFinalPosition(self, x, y, z):
        self.sendUpdate('setFinalPosition', [x, y, z])
