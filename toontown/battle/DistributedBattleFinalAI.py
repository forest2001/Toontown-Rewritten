from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleBaseAI import DistributedBattleBaseAI

class DistributedBattleFinalAI(DistributedBattleBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBattleFinalAI")

    def setBossCogId(self, todo0):
        pass

    def setBattleNumber(self, todo0):
        pass

    def setBattleSide(self, todo0):
        pass

