from toontown.building.DistributedElevatorInt import DistributedElevatorInt

class DistributedCogdoElevatorInt(DistributedElevatorInt):
    __module__ = __name__

    def _getDoorsClosedInfo(self):
        return ('cogdoInterior', 'cogdoInterior')
