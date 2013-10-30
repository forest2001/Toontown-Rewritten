from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI

class DistributedFactoryElevatorExtAI(DistributedElevatorExtAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFactoryElevatorExtAI")

    def setEntranceId(self, todo0):
        pass

    def setFactoryInteriorZone(self, todo0):
        pass

    def setFactoryInteriorZoneForce(self, todo0):
        pass

