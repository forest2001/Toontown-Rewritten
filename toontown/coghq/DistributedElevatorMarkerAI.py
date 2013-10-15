from direct.directnotify import DirectNotifyGlobal
from otp.level.DistributedEntityAI import DistributedEntityAI

class DistributedElevatorMarkerAI(DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorMarkerAI")

