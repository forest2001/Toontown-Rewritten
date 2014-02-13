from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals

class DistributedSafezoneInvasion(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.accept('localPieSplat', self.__localPieSplat)

        base.cr.playGame.hood.loader.music.stop() #This will already be gone before the election sequence starts. We'll just delete it for now.
        musicEnter = base.loadMusic(SafezoneInvasionGlobals.InvasionMusicEnter)
        base.playMusic(musicEnter, looping=1, volume=1.0) #This will be called somewhere else once we have all parts to the soundtrack to piece together.      

        self.startCogSky()

    def delete(self):
        DistributedObject.delete(self)
        del self.sky
        del self.cogSkyBegin
        self.ignoreAll()

    def startCogSky(self):
        if hasattr(self, 'sky') and self.sky:
            self.stopCogSky()
        self.cogSkyBegin = Sequence(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 6.0, Vec4(0.4, 0.4, 0.4, 1)))
        self.cogSkyEnd = LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 5.0, Vec4(1, 1, 1, 1))
        self.sky = loader.loadModel(SafezoneInvasionGlobals.CogSkyFile)
        self.sky.setTag('sky', 'Invasion')
        self.sky.setScale(1.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.3, 0.3, 0.28, 1)
        self.sky.setBin('background', 100)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval(5.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0), blendType='easeInOut')
        fadeIn.start()
        self.sky.setZ(-20.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        self.cogSkyBegin.start()

    def stopCogSky(self):
        if hasattr(self, 'sky') and self.sky:
            base.cr.playGame.hood.loader.stopSky()
            fadeOut = self.sky.colorScaleInterval(5.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
            fadeIn.start()

    def __localPieSplat(self, pieCode, entry):
        if pieCode == ToontownGlobals.PieCodeToon:
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Toon %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
                return
            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                self.d_hitToon(doId)
        elif pieCode == ToontownGlobals.PieCodeInvasionSuit:
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Suit %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
                return
            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                self.d_hitSuit(doId)

    def d_hitToon(self, doId):
        self.sendUpdate('hitToon', [doId])

    def d_hitSuit(self, doId):
        self.sendUpdate('hitSuit', [doId])
