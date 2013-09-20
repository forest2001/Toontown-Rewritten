# 2013.08.22 22:16:43 Pacific Daylight Time
# Embedded file name: toontown.building.DistributedBBElevator
import DistributedElevator
import DistributedBossElevator
from ElevatorConstants import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedBBElevator(DistributedBossElevator.DistributedBossElevator):
    __module__ = __name__

    def __init__(self, cr):
        DistributedBossElevator.DistributedBossElevator.__init__(self, cr)
        self.type = ELEVATOR_BB
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.elevatorPoints = BossbotElevatorPoints

    def setupElevator(self):
        geom = base.cr.playGame.hood.loader.geom
        self.elevatorModel = loader.loadModel('phase_12/models/bossbotHQ/BB_Elevator')
        self.leftDoor = self.elevatorModel.find('**/left-door')
        if self.leftDoor.isEmpty():
            self.leftDoor = self.elevatorModel.find('**/left_door')
        self.rightDoor = self.elevatorModel.find('**/right-door')
        if self.rightDoor.isEmpty():
            self.rightDoor = self.elevatorModel.find('**/right_door')
        locator = geom.find('**/elevator_locator')
        self.elevatorModel.reparentTo(locator)
        DistributedElevator.DistributedElevator.setupElevator(self)

    def getDestName(self):
        return TTLocalizer.ElevatorBossBotBoss
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\building\DistributedBBElevator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:43 Pacific Daylight Time
