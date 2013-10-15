from direct.directnotify import DirectNotifyGlobal
from otp.distributed.DistributedDistrictAI import DistributedDistrictAI

class ToontownDistrictAI(DistributedDistrictAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownDistrictAI")
    ahnnLog = 0

    def allowAHNNLog(self, ahnnLog):
        self.ahnnLog = ahnnLog

    def d_allowAHNNLog(self, ahnnLog):
        self.sendUpdate('allowAHNNLog', [ahnnLog])

    def b_allowAHNNLog(self, ahnnLog):
        self.allowAHNNLog(ahnnLog)
        self.d_allowAHNNLog(ahnnLog)

    def getAllowAHNNLog(self):
        return self.ahnnLog
