from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI

class DistributedLawOfficeElevatorExtAI(DistributedElevatorExtAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawOfficeElevatorExtAI")

    def setEntranceId(self, todo0):
        pass

    def setLawOfficeInteriorZone(self, todo0):
        pass

    def setLawOfficeInteriorZoneForce(self, todo0):
        pass

