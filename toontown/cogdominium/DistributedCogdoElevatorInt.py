# 2013.08.22 22:18:00 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.DistributedCogdoElevatorInt
from toontown.building.DistributedElevatorInt import DistributedElevatorInt

class DistributedCogdoElevatorInt(DistributedElevatorInt):
    __module__ = __name__

    def _getDoorsClosedInfo(self):
        return ('cogdoInterior', 'cogdoInterior')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\DistributedCogdoElevatorInt.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:00 Pacific Daylight Time
