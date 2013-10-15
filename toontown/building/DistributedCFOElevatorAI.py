from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedBossElevatorAI import DistributedBossElevatorAI

class DistributedCFOElevatorAI(DistributedBossElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCFOElevatorAI")

