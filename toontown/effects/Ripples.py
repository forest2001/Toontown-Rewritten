# 2013.08.22 22:19:55 Pacific Daylight Time
# Embedded file name: toontown.effects.Ripples
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import globalPropPool

class Ripples(NodePath):
    __module__ = __name__
    rippleCount = 0

    def __init__(self, parent = hidden):
        NodePath.__init__(self)
        self.assign(globalPropPool.getProp('ripples'))
        self.reparentTo(parent)
        self.getChild(0).setZ(0.1)
        self.seqNode = self.find('**/+SequenceNode').node()
        self.seqNode.setPlayRate(0)
        self.track = None
        self.trackId = Ripples.rippleCount
        Ripples.rippleCount += 1
        self.setBin('fixed', 100, 1)
        self.hide()
        return

    def createTrack(self, rate = 1):
        tflipDuration = self.seqNode.getNumChildren() / (float(rate) * 24)
        self.track = Sequence(Func(self.show), Func(self.seqNode.play, 0, self.seqNode.getNumFrames() - 1), Func(self.seqNode.setPlayRate, rate), Wait(tflipDuration), Func(self.seqNode.setPlayRate, 0), Func(self.hide), name='ripples-track-%d' % self.trackId)

    def play(self, rate = 1):
        self.stop()
        self.createTrack(rate)
        self.track.start()

    def loop(self, rate = 1):
        self.stop()
        self.createTrack(rate)
        self.track.loop()

    def stop(self):
        if self.track:
            self.track.finish()

    def destroy(self):
        self.stop()
        self.track = None
        del self.seqNode
        self.removeNode()
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\effects\Ripples.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:56 Pacific Daylight Time
