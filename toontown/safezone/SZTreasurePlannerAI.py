from RegenTreasurePlannerAI import RegenTreasurePlannerAI
from direct.directnotify import DirectNotifyGlobal

class SZTreasurePlannerAI(RegenTreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SZTreasurePlannerAI')

    def __init__(self, zoneId, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures):
        self.zoneId = zoneId
        self.spawnPoints = spawnPoints
        self.healAmount = healAmount
        RegenTreasurePlannerAI.__init__(self, zoneId, treasureType, 'SZTreasurePlanner-%d' % zoneId, spawnRate, maxTreasures)

    def initSpawnPoints(self):
        pass

    def validAvatar(self, treasure, av):
        # Avatars can only heal if they are missing some health, but aren't sad.
        if av.getHp() < av.getMaxHp() and av.getHp > 0:
            av.toonUp(self.healAmount)
            return True
        else:
            return False
