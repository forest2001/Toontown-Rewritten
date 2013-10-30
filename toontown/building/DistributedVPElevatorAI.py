from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedBossElevatorAI import DistributedBossElevatorAI

class DistributedVPElevatorAI(DistributedBossElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedVPElevatorAI")

