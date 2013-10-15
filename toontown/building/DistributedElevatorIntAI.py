from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorAI import DistributedElevatorAI

class DistributedElevatorIntAI(DistributedElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorIntAI")

    def requestBuildingExit(self):
        pass

    def forcedExit(self, todo0):
        pass

