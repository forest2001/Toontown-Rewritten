from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedCrusherEntityAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrusherEntityAI")

