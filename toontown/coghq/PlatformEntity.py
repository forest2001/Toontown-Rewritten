# 2013.08.22 22:19:19 Pacific Daylight Time
# Embedded file name: toontown.coghq.PlatformEntity
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.level import BasicEntities
import MovingPlatform

class PlatformEntity(BasicEntities.NodePathEntity):
    __module__ = __name__

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.start()

    def destroy(self):
        self.stop()
        BasicEntities.NodePathEntity.destroy(self)

    def start(self):
        model = loader.loadModel(self.modelPath)
        if model is None:
            return
        if len(self.floorName) == 0:
            return
        model.setScale(self.modelScale)
        model.flattenMedium()
        self.platform = MovingPlatform.MovingPlatform()
        self.platform.setupCopyModel(self.getParentToken(), model, self.floorName)
        self.platform.reparentTo(self)
        startPos = Point3(0, 0, 0)
        endPos = self.offset
        distance = Vec3(self.offset).length()
        waitDur = self.period * self.waitPercent
        moveDur = self.period - waitDur
        self.moveIval = Sequence(WaitInterval(waitDur * 0.5), LerpPosInterval(self.platform, moveDur * 0.5, endPos, startPos=startPos, name='platformOut%s' % self.entId, blendType=self.motion, fluid=1), WaitInterval(waitDur * 0.5), LerpPosInterval(self.platform, moveDur * 0.5, startPos, startPos=endPos, name='platformBack%s' % self.entId, blendType=self.motion, fluid=1), name=self.getUniqueName('platformIval'))
        self.moveIval.loop()
        self.moveIval.setT(globalClock.getFrameTime() - self.level.startTime + self.period * self.phaseShift)
        return

    def stop(self):
        if hasattr(self, 'moveIval'):
            self.moveIval.pause()
            del self.moveIval
        if hasattr(self, 'platform'):
            self.platform.destroy()
            del self.platform

    if __dev__:

        def attribChanged(self, *args):
            self.stop()
            self.start()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\PlatformEntity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:19 Pacific Daylight Time
