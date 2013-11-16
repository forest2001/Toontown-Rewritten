from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import cPickle


class DistributedHQInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHQInteriorAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.isTutorial = False
        self.zoneId = 0
        self.block = 0
        self.leaderData = cPickle.dumps(([], [], []))

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def setLeaderBoard(self, leaderData):
        self.leaderData = leaderData

    def setTutorial(self, isTutorial):
        self.isTutorial = False

    def getZoneIdAndBlock(self):
        return (self.zoneId, self.block)

    def getLeaderBoard(self):
        return self.leaderData

    def getTutorial(self):
        return self.isTutorial