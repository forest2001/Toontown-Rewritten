from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI

class DistributedMintElevatorExtAI(DistributedElevatorExtAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMintElevatorExtAI")

    def setMintId(self, todo0):
        pass

    def setMintInteriorZone(self, todo0):
        pass

    def setMintInteriorZoneForce(self, todo0):
        pass

