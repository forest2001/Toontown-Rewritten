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

        # Let's load some models
        self.sky = loader.loadModel(SafezoneInvasionGlobals.CogSkyFile)
        self.sky.setBin('background', 100)
        self.sky.setColor(0.3, 0.3, 0.28, 1)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setFogOff()
        self.sky.setZ(-20.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)

        # Stop the music in case it wasn't already.
        base.cr.playGame.hood.loader.music.stop()

        #Define the invasion music we'll need
        self.musicEnter = base.loadMusic(SafezoneInvasionGlobals.InvasionMusicEnter)

        self.invasionOn = False

        # Did we join in late? If so, let's get back up to speed
        if self.invasionOn == True:
            base.playMusic(self.musicEnter, looping=1, volume=1.0)
            self.sky.reparentTo(camera)
            self.geom.setColor(Vec4(0.4, 0.4, 0.4, 1))
            self.showFloor.setColor(Vec4(0.4, 0.4, 0.4, 1))

    def delete(self):
        DistributedObject.delete(self)
        # We should check if the invasion is loaded first to be safe.
        if self.invasionOn == True:
            # These are only called if the sky is loaded
            del self.cogSkyBegin
            del self.cogSkyEnd
            del self.cogSkyBeginStage
            del self.cogSkyEndStage
        self.sky.removeNode()
        del self.musicEnter
        self.ignoreAll()

    def startInvasion(self):
        self.startCogSky()
        base.playMusic(self.musicEnter, looping=1, volume=1.0)
        self.invasionOn = True

    def finishInvasion(self):
        self.stopCogSky()
        self.invasionOn = False

    def deleteInvasion(self):
        self.stopCogSky()
        base.stopMusic(self.musicEnter)

    def startCogSky(self):
        self.sky.reparentTo(camera)
        # If this gets called again for some reason, no need for it to fade in again.
        if self.invasionOn == True:
            self.geom.setColor(Vec4(0.4, 0.4, 0.4, 1))
            self.showFloor.setColor(Vec4(0.4, 0.4, 0.4, 1))
            return
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
        if self.invasionOn == True:
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
