from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToontownGlobals import *
from toontown.safezone import RegenTreasurePlannerAI
from toontown.safezone import TreasureGlobals

class TagTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TagTreasurePlannerAI')

    def __init__(self, zoneId, game, callback):
        self.numPlayers = 0
        self.game = game
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(self, zoneId, TreasureGlobals.TreasureTT, 'TagTreasurePlanner-' + str(zoneId), 3, 4, callback)
        return None

    def initSpawnPoints(self):
        self.spawnPoints = [(0, 0, 0.1),
         (5, 20, 0.1),
         (0, 40, 0.1),
         (-5, -20, 0.1),
         (0, -40, 0.1),
         (20, 0, 0.1),
         (40, 5, 0.1),
         (-20, -5, 0.1),
         (-40, 0, 0.1),
         (22, 20, 0.1),
         (-20, 22, 0.1),
         (20, -20, 0.1),
         (-25, -20, 0.1),
         (20, 40, 0.1),
         (20, -44, 0.1),
         (-24, 40, 0.1),
         (-20, -40, 0.1)]
        return self.spawnPoints

    def validAvatar(self, treasure, av):
        return av.doId != self.game.itAvId
