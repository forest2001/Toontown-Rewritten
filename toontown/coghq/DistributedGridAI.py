from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedGridAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGridAI")

