from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class BattleBlockerAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("BattleBlockerAI")

    def setActive(self, todo0):
        pass

    def setSuits(self, todo0):
        pass

    def setBattle(self, todo0):
        pass

    def setBattleFinished(self):
        pass

