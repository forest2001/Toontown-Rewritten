from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedInteractiveEntityAI import DistributedInteractiveEntityAI

class DistributedSwitchAI(DistributedInteractiveEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSwitchAI")

