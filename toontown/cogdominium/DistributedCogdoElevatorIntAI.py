from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorIntAI import DistributedElevatorIntAI

class DistributedCogdoElevatorIntAI(DistributedElevatorIntAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogdoElevatorIntAI")

