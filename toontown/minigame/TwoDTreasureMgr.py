# 2013.08.22 22:23:08 Pacific Daylight Time
# Embedded file name: toontown.minigame.TwoDTreasureMgr
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDTreasure
import random

class TwoDTreasureMgr(DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDTreasureMgr')

    def __init__(self, section, treasureList, enemyList):
        self.section = section
        self.treasureList = treasureList
        self.enemyList = enemyList
        self.load()

    def destroy(self):
        while len(self.treasures):
            treasure = self.treasures[0]
            treasure.destroy()
            self.treasures.remove(treasure)

        self.treasures = None
        self.section = None
        return

    def load(self):
        if len(self.treasureList):
            self.treasuresNP = NodePath('Treasures')
            self.treasuresNP.reparentTo(self.section.sectionNP)
        self.treasures = []
        for index in xrange(len(self.treasureList)):
            treasureAttribs = self.treasureList[index][0]
            treasureValue = self.treasureList[index][1]
            self.createNewTreasure(treasureAttribs, treasureValue)

        self.enemyTreasures = []
        numPlayers = self.section.sectionMgr.game.numPlayers
        pos = Point3(-1, -1, -1)
        for index in xrange(len(self.enemyList)):
            self.createNewTreasure([pos], numPlayers, isEnemyGenerated=True)

    def createNewTreasure(self, attrib, value, isEnemyGenerated = False, model = None):
        treasureId = self.section.getSectionizedId(len(self.treasures))
        if model == None:
            model = self.getModel(value, self.section.sectionMgr.game.assetMgr.treasureModelList)
        newTreasure = TwoDTreasure.TwoDTreasure(self, treasureId, attrib[0], value, isEnemyGenerated, model)
        newTreasure.model.reparentTo(self.treasuresNP)
        self.treasures.append(newTreasure)
        if isEnemyGenerated:
            self.enemyTreasures.append(newTreasure)
        return

    def getModel(self, value, modelList):
        value -= 1
        model = modelList[value]
        if value == 0:
            model.setColor(1, 0.8, 0.8, 1)
        elif value == 1:
            model.setColor(0.8, 1, 0.8, 1)
        elif value == 2:
            model.setColor(0.9, 0.9, 1, 1)
        elif value == 3:
            model.setColor(1, 1, 0.6, 1)
        return model
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\TwoDTreasureMgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:08 Pacific Daylight Time
