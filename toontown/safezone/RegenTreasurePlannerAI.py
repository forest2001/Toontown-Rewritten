# 2013.08.22 22:24:44 Pacific Daylight Time
# Embedded file name: toontown.safezone.RegenTreasurePlannerAI
from direct.distributed.ClockDelta import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import random
import TreasurePlannerAI

class RegenTreasurePlannerAI(TreasurePlannerAI.TreasurePlannerAI):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('RegenTreasurePlannerAI')

    def __init__(self, zoneId, treasureConstructor, taskName, spawnInterval, maxTreasures, callback = None):
        TreasurePlannerAI.TreasurePlannerAI.__init__(self, zoneId, treasureConstructor, callback)
        self.taskName = '%s-%s' % (taskName, zoneId)
        self.spawnInterval = spawnInterval
        self.maxTreasures = maxTreasures

    def start(self):
        self.preSpawnTreasures()
        self.startSpawning()

    def stop(self):
        self.stopSpawning()

    def stopSpawning(self):
        taskMgr.remove(self.taskName)

    def startSpawning(self):
        self.stopSpawning()
        taskMgr.doMethodLater(self.spawnInterval, self.upkeepTreasurePopulation, self.taskName)

    def upkeepTreasurePopulation(self, task):
        if self.numTreasures() < self.maxTreasures:
            self.placeRandomTreasure()
        taskMgr.doMethodLater(self.spawnInterval, self.upkeepTreasurePopulation, self.taskName)
        return Task.done

    def placeRandomTreasure(self):
        self.notify.debug('Placing a Treasure...')
        spawnPointIndex = self.nthEmptyIndex(random.randrange(self.countEmptySpawnPoints()))
        self.placeTreasure(spawnPointIndex)

    def preSpawnTreasures(self):
        for i in range(self.maxTreasures):
            self.placeRandomTreasure()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\RegenTreasurePlannerAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:44 Pacific Daylight Time
