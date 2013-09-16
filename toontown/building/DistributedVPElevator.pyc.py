# 2013.08.22 22:16:56 Pacific Daylight Time
# Embedded file name: toontown.building.DistributedVPElevator
import DistributedElevator
import DistributedBossElevator
from ElevatorConstants import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedVPElevator(DistributedBossElevator.DistributedBossElevator):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVPElevator')

    def __init__(self, cr):
        DistributedBossElevator.DistributedBossElevator.__init__(self, cr)
        self.type = ELEVATOR_VP
        self.countdownTime = ElevatorData[self.type]['countdown']

    def setupElevator(self):
        self.elevatorModel = loader.loadModel('phase_9/models/cogHQ/cogHQ_elevator')
        icon = self.elevatorModel.find('**/big_frame/')
        icon.hide()
        self.leftDoor = self.elevatorModel.find('**/left-door')
        self.rightDoor = self.elevatorModel.find('**/right-door')
        geom = base.cr.playGame.hood.loader.geom
        locator = geom.find('**/elevator_locator')
        self.elevatorModel.reparentTo(locator)
        self.elevatorModel.setH(180)
        DistributedElevator.DistributedElevator.setupElevator(self)

    def getDestName(self):
        return TTLocalizer.ElevatorSellBotBoss
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\building\DistributedVPElevator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:16:56 Pacific Daylight Time
