from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals

class DistributedSafezoneInvasion(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.accept('localPieSplat', self.__localPieSplat)
        self.accept('enterSuitAttack', self.__localToonHit)

        self.showFloor = base.render.find('**/ShowFloor')
        self.geom = base.cr.playGame.hood.loader.geom

        base.cr.playGame.hood.loader.music.stop() #This will already be gone before the election sequence starts. We'll just delete it for now.
        musicEnter = base.loadMusic(SafezoneInvasionGlobals.InvasionMusicEnter)
        base.playMusic(musicEnter, looping=1, volume=1.0) #This will be called somewhere else once we have all parts to the soundtrack to piece together.      

        self.startCogSky()

    def delete(self):
        DistributedObject.delete(self)
        self.stopCogSky()
        del self.cogSkyBegin
        del self.cogSkyEnd
        del self.cogSkyBeginStage
        del self.cogSkyEndStage
        del self.sky
        self.ignoreAll()

    def startCogSky(self):
        if hasattr(self, 'sky') and self.sky:
            return
        self.sky = loader.loadModel(SafezoneInvasionGlobals.CogSkyFile)
        self.sky.setTag('sky', 'Invasion')
        self.sky.setBin('background', 100)
        self.sky.setColor(0.3, 0.3, 0.28, 1)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setFogOff()
        self.sky.setZ(-20.0)
        self.sky.reparentTo(camera)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)

        self.fadeIn = self.sky.colorScaleInterval(5.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0), blendType='easeInOut')
        self.fadeOut = self.sky.colorScaleInterval(10.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        self.cogSkyBegin = LerpColorScaleInterval(self.geom, 6.0, Vec4(0.4, 0.4, 0.4, 1), blendType='easeInOut')
        self.cogSkyEnd = LerpColorScaleInterval(self.geom, 9.0, Vec4(1, 1, 1, 1), blendType='easeInOut') 
        self.cogSkyBeginStage = LerpColorScaleInterval(self.showFloor, 6.0, Vec4(0.4, 0.4, 0.4, 1), blendType='easeInOut')
        self.cogSkyEndStage = LerpColorScaleInterval(self.showFloor, 9.0, Vec4(1, 1, 1, 1), blendType='easeInOut') 
        self.fadeIn.start()
        self.cogSkyBegin.start()
        self.cogSkyBeginStage.start()

    def stopCogSky(self):
        self.cogSkyEnd.start()
        self.cogSkyEndStage.start()
        self.fadeOut.start()

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

    def __localToonHit(self, entry):
        damage = int(entry.getIntoNode().getTag('damage'))
        self.d_takeDamage(damage)

    def d_takeDamage(self, damage):
        self.sendUpdate('takeDamage', [damage])
