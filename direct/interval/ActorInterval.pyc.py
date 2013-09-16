# 2013.08.22 22:14:20 Pacific Daylight Time
# Embedded file name: direct.interval.ActorInterval
__all__ = ['ActorInterval', 'LerpAnimInterval']
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import Interval
import math
from direct.showbase import LerpBlendHelpers

class ActorInterval(Interval.Interval):
    __module__ = __name__
    notify = directNotify.newCategory('ActorInterval')
    animNum = 1

    def __init__(self, actor, animName, loop = 0, constrainedLoop = 0, duration = None, startTime = None, endTime = None, startFrame = None, endFrame = None, playRate = 1.0, name = None, forceUpdate = 0, partName = None, lodName = None):
        id = 'Actor-%s-%d' % (animName, ActorInterval.animNum)
        ActorInterval.animNum += 1
        self.actor = actor
        self.animName = animName
        self.controls = self.actor.getAnimControls(self.animName, partName=partName, lodName=lodName)
        self.loopAnim = loop
        self.constrainedLoop = constrainedLoop
        self.forceUpdate = forceUpdate
        self.playRate = playRate
        if name == None:
            name = id
        if len(self.controls) == 0:
            self.notify.warning('Unknown animation for actor: %s' % self.animName)
            self.frameRate = 1.0
            self.startFrame = 0
            self.endFrame = 0
        else:
            self.frameRate = self.controls[0].getFrameRate() * abs(playRate)
            if startFrame != None:
                self.startFrame = startFrame
            elif startTime != None:
                self.startFrame = startTime * self.frameRate
            else:
                self.startFrame = 0
            if endFrame != None:
                self.endFrame = endFrame
            elif endTime != None:
                self.endFrame = endTime * self.frameRate
            elif duration != None:
                if startTime == None:
                    startTime = float(self.startFrame) / float(self.frameRate)
                endTime = startTime + duration
                self.endFrame = duration * self.frameRate
            else:
                maxFrames = self.controls[0].getNumFrames()
                warned = 0
                for i in range(1, len(self.controls)):
                    numFrames = self.controls[i].getNumFrames()
                    if numFrames != maxFrames and numFrames != 1 and not warned:
                        self.notify.warning("Animations '%s' on %s have an inconsistent number of frames." % (animName, actor.getName()))
                        warned = 1
                    maxFrames = max(maxFrames, numFrames)

                self.endFrame = maxFrames - 1
        self.reverse = playRate < 0
        if self.endFrame < self.startFrame:
            self.reverse = 1
            t = self.endFrame
            self.endFrame = self.startFrame
            self.startFrame = t
        self.numFrames = self.endFrame - self.startFrame + 1
        self.implicitDuration = 0
        if duration == None:
            self.implicitDuration = 1
            duration = float(self.numFrames) / self.frameRate
        Interval.Interval.__init__(self, name, duration)
        return

    def getCurrentFrame(self):
        retval = None
        if not self.isStopped():
            framesPlayed = self.numFrames * self.currT
            retval = self.startFrame + framesPlayed
        return retval

    def privStep(self, t):
        frameCount = t * self.frameRate
        if self.constrainedLoop:
            frameCount = frameCount % self.numFrames
        if self.reverse:
            absFrame = self.endFrame - frameCount
        else:
            absFrame = self.startFrame + frameCount
        intFrame = int(math.floor(absFrame + 0.0001))
        for control in self.controls:
            numFrames = control.getNumFrames()
            if self.loopAnim:
                frame = intFrame % numFrames + (absFrame - intFrame)
            else:
                frame = max(min(absFrame, numFrames - 1), 0)
            control.pose(frame)

        if self.forceUpdate:
            self.actor.update()
        self.state = CInterval.SStarted
        self.currT = t

    def privFinalize(self):
        if self.implicitDuration and not self.loopAnim:
            if self.reverse:
                for control in self.controls:
                    control.pose(self.startFrame)

            else:
                for control in self.controls:
                    control.pose(self.endFrame)

            if self.forceUpdate:
                self.actor.update()
        else:
            self.privStep(self.getDuration())
        self.state = CInterval.SFinal
        self.intervalDone()

    def resetControls(self, partName, lodName = None):
        self.controls = self.actor.getAnimControls(self.animName, partName=partName, lodName=lodName)


class LerpAnimInterval(CLerpAnimEffectInterval):
    __module__ = __name__
    lerpAnimNum = 1

    def __init__(self, actor, duration, startAnim, endAnim, startWeight = 0.0, endWeight = 1.0, blendType = 'noBlend', name = None, partName = None, lodName = None):
        if name == None:
            name = 'LerpAnimInterval-%d' % LerpAnimInterval.lerpAnimNum
            LerpAnimInterval.lerpAnimNum += 1
        blendType = self.stringBlendType(blendType)
        CLerpAnimEffectInterval.__init__(self, name, duration, blendType)
        if startAnim != None:
            controls = actor.getAnimControls(startAnim, partName=partName, lodName=lodName)
            for control in controls:
                self.addControl(control, startAnim, 1.0 - startWeight, 1.0 - endWeight)

        if endAnim != None:
            controls = actor.getAnimControls(endAnim, partName=partName, lodName=lodName)
            for control in controls:
                self.addControl(control, endAnim, startWeight, endWeight)

        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\ActorInterval.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:20 Pacific Daylight Time
