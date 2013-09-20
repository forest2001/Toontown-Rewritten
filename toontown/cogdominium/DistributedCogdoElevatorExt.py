# 2013.08.22 22:18:00 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.DistributedCogdoElevatorExt
from toontown.building.DistributedElevatorExt import DistributedElevatorExt

class DistributedCogdoElevatorExt(DistributedElevatorExt):
    __module__ = __name__

    def setupElevator(self):
        DistributedElevatorExt.setupElevator(self)
        self.elevatorSphereNodePath.setY(-1.0)
        self.elevatorSphereNodePath.setZ(1.5)

    def getElevatorModel(self):
        return self.bldg.getCogdoElevatorNodePath()

    def getBldgDoorOrigin(self):
        return self.bldg.getCogdoDoorOrigin()

    def _getDoorsClosedInfo(self):
        return ('cogdoInterior', 'cogdoInterior')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\DistributedCogdoElevatorExt.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:00 Pacific Daylight Time
