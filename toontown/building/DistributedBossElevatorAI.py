from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI

class DistributedBossElevatorAI(DistributedElevatorExtAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBossElevatorAI")

    def setBossOfficeZone(self, todo0):
        pass

    def setBossOfficeZoneForce(self, todo0):
        pass

