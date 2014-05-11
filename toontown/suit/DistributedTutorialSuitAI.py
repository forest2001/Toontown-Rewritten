from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.tutorial.DistributedBattleTutorialAI import DistributedBattleTutorialAI
from panda3d.core import *
import SuitDNA

class FakeBattleManager:
    def destroy(self, battle):
        pass

class DistributedTutorialSuitAI(DistributedSuitBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTutorialSuitAI")

    def __init__(self, air):
        DistributedSuitBaseAI.__init__(self, air, None)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('f')
        self.dna = suitDNA
        self.setLevel(0)
        
    def destroy(self):
        del self.dna

    def requestBattle(self, x, y, z, h, p, r):
        self.confrontPosHpr = (LPoint3f(x, y, z), LPoint3f(h, p, r))
        avId = self.air.getAvatarIdFromSender()
        battle = DistributedBattleTutorialAI(self.air, FakeBattleManager(), LPoint3f(x,y,z), self, avId, 20001, maxSuits=1, tutorialFlag=1)
        battle.generateWithRequired(self.zoneId)
        battle.battleCellId = 0
        pass

    def getConfrontPosHpr(self):
        return self.confrontPosHpr
