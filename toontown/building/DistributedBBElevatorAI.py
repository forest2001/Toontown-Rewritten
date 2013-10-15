from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedBossElevatorAI import DistributedBossElevatorAI

class DistributedBBElevatorAI(DistributedBossElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBBElevatorAI")

