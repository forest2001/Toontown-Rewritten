from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedStomperPairAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStomperPairAI")

    def setChildren(self, todo0):
        pass

    def setSquash(self):
        pass

