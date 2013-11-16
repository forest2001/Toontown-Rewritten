from RegenTreasurePlannerAI import RegenTreasurePlannerAI
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from DistributedTTTreasureAI import DistributedTTTreasureAI

class TTTreasurePlannerAI(RegenTreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTTreasurePlannerAI')

    def __init__(self):
        self.numPlayers = 0
        RegenTreasurePlannerAI.__init__(self, ToontownGlobals.ToontownCentral, DistributedTTTreasureAI, 'TTTTreasurePlanner', 15, 8, self.toonUp)

    def toonUp(self, avId):
        av = simbase.air.doId2do.get(avId)
        if not av is None:
            av.toonUp(1)

    def initSpawnPoints(self):
        self.spawnPoints = [
          (-60, -9, 1),
          (7.5, 0.5, 4),
          (74, 85, 3),
          (-49, 68, 0),
          (-114.5, -56, 0.5),
          (-7, -62.5, 0),
          (60, -85.5, 3),
          (21, -124, 2.5)
        ]
        return self.spawnPoints
