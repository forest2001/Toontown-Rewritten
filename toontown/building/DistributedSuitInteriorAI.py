from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedSuitInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitInteriorAI")

    def setZoneId(self, todo0):
        pass

    def setExtZoneId(self, todo0):
        pass

    def setDistBldgDoId(self, todo0):
        pass

    def setNumFloors(self, todo0):
        pass

    def setToons(self, todo0, todo1):
        pass

    def setSuits(self, todo0, todo1, todo2):
        pass

    def setState(self, todo0, todo1):
        pass

    def setAvatarJoined(self):
        pass

    def elevatorDone(self):
        pass

    def reserveJoinDone(self):
        pass

