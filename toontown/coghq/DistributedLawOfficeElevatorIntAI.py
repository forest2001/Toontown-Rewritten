from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorFloorAI import DistributedElevatorFloorAI

class DistributedLawOfficeElevatorIntAI(DistributedElevatorFloorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawOfficeElevatorIntAI")

    def setLawOfficeInteriorZone(self, todo0):
        pass

