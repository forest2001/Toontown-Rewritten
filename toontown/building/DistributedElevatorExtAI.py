from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorAI import DistributedElevatorAI

class DistributedElevatorExtAI(DistributedElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorExtAI")

    def setFloor(self, todo0):
        pass

