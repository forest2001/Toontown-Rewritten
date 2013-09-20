# 2013.08.22 22:19:54 Pacific Daylight Time
# Embedded file name: toontown.effects.Glow
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect

class Glow(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)

    def createTrack(self):
        model = loader.loadModel('phase_4/models/props/tt_m_efx_ext_particleCards')
        self.spark = model.find('**/tt_t_efx_ext_particleSparkle')
        self.effectModel = self.attachNewNode('effectModelNode')
        self.spark.reparentTo(self.effectModel)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectModel.hide()
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.effectModel.hide()
        self.effectModel.setColorScale(self.effectColor)
        pulseIval = Sequence(Wait(0.1), Func(self.effectModel.setColorScale, self.effectColor), Wait(0.1), Func(self.effectModel.setColorScale, Vec4(1, 1, 1, 0.7)))
        self.startEffect = Sequence(Func(self.effectModel.show), Func(pulseIval.loop))
        self.endEffect = Sequence(Func(pulseIval.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def cleanUpEffect(self):
        self.effectModel.hide()
        EffectController.cleanUpEffect(self)
        if self.pool and self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\effects\Glow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:54 Pacific Daylight Time
