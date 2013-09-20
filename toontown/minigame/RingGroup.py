# 2013.08.22 22:22:58 Pacific Daylight Time
# Embedded file name: toontown.minigame.RingGroup
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import NodePath
import Ring
import RingTrack
import RingTrackGroup
import RingGameGlobals

class RingGroup(NodePath):
    __module__ = __name__

    def __init__(self, trackGroup, ringModel, posScale, colorIndices):
        NodePath.__init__(self)
        self.assign(hidden.attachNewNode(base.localAvatar.uniqueName('ring-group')))
        self.__period = trackGroup.period
        self.__reverseFlag = trackGroup.reverseFlag
        self.__tOffset = trackGroup.tOffset
        self.__numRings = len(trackGroup.tracks)
        self.__rings = []
        self.__ringModels = []
        for i in range(0, self.__numRings):
            track = trackGroup.tracks[i]
            tOffset = trackGroup.trackTOffsets[i]
            ring = Ring.Ring(track, tOffset, posScale)
            ring.reparentTo(self)
            model = ringModel.copyTo(ring)
            model.setColor(RingGameGlobals.ringColors[colorIndices[i]][1])
            self.__rings.append(ring)
            self.__ringModels.append(model)

    def delete(self):
        for model in self.__ringModels:
            model.removeNode()

        for ring in self.__rings:
            ring.removeNode()

        del self.__rings
        del self.__ringModels

    def getRing(self, index):
        return self.__ringModels[index]

    def setT(self, t):
        normT = (t / self.__period + self.__tOffset) % 1.0
        if self.__reverseFlag:
            normT = 1.0 - normT
        for ring in self.__rings:
            ring.setT(normT)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\RingGroup.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:58 Pacific Daylight Time
