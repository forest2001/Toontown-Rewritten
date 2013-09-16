# 2013.08.22 22:22:57 Pacific Daylight Time
# Embedded file name: toontown.minigame.Ring
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import NodePath
import RingTrack

class Ring(NodePath):
    __module__ = __name__

    def __init__(self, moveTrack, tOffset, posScale = 1.0):
        NodePath.__init__(self)
        self.assign(hidden.attachNewNode(base.localAvatar.uniqueName('ring')))
        self.setMoveTrack(moveTrack)
        self.setTOffset(tOffset)
        self.setPosScale(posScale)
        self.setT(0.0)

    def setMoveTrack(self, moveTrack):
        self.__moveTrack = moveTrack

    def setTOffset(self, tOffset):
        self.__tOffset = float(tOffset)

    def setPosScale(self, posScale):
        self.__posScale = posScale

    def setT(self, t):
        pos = self.__moveTrack.eval((t + self.__tOffset) % 1.0)
        self.setPos(pos[0] * self.__posScale, 0, pos[1] * self.__posScale)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\Ring.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:57 Pacific Daylight Time
