from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorFSMAI import DistributedElevatorFSMAI

class DistributedElevatorFloorAI(DistributedElevatorFSMAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorFloorAI")

    def setFloor(self, todo0):
        pass

    def setLocked(self, todo0):
        pass

    def setEntering(self, todo0):
        pass

    def kickToonsOut(self):
        pass

    def setLatch(self, todo0):
        pass

