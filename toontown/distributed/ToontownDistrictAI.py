from direct.directnotify import DirectNotifyGlobal
from otp.distributed.DistributedDistrictAI import DistributedDistrictAI

class ToontownDistrictAI(DistributedDistrictAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownDistrictAI")

    def setParentingRules(self, todo0, todo1):
        pass

    def allowAHNNLog(self, todo0):
        pass

