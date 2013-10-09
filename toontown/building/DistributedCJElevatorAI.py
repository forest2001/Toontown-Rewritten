from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedBossElevatorAI import DistributedBossElevatorAI

class DistributedCJElevatorAI(DistributedBossElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCJElevatorAI")

