# 2013.08.22 22:24:13 Pacific Daylight Time
# Embedded file name: toontown.racing.EffectManager
from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import *
from toontown.battle import MovieUtil

class EffectManager(DirectObject):
    __module__ = __name__

    def __init__(self):
        self.effectList = []

    def delete(self):
        for effect in effectList:
            self.__removeEffect(effect)

    def addSplatEffect(self, spawner, splatName = 'splat-creampie', time = 1, size = 6, parent = render):
        splat = globalPropPool.getProp(splatName)
        splatSeq = Sequence()
        splatType = globalPropPool.getPropType(splatName)
        splatShow = Func(self.__showProp, splat, size, parent, spawner.getPos(parent))
        splatAnim = ActorInterval(splat, splatName)
        splatHide = Func(MovieUtil.removeProp, splat)
        splatRemove = Func(self.__removeEffect, splatSeq)
        splatSeq.append(splatShow)
        splatSeq.append(splatAnim)
        splatSeq.append(splatHide)
        splatSeq.append(splatRemove)
        splatSeq.start()
        self.effectList.append(splatSeq)

    def __showProp(self, prop, size, parent, pos):
        prop.reparentTo(parent)
        prop.setScale(size)
        prop.setBillboardPointEye()
        prop.setPos(pos + Vec3(0, 0, size / 2))

    def __removeEffect(self, effect):
        if effect.isPlaying():
            effect.finish()
        self.effectList.remove(effect)
        effect = None
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\EffectManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:24:14 Pacific Daylight Time
