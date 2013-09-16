# 2013.08.22 22:24:28 Pacific Daylight Time
# Embedded file name: toontown.safezone.DistributedEFlyingTreasure
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
import DistributedSZTreasure
from direct.task.Task import Task
import math
import random

class DistributedEFlyingTreasure(DistributedSZTreasure.DistributedSZTreasure):
    __module__ = __name__

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_5.5/models/props/popsicle_treasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'
        self.scale = 2
        self.delT = math.pi * 2.0 * random.random()
        self.shadow = 0

    def disable(self):
        DistributedSZTreasure.DistributedSZTreasure.disable(self)
        taskMgr.remove(self.taskName('flying-treasure'))

    def generateInit(self):
        DistributedSZTreasure.DistributedSZTreasure.generateInit(self)

    def setPosition(self, x, y, z):
        DistributedSZTreasure.DistributedSZTreasure.setPosition(self, x, y, z)
        self.initPos = self.nodePath.getPos()
        self.pos = self.nodePath.getPos()

    def startAnimation(self):
        taskMgr.add(self.animateTask, self.taskName('flying-treasure'))

    def animateTask(self, task):
        pos = self.initPos
        t = 0.5 * math.pi * globalClock.getFrameTime()
        dZ = 5.0 * math.sin(t + self.delT)
        dY = 2.0 * math.cos(t + self.delT)
        self.nodePath.setPos(pos[0], pos[1], pos[2] + dZ)
        if self.pos:
            del self.pos
        self.pos = self.nodePath.getPos()
        return Task.cont
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\safezone\DistributedEFlyingTreasure.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:29 Pacific Daylight Time
