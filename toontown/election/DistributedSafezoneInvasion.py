from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
from otp.avatar import Emote
import SafezoneInvasionGlobals

class DistributedSafezoneInvasion(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        
        # Extra stuff...
        cr.invasion = self
        self.invasionOn = False
        
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

        # Define the invasion music we'll need
        self.musicEnter = base.loadMusic(SafezoneInvasionGlobals.InvasionMusicEnter)

        # Victory Music
        self.victoryMusic = base.loadMusic('phase_9/audio/bgm/CogHQ_finale.ogg')

    def delete(self):
        self.cr.invasion = None
        DistributedObject.delete(self)

        # Fade out the cog sky
        self.stopCogSky()

        # Restart the TTC Music
        # base.cr.playGame.hood.loader.music.play()
        base.playMusic(self.victoryMusic, looping=0, volume=0.9) 
        victoryDanceDuration = (2 * 5.15)
        self.victoryIval = Sequence(
            Func(Emote.globalEmote.disableAll, base.localAvatar, 'dbattle, enterReward'),
            Func(base.localAvatar.disableAvatarControls),
            # Parallel(ActorInterval(base.localAvatar, 'victory', loop=1, duration=victoryDanceDuration)),
            # Wait(victoryDanceDuration),
            Func(base.localAvatar.b_setEmoteState, 6, 1.0),
            Wait(5.15),
            Func(Emote.globalEmote.releaseAll, base.localAvatar, 'dbattle, enterReward'),
            Func(base.localAvatar.enableAvatarControls),
            )
        self.victoryIval.start()

        # We should check if the invasion is loaded first to be safe.
        if self.invasionOn:
            # These are only called if the sky is loaded
            del self.cogSkyBegin
            del self.cogSkyEnd
            del self.cogSkyBeginStage
            del self.cogSkyEndStage
        del self.musicEnter
        self.ignoreAll()
    
    def setInvasionStarted(self, started):
        if started and not self.invasionOn:
            self.startCogSky()
            base.playMusic(self.musicEnter, looping=1, volume=1.0)
        elif not started and self.invasionOn:
            self.delete() # Clean everything up
        else:
            return # We don't care about this change...
        self.invasionOn = started

    def startCogSky(self):
        self.sky.reparentTo(camera)
        self.fadeIn = self.sky.colorScaleInterval(5.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0), blendType='easeInOut')
        self.fadeOut = self.sky.colorScaleInterval(6.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        self.cogSkyBegin = LerpColorScaleInterval(self.geom, 6.0, Vec4(0.4, 0.4, 0.4, 1), blendType='easeInOut')
        self.cogSkyEnd = LerpColorScaleInterval(self.geom, 7.0, Vec4(1, 1, 1, 1), blendType='easeInOut') 
        self.cogSkyBeginStage = LerpColorScaleInterval(self.showFloor, 6.0, Vec4(0.4, 0.4, 0.4, 1), blendType='easeInOut')
        self.cogSkyEndStage = LerpColorScaleInterval(self.showFloor, 7.0, Vec4(1, 1, 1, 1), blendType='easeInOut') 
        self.fadeIn.start()
        self.cogSkyBegin.start()
        self.cogSkyBeginStage.start()

    def stopCogSky(self):
        if self.invasionOn:
            cogSkySequence = Sequence(
                Func(self.cogSkyEnd.start),
                Func(self.cogSkyEndStage.start),
                Func(self.fadeOut.start),
                Wait(7),
                Func(self.sky.removeNode) # Remove the sky node after the fade out
                )
            cogSkySequence.start()

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
