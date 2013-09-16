# 2013.08.22 22:14:22 Pacific Daylight Time
# Embedded file name: direct.interval.LerpInterval
__all__ = ['LerpNodePathInterval',
 'LerpPosInterval',
 'LerpHprInterval',
 'LerpQuatInterval',
 'LerpScaleInterval',
 'LerpShearInterval',
 'LerpPosHprInterval',
 'LerpPosQuatInterval',
 'LerpHprScaleInterval',
 'LerpQuatScaleInterval',
 'LerpPosHprScaleInterval',
 'LerpPosQuatScaleInterval',
 'LerpPosHprScaleShearInterval',
 'LerpPosQuatScaleShearInterval',
 'LerpColorInterval',
 'LerpColorScaleInterval',
 'LerpTexOffsetInterval',
 'LerpTexRotateInterval',
 'LerpTexScaleInterval',
 'LerpFunctionInterval',
 'LerpFunc',
 'LerpFunctionNoStateInterval',
 'LerpFuncNS']
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import Interval
from direct.showbase import LerpBlendHelpers

class LerpNodePathInterval(CLerpNodePathInterval):
    __module__ = __name__
    lerpNodePathNum = 1

    def __init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other):
        if name == None:
            name = '%s-%d' % (self.__class__.__name__, self.lerpNodePathNum)
            LerpNodePathInterval.lerpNodePathNum += 1
        elif '%d' in name:
            name = name % LerpNodePathInterval.lerpNodePathNum
            LerpNodePathInterval.lerpNodePathNum += 1
        blendType = self.stringBlendType(blendType)
        if other == None:
            other = NodePath()
        CLerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        return

    def anyCallable(self, *params):
        for param in params:
            if callable(param):
                return 1

        return 0

    def setupParam(self, func, param):
        if param != None:
            if callable(param):
                func(param())
            else:
                func(param)
        return


class LerpPosInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, startPos = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(pos, startPos)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpHprInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, hpr, startHpr = None, startQuat = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(hpr, startHpr, startQuat)
        if self.paramSetup:
            self.endHpr = hpr
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.inPython = 1
        else:
            self.setEndHpr(hpr)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndHpr, self.endHpr)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpQuatInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, quat = None, startHpr = None, startQuat = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None, hpr = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        if not quat:
            quat = LOrientationf()
            quat.setHpr(hpr)
        self.paramSetup = self.anyCallable(quat, startHpr, startQuat)
        if self.paramSetup:
            self.endQuat = quat
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.inPython = 1
        else:
            self.setEndQuat(quat)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndQuat, self.endQuat)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, scale, startScale = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(scale, startScale)
        if self.paramSetup:
            self.endScale = scale
            self.startScale = startScale
            self.inPython = 1
        else:
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpShearInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, shear, startShear = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(shear, startShear)
        if self.paramSetup:
            self.endShear = shear
            self.startShear = startShear
            self.inPython = 1
        else:
            self.setEndShear(shear)
            if startShear != None:
                self.setStartShear(startShear)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndShear, self.endShear)
            self.setupParam(self.setStartShear, self.startShear)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpPosHprInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, hpr, startPos = None, startHpr = None, startQuat = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(pos, startPos, hpr, startHpr, startQuat)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.endHpr = hpr
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
            self.setEndHpr(hpr)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
            self.setupParam(self.setEndHpr, self.endHpr)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpPosQuatInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, quat = None, startPos = None, startHpr = None, startQuat = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None, hpr = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        if not quat:
            quat = LOrientationf()
            quat.setHpr(hpr)
        self.paramSetup = self.anyCallable(pos, startPos, quat, startHpr, startQuat)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.endQuat = quat
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
            self.setEndQuat(quat)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
            self.setupParam(self.setEndQuat, self.endQuat)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpHprScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, hpr, scale, startHpr = None, startQuat = None, startScale = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(hpr, startHpr, startQuat, scale, startScale)
        if self.paramSetup:
            self.endHpr = hpr
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.endScale = scale
            self.startScale = startScale
            self.inPython = 1
        else:
            self.setEndHpr(hpr)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndHpr, self.endHpr)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpQuatScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, quat = None, scale = None, hpr = None, startHpr = None, startQuat = None, startScale = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        if not quat:
            quat = LOrientationf()
            quat.setHpr(hpr)
        self.paramSetup = self.anyCallable(quat, startHpr, startQuat, scale, startScale)
        if self.paramSetup:
            self.endQuat = quat
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.endScale = scale
            self.startScale = startScale
            self.inPython = 1
        else:
            self.setEndQuat(quat)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndQuat, self.endQuat)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpPosHprScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, hpr, scale, startPos = None, startHpr = None, startQuat = None, startScale = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(pos, startPos, hpr, startHpr, startQuat, scale, startScale)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.endHpr = hpr
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.endScale = scale
            self.startScale = startScale
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
            self.setEndHpr(hpr)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
            self.setupParam(self.setEndHpr, self.endHpr)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpPosQuatScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, quat = None, scale = None, startPos = None, startHpr = None, startQuat = None, startScale = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None, hpr = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        if not quat:
            quat = LOrientationf()
            quat.setHpr(hpr)
        self.paramSetup = self.anyCallable(pos, startPos, quat, startHpr, startQuat, scale, startScale)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.endQuat = quat
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.endScale = scale
            self.startScale = startScale
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
            self.setEndQuat(quat)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
            self.setupParam(self.setEndQuat, self.endQuat)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpPosHprScaleShearInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, hpr, scale, shear, startPos = None, startHpr = None, startQuat = None, startScale = None, startShear = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        self.paramSetup = self.anyCallable(pos, startPos, hpr, startHpr, startQuat, scale, startScale, shear, startShear)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.endHpr = hpr
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.endScale = scale
            self.startScale = startScale
            self.endShear = shear
            self.startShear = startShear
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
            self.setEndHpr(hpr)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
            self.setEndShear(shear)
            if startShear != None:
                self.setStartShear(startShear)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
            self.setupParam(self.setEndHpr, self.endHpr)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
            self.setupParam(self.setEndShear, self.endShear)
            self.setupParam(self.setStartShear, self.startShear)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpPosQuatScaleShearInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, pos, quat = None, scale = None, shear = None, startPos = None, startHpr = None, startQuat = None, startScale = None, startShear = None, other = None, blendType = 'noBlend', bakeInStart = 1, fluid = 0, name = None, hpr = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, fluid, nodePath, other)
        if not quat:
            quat = LOrientationf()
            quat.setHpr(hpr)
        self.paramSetup = self.anyCallable(pos, startPos, quat, startHpr, startQuat, scale, startScale, shear, startShear)
        if self.paramSetup:
            self.endPos = pos
            self.startPos = startPos
            self.endQuat = quat
            self.startHpr = startHpr
            self.startQuat = startQuat
            self.endScale = scale
            self.startScale = startScale
            self.endShear = shear
            self.startShear = startShear
            self.inPython = 1
        else:
            self.setEndPos(pos)
            if startPos != None:
                self.setStartPos(startPos)
            self.setEndQuat(quat)
            if startHpr != None:
                self.setStartHpr(startHpr)
            if startQuat != None:
                self.setStartQuat(startQuat)
            self.setEndScale(scale)
            if startScale != None:
                self.setStartScale(startScale)
            self.setEndShear(shear)
            if startShear != None:
                self.setStartShear(startShear)
        return

    def privDoEvent(self, t, event):
        if self.paramSetup and event == CInterval.ETInitialize:
            self.setupParam(self.setEndPos, self.endPos)
            self.setupParam(self.setStartPos, self.startPos)
            self.setupParam(self.setEndQuat, self.endQuat)
            self.setupParam(self.setStartHpr, self.startHpr)
            self.setupParam(self.setStartQuat, self.startQuat)
            self.setupParam(self.setEndScale, self.endScale)
            self.setupParam(self.setStartScale, self.startScale)
            self.setupParam(self.setEndShear, self.endShear)
            self.setupParam(self.setStartShear, self.startShear)
        LerpNodePathInterval.privDoEvent(self, t, event)


class LerpColorInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, color, startColor = None, other = None, blendType = 'noBlend', bakeInStart = 1, name = None, override = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, 0, nodePath, other)
        self.setEndColor(color)
        if startColor != None:
            self.setStartColor(startColor)
        if override != None:
            self.setOverride(override)
        return


class LerpColorScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, colorScale, startColorScale = None, other = None, blendType = 'noBlend', bakeInStart = 1, name = None, override = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, 0, nodePath, other)
        self.setEndColorScale(colorScale)
        if startColorScale != None:
            self.setStartColorScale(startColorScale)
        if override != None:
            self.setOverride(override)
        return


class LerpTexOffsetInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, texOffset, startTexOffset = None, other = None, blendType = 'noBlend', textureStage = None, bakeInStart = 1, name = None, override = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, 0, nodePath, other)
        self.setEndTexOffset(texOffset)
        if startTexOffset != None:
            self.setStartTexOffset(startTexOffset)
        if textureStage != None:
            self.setTextureStage(textureStage)
        if override != None:
            self.setOverride(override)
        return


class LerpTexRotateInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, texRotate, startTexRotate = None, other = None, blendType = 'noBlend', textureStage = None, bakeInStart = 1, name = None, override = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, 0, nodePath, other)
        self.setEndTexRotate(texRotate)
        if startTexRotate != None:
            self.setStartTexRotate(startTexRotate)
        if textureStage != None:
            self.setTextureStage(textureStage)
        if override != None:
            self.setOverride(override)
        return


class LerpTexScaleInterval(LerpNodePathInterval):
    __module__ = __name__

    def __init__(self, nodePath, duration, texScale, startTexScale = None, other = None, blendType = 'noBlend', textureStage = None, bakeInStart = 1, name = None, override = None):
        LerpNodePathInterval.__init__(self, name, duration, blendType, bakeInStart, 0, nodePath, other)
        self.setEndTexScale(texScale)
        if startTexScale != None:
            self.setStartTexScale(startTexScale)
        if textureStage != None:
            self.setTextureStage(textureStage)
        if override != None:
            self.setOverride(override)
        return


class LerpFunctionNoStateInterval(Interval.Interval):
    __module__ = __name__
    lerpFunctionIntervalNum = 1
    notify = directNotify.newCategory('LerpFunctionNoStateInterval')

    def __init__(self, function, duration = 0.0, fromData = 0, toData = 1, blendType = 'noBlend', extraArgs = [], name = None):
        self.function = function
        self.fromData = fromData
        self.toData = toData
        self.blendType = LerpBlendHelpers.getBlend(blendType)
        self.extraArgs = extraArgs
        if name == None:
            name = 'LerpFunctionInterval-%d' % LerpFunctionNoStateInterval.lerpFunctionIntervalNum
            LerpFunctionNoStateInterval.lerpFunctionIntervalNum += 1
        elif '%d' in name:
            name = name % LerpFunctionNoStateInterval.lerpFunctionIntervalNum
            LerpFunctionNoStateInterval.lerpFunctionIntervalNum += 1
        Interval.Interval.__init__(self, name, duration)
        return

    def privStep(self, t):
        if t >= self.duration:
            if t > self.duration:
                print 'after end'
        elif self.duration == 0.0:
            apply(self.function, [self.toData] + self.extraArgs)
        else:
            bt = self.blendType(t / self.duration)
            data = self.fromData * (1 - bt) + self.toData * bt
            apply(self.function, [data] + self.extraArgs)
        self.state = CInterval.SStarted
        self.currT = t


class LerpFuncNS(LerpFunctionNoStateInterval):
    __module__ = __name__

    def __init__(self, *args, **kw):
        LerpFunctionNoStateInterval.__init__(self, *args, **kw)


class LerpFunctionInterval(Interval.Interval):
    __module__ = __name__
    lerpFunctionIntervalNum = 1
    notify = directNotify.newCategory('LerpFunctionInterval')

    def __init__(self, function, duration = 0.0, fromData = 0, toData = 1, blendType = 'noBlend', extraArgs = [], name = None):
        self.function = function
        self.fromData = fromData
        self.toData = toData
        self.blendType = LerpBlendHelpers.getBlend(blendType)
        self.extraArgs = extraArgs
        if name == None:
            name = 'LerpFunctionInterval-%s-%d' % (function.__name__, LerpFunctionInterval.lerpFunctionIntervalNum)
            LerpFunctionInterval.lerpFunctionIntervalNum += 1
        elif '%d' in name:
            name = name % LerpFunctionInterval.lerpFunctionIntervalNum
            LerpFunctionInterval.lerpFunctionIntervalNum += 1
        Interval.Interval.__init__(self, name, duration)
        return

    def privStep(self, t):
        if t >= self.duration:
            apply(self.function, [self.toData] + self.extraArgs)
        elif self.duration == 0.0:
            apply(self.function, [self.toData] + self.extraArgs)
        else:
            bt = self.blendType(t / self.duration)
            data = self.fromData * (1 - bt) + self.toData * bt
            apply(self.function, [data] + self.extraArgs)
        self.state = CInterval.SStarted
        self.currT = t


class LerpFunc(LerpFunctionInterval):
    __module__ = __name__

    def __init__(self, *args, **kw):
        LerpFunctionInterval.__init__(self, *args, **kw)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\LerpInterval.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:23 Pacific Daylight Time
