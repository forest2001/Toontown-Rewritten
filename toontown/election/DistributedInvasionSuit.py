from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from direct.task.Task import Task
from otp.nametag.NametagConstants import *
from toontown.suit.DistributedSuitBase import DistributedSuitBase
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals
from toontown.battle import BattleParticles, SuitBattleGlobals, BattleProps
from InvasionSuitBase import InvasionSuitBase
from toontown.distributed.DelayDeletable import DelayDeletable
from toontown.distributed.DelayDelete import *
import random

class DistributedInvasionSuit(DistributedSuitBase, InvasionSuitBase, FSM, DelayDeletable):
    def __init__(self, cr):
        DistributedSuitBase.__init__(self, cr)
        InvasionSuitBase.__init__(self)
        FSM.__init__(self, 'InvasionSuitFSM')

        self.spawnPointId = 0
        self.moveTask = None

        self._lerpTimestamp = 0
        self._turnInterval = None
        self._staticPoint = (0, 0, 0)

        self.explodeTrack = None

        self.attackTarget = 0
        self.attackProp = ''
        self.attackDamage = 0
        self.exploding = False
        self.invasionFinale = False
        self._attackInterval = None
        self.phraseSequence = None
        self.finaleBrainstormSequence = None

        # For the Director's attacks
        self.brainstormSfx = loader.loadSfx('phase_5/audio/sfx/SA_brainstorm.ogg')
        self.quakeLiftSfx = loader.loadSfx('phase_5/audio/sfx/General_throw_miss.ogg')
        self.quakeLandSfx = loader.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')

        # Cog speeches, for when we want to manually define it
        phasePath = 'phase_3.5/audio/dial/'
        self.speechMurmurSfx = loader.loadSfx(phasePath + 'COG_VO_murmur.ogg')
        self.speechStatementSfx = loader.loadSfx(phasePath + 'COG_VO_statement.ogg')
        self.speechQuestionSfx = loader.loadSfx(phasePath + 'COG_VO_question.ogg')
        self.speechGruntSfx = loader.loadSfx(phasePath + 'COG_VO_grunt.ogg') # This one is currently the only one used in this file. Remove the rest if they aren't used before deploying.


        # Get a few things defined for our Shakers
        self.shakerRadialAttack = None
        self.stompSfx = loader.loadSfx('phase_5/audio/sfx/SA_tremor.ogg')
        self.msStartStomp = Sequence(
            Func(self.play, 'walk', fromFrame=0, toFrame=22),
            Wait(0.9),
            Func(self.loop, 'walk', fromFrame=22, toFrame=62)
        )
        self.msSoundLoop = Sequence(SoundInterval(self.stompSfx, duration=1.6, startTime=0.3, volume=0.4, node=self))

    def announceGenerate(self):
        DistributedSuitBase.announceGenerate(self)
        self.corpMedallion.hide()
        self.healthBar.show()
        self.updateHealthBar(0, 1)

        self.walkSpeed = (ToontownGlobals.SuitWalkSpeed *
                          SuitBattleGlobals.SuitSizes[self.dna.name] / 4.0)

        # Set ourselves up for a good pieing:
        colNode = self.find('**/distAvatarCollNode*')
        colNode.setTag('pieCode', str(ToontownGlobals.PieCodeInvasionSuit))

    def generateAnimDict(self):
        animDict = DistributedSuitBase.generateAnimDict(self)

        if self.style.name == 'ms':
            # Movers and Shakers should stomp instead of walk
            animDict['walk'] = 'phase_5/models/char/suitB-stomp'

        if self.style.body == 'b':
            animDict['effort'] = 'phase_5/models/char/suitB-effort'
            animDict['jump'] = 'phase_6/models/char/suitB-jump'

        if self.style.body == 'c':
            # Suit C's (Flunky, etc.) animations are located in phase_3.5, because of the tutorial.
            animDict['throw-paper'] = 'phase_3.5/models/char/suitC-throw-paper'
            animDict['throw-object'] = 'phase_3.5/models/char/suitC-throw-paper'
        else:
            # The rest of the suit animations are in phase_5, for the most part.
            animDict['throw-paper'] = 'phase_5/models/char/suit%s-throw-paper' % (self.style.body.upper())
            animDict['throw-object'] = 'phase_5/models/char/suit%s-throw-object' % (self.style.body.upper())
        return animDict
        
    def delete(self):
        self.demand('Off')
        self.stopShakerRadialAttack()
        self.stopMoveTask()
        DistributedSuitBase.delete(self)


    '''
     STANDARD COGS                                                                                         
       The cogs have three main states: March, Attack, and Idle.                                              
       Standard Cogs find a toon to attack, then March towards them until the toon is gone or they have died. 
    '''
    def enterIdle(self, time):
        self.loop('neutral', 0)

    def enterFlyDown(self, time):
        if self.spawnPointId == 99:
            x, y, z, h = SafezoneInvasionGlobals.FirstSuitSpawnPoint
        else:
            x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.loop('neutral', 0)
        self.mtrack = self.beginSupaFlyMove(Point3(x, y, z), 1, 'fromSky',
                                            walkAfterLanding=False)
        self.mtrack.start(time)

    def exitFlyDown(self):
        self.mtrack.finish()
        del self.mtrack
        self.detachPropeller()

    def __moveToStaticPoint(self):
        x, y, h = self._staticPoint
        self.setX(x)
        self.setY(y)

        if self._turnInterval:
            self._turnInterval.finish()
        q = Quat()
        q.setHpr((h, 0, 0))
        self._turnInterval = self.quatInterval(0.1, q, blendType='easeOut')
        self._turnInterval.start()

        # And set the Z properly:
        self.__placeOnGround()

    def enterMarch(self, time):
        if self.style.name == 'ms':
            self.msStartStomp.start(time)
            self.msSoundLoop.loop(time)
            self.shakerRadialAttack = taskMgr.add(self.__checkToonsInRadius, self.uniqueName('ShakerAttack'))
        else:
            self.loop('walk', 0)
        self.startMoveTask()

    def exitMarch(self):
        if self.msStartStomp.isPlaying():
            self.msStartStomp.finish()
        if self.msSoundLoop.isPlaying():
            self.msSoundLoop.finish()
        self.loop('neutral', 0)
        self.stopMoveTask()
        self.stopShakerRadialAttack()
        self.__moveToStaticPoint()

    def enterAttack(self, time):
        if self.style.name == 'ms':
            self.shakerRadialAttack = taskMgr.add(self.__checkToonsInRadius, self.uniqueName('ShakerAttack'))
            self.msStartStomp.start(time)
            self.msSoundLoop.loop(time)
            return
        self._attackInterval = self.makeAttackTrack()
        self._attackInterval.start(time)

    def exitAttack(self):
        if self._attackInterval and self._attackInterval.isPlaying():
            self._attackInterval.pause()
            self.cleanupProp(self._attackInterval.prop, self._attackInterval.propIsActor)
            #hehehe manual cleanup. so bad
        if self.msStartStomp.isPlaying():
            self.msStartStomp.finish()
        if self.msSoundLoop.isPlaying():
            self.msSoundLoop.finish()
        self.stopShakerRadialAttack()

    def setAttackInfo(self, targetId, attackProp, attackDamage):
        self.attackTarget = targetId
        self.attackProp = attackProp
        self.attackDamage = attackDamage

    def makeAttackTrack(self):
        # TODO: Add more props than the tie. Possibly more animations.
        prop = BattleProps.globalPropPool.getProp(self.attackProp)
        propIsActor = True
        animName = 'throw-paper'
        x, y, z, h, p, r = (0.1, 0.2, -0.35, 0, 336, 0)
        if self.attackProp == 'redtape':
            animName = 'throw-object'
            x,y,z,h,p,r = (0.24, 0.09, -0.38, -1.152, 86.581, -76.784)
            propIsActor = False
        elif self.attackProp == 'newspaper':
            animName = 'throw-object'
            propIsActor = False
            x,y,z,h,p,r = (-0.07, 0.17, -0.13, 161.867, -33.149, -48.086)
            prop.setScale(4)
        elif self.attackProp == 'pink-slip':
            animName = 'throw-paper'
            propIsActor = False
            x,y,z,h,p,r = (0.07, -0.06, -0.18, -172.075, -26.715, -89.131)
            prop.setScale(5)
        elif self.attackProp == 'power-tie':
            animName = 'throw-paper'
            propIsActor = False
            x,y,z,h,p,r = (1.16, 0.24, 0.63, 171.561, 1.745, -163.443)
            prop.setScale(4)
        # Prop collisions:
        colNode = CollisionNode('SuitAttack')
        colNode.setTag('damage', str(self.attackDamage))

        bounds = prop.getBounds()
        center = bounds.getCenter()
        radius = bounds.getRadius()
        sphere = CollisionSphere(center.getX(), center.getY(), center.getZ(), radius)
        sphere.setTangible(0)
        colNode.addSolid(sphere)
        prop.attachNewNode(colNode)

        toonId = self.attackTarget

        # Rotate the suit to look at the toon it is attacking
        self.lookAtTarget()

        if self.style.body in ['a', 'b']:
            throwDelay = 3
        elif self.style.body == 'c':
            throwDelay = 2.3

        def throwProp():
            toon = self.cr.doId2do.get(toonId)
            if not toon:
                self.cleanupProp(prop, propIsActor)
                return

            self.lookAtTarget()

            prop.wrtReparentTo(render)

            hitPos = toon.getPos() + Vec3(0, 0, 2.5)
            distance = (prop.getPos() - hitPos).length()
            speed = 50.0

            Sequence(prop.posInterval(distance/speed, hitPos),
                     Func(self.cleanupProp, prop, propIsActor)).start()
                     

        track = Sequence(Parallel(
            ActorInterval(self, animName),
            Track(
                (0.4, Func(prop.reparentTo, self.getRightHand())),
                (0.0, Func(prop.setPosHpr, x, y, z, h, p, r)),
                (0.0, Func(self.sayFaceoffTaunt)),
                (throwDelay, Func(throwProp))
            ),
        ))
        track.prop = prop
        track.propIsActor = propIsActor

        return track
    

    def cleanupProp(self, prop, propIsActor):
        if propIsActor:
            prop.cleanup()
            prop.removeNode()
        else:
            prop.removeNode()

    def lookAtTarget(self):
        if not self.attackTarget:
            return # No target to look at.
        target = self.cr.doId2do.get(self.attackTarget)
        if not target:
            return # Target not found.
        self.lookAt(target)

    def setHP(self, hp):
        currHP = getattr(self, 'currHP', 0)
        if currHP > hp:
            self.showHpText(hp - currHP)

        DistributedSuitBase.setHP(self, hp)

        self.updateHealthBar(0, 1)

    def enterStunned(self, time):
        self._stunInterval = ActorInterval(self, 'pie-small-react')
        self._stunInterval.start(time)

    def exitStunned(self):
        self._stunInterval.finish()

    def enterExplode(self, time):
        # We're done with this guy
        self.stash()

        # Are we exploding?
        self.exploding = True

        # Lets create a specific actor for the explosion and load the explosion stuff
        loseActor = self.getLoseActor()
        loseActor.reparentTo(render)
        spinningSound = base.loadSfx('phase_3.5/audio/sfx/Cog_Death.ogg')
        deathSound = base.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')

        # Oh boy, time to load all of our explosion effects!
        explosionInterval = ActorInterval(loseActor, 'lose', startFrame=0, endFrame=150)
        deathSoundTrack = Sequence(Wait(0.6), SoundInterval(spinningSound, duration=1.2, startTime=1.5, volume=0.2, node=loseActor), SoundInterval(spinningSound, duration=3.0, startTime=0.6, volume=0.8, node=loseActor), SoundInterval(deathSound, volume=0.32, node=loseActor))
        
        # Load the particles for the explosion
        BattleParticles.loadParticles()
        smallGears = BattleParticles.createParticleEffect(file='gearExplosionSmall')
        singleGear = BattleParticles.createParticleEffect('GearExplosion', numParticles=1)
        smallGearExplosion = BattleParticles.createParticleEffect('GearExplosion', numParticles=10)
        bigGearExplosion = BattleParticles.createParticleEffect('BigGearExplosion', numParticles=30)
        gearPoint = Point3(loseActor.getX(), loseActor.getY(), loseActor.getZ())
        smallGears.setDepthWrite(False)
        singleGear.setDepthWrite(False)
        smallGearExplosion.setDepthWrite(False)
        bigGearExplosion.setDepthWrite(False)

        # Create the explosion track
        explosionTrack = Sequence()
        explosionTrack.append(Wait(5.4))
        explosionTrack.append(self.createKapowExplosionTrack(loseActor))

        gears1Track = Sequence(Wait(2.0), ParticleInterval(smallGears, loseActor, worldRelative=0, duration=4.3, cleanup=True), name='gears1Track')
        gears2MTrack = Track((0.0, explosionTrack), (0.7, ParticleInterval(singleGear, loseActor, worldRelative=0, duration=5.7, cleanup=True)), (5.2, ParticleInterval(smallGearExplosion, loseActor, worldRelative=0, duration=1.2, cleanup=True)), (5.4, ParticleInterval(bigGearExplosion, loseActor, worldRelative=0, duration=1.0, cleanup=True)), name='gears2MTrack')
        
        # Cleanup
        
        cleanupTrack = Track((6.5, Func(self.cleanupLoseActor))) # Better delete the poor guy when we're done

        # Blow the sucker up
        self.explodeTrack = Sequence(Parallel(explosionInterval, deathSoundTrack, gears1Track, gears2MTrack))
        self.explodeTrack.delayDelete = DelayDelete(self, 'cleanupExplode')
        self.explodeTrack.append(Func(self.explodeTrack.delayDelete.destroy))
        self.explodeTrack.start()
        self.explodeTrack.setT(time)

    def exitExplode(self):
        self.explodeTrack.finish()

    def createKapowExplosionTrack(self, parent): #(self, parent, explosionPoint, scale)
        explosionTrack = Sequence()
        explosion = loader.loadModel('phase_3.5/models/props/explosion.bam')
        explosion.setBillboardPointEye()
        explosion.setDepthWrite(False)
        explosionPoint = Point3(0, 0, 4.1) #This should be set according to suit height.
        explosionTrack.append(Func(explosion.reparentTo, parent))
        explosionTrack.append(Func(explosion.setPos, explosionPoint))
        explosionTrack.append(Func(explosion.setScale, 0.4)) #The scale should also be set according to the suit.
        explosionTrack.append(Wait(0.6))
        explosionTrack.append(Func(explosion.removeNode))
        return explosionTrack

    def setSpawnPoint(self, spawnPointId):
        self.spawnPointId = spawnPointId
        if self.spawnPointId == 99:
            x, y, z, h = SafezoneInvasionGlobals.FirstSuitSpawnPoint
        else:
            x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.freezeLerp(x, y)
        self.setPos(x, y, z)
        self.setH(h)

    def setMarchLerp(self, x1, y1, x2, y2, timestamp):
        self.setLerpPoints(x1, y1, x2, y2)
        self._lerpTimestamp = timestamp

        # Also turn to our new ideal "H":
        if self._turnInterval:
            self._turnInterval.finish()
        q = Quat()
        q.setHpr((self._idealH, 0, 0))
        self._turnInterval = self.quatInterval(0.1, q, blendType='easeOut')
        self._turnInterval.start()

    def setStaticPoint(self, x, y, h):
        self._staticPoint = (x, y, h)
        if self.state != 'March':
            self.__moveToStaticPoint()

    def sayFaceoffTaunt(self, custom = False, phrase = "", dialogue = None):
        if custom == True:
            self.setChatAbsolute(phrase, CFSpeech | CFTimeout, dialogue)
        elif custom == False:
            if random.random() < 0.2:
                taunt = SuitBattleGlobals.getFaceoffTaunt(self.getStyleName(), self.doId, randomChoice = True)
                self.setChatAbsolute(taunt, CFSpeech | CFTimeout)

    def makeSkelecog(self):
        self.setSkelecog(1)
        self.corpMedallion.hide()
        self.healthBar.show()

    def setState(self, state, timestamp):
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def startMoveTask(self):
        if self.moveTask:
            return
        self.moveTask = taskMgr.add(self.__move, self.uniqueName('move-task'))

    def __move(self, task):
        x, y = self.getPosAt(globalClockDelta.localElapsedTime(self._lerpTimestamp))
        self.setX(x)
        self.setY(y)

        self.__placeOnGround()
        
        return task.cont

    def __placeOnGround(self):
        # This schedules a task to fire after the shadow-culling to place the
        # suit directly on his shadow.
        taskMgr.add(self.__placeOnGroundTask, self.uniqueName('place-on-ground'), sort=31)

    def __placeOnGroundTask(self, task):
        if getattr(self, 'shadowPlacer', None) and \
           getattr(self.shadowPlacer, 'shadowNodePath', None):
            self.setZ(self.shadowPlacer.shadowNodePath, 0.025)
        return task.done
        
    def stopMoveTask(self):
        if self.moveTask:
            self.moveTask.remove()
            self.moveTask = None
    
    
    '''
     MOVER AND SHAKERS
       Mover and Shakers are the same as standard cogs, though they stomp the ground as they march.
       Toons within a certain radius of them will lose laff, forcing them to hit them from a distance.
    '''
    def d_takeShakerDamage(self, damage, toon):
        if toon.isStunned:
            return
        if toon is base.localAvatar:
            if toon.hp > 0:
                self.sendUpdate('takeShakerDamage', [damage])
                # Check if he still has more than 0 after taking damage
                if toon.hp > 0:
                    base.localAvatar.disableAvatarControls()
                    taskMgr.doMethodLater(1.5, self.enableAvatarControls, 'EnableAvatarControls', extraArgs = [toon])
                    toon.b_setEmoteState(12, 1.0)
                    toon.stunToon()

    def enableAvatarControls(self, toon):
        if toon.hp > 0:
            base.localAvatar.enableAvatarControls()

    def __checkToonsInRadius(self, task):
        if self.exploding:
            return task.done

        toon = base.localAvatar
        if toon:
            if Vec3(toon.getPos(self)).length() <= SafezoneInvasionGlobals.MoveShakerRadius:
                self.applyShakeAttack(toon, SafezoneInvasionGlobals.MoveShakerDamageRadius)
        return task.cont

    def applyShakeAttack(self, toon, damage):
        if not getattr(localAvatar.controlManager.currentControls, 'isAirborne', 0):
            if toon.hp > 0:
                if not toon.isStunned:
                    self.d_takeShakerDamage(damage, toon)
                    toon.stunToon()
            else:
                # Dont try and enable avatar controls if a toon is sad
                taskMgr.remove('EnableAvatarControls')

    def stopShakerRadialAttack(self):
        if self.shakerRadialAttack:
            self.shakerRadialAttack.remove()
            self.shakerRadialAttack = None

    '''
     THE INVASION FINALE
      To end the invasion, we send in the Boss of it. He brainstorms ideas and occasionally loses his temper.
      The appears to take damage but actually takes none, as his death is a scripted sequence.
    '''
    def setInvasionFinale(self, finale):
        if finale and not self.invasionFinale:
            if not self.isSkelecog:
                self.makeSkelecog()
            self.nametag.setWordwrap(10.0)
            self.setDisplayName(SafezoneInvasionGlobals.FinaleSuitName)
            self.setPickable(0) # We don't want people to see the cog's true identity, a Level 11 Loanshark.
            self.setScale(1.1)
            self.walkSpeed = ToontownGlobals.SuitWalkSpeed # The Director should walk slower than other high-level cogs
            self.acceptOnce('wrapUpSequence', self.wrapUp)
        elif not finale and self.invasionFinale:
            pass
        else:
            return # We don't care about this change...
        self.invasionFinale = finale
        
    def wrapUp(self, offset):
        print 'WE DID IT BOIS'
        cogSequence = Sequence()
        cogSequence.start()
        cogSequence.setT(offset)
    

    def enterFinalePhrases(self, offset):
        self.phraseSequence = Sequence(
            Wait(6.5),
            Func(self.sayFaceoffTaunt, True, SafezoneInvasionGlobals.FinaleSuitPhrases[0]),
            Wait(5),
            Func(self.sayFaceoffTaunt, True, SafezoneInvasionGlobals.FinaleSuitPhrases[1]),
            Wait(4),
            Func(self.sayFaceoffTaunt, True, SafezoneInvasionGlobals.FinaleSuitPhrases[2])
        )
        self.phraseSequence.setT(offset)
        self.phraseSequence.start()

    def exitFinalePhrases(self):
        pass

    def enterFinaleBrainstormAttack(self, offset):
        if Vec3(base.localAvatar.getPos(self)).length() <= 40:
            # Currently, the cloud only forms over the local toon.
            # Preferably it would form over all toons in the area, but I'm not sure how to go about doing that.
            # That may not be good for performance either.
            braincloud = BattleProps.globalPropPool.getProp('stormcloud')
            braincloud.reparentTo(base.localAvatar)
            braincloud.setScale(0)
            braincloud.setZ(6)
            brainstorm = BattleParticles.createParticleEffect(name='BrainStorm')
            brainstorm.setDepthWrite(False)

            def __checkNearCloud(task):
                if Vec3(base.localAvatar.getPos(braincloud)).length() <= 5:
                    self.applyShakeAttack(base.localAvatar, SafezoneInvasionGlobals.FinaleSuitAttackDamage)

            self.finaleBrainstormSequence = Sequence(
                braincloud.scaleInterval(3, (3.5, 3.5, 2.5)),
                Parallel(
                    Func(base.playSfx, self.brainstormSfx),
                    Func(braincloud.wrtReparentTo, render),
                    ParticleInterval(brainstorm, braincloud, worldRelative=0, duration=4.3, cleanup=True)
                ),
                Wait(1),
                braincloud.scaleInterval(1, (0.0, 0.0, 0.0)),
            )
            taskMgr.doMethodLater(4, __checkNearCloud, 'CheckNearBraincloud')
            self.finaleBrainstormSequence.setT(offset)
            self.finaleBrainstormSequence.start()

        self.sayFaceoffTaunt(True, SafezoneInvasionGlobals.FinaleSuitPhrases[2])
        self.play('effort')

    def exitFinaleBrainstormAttack(self):
        if self.finaleBrainstormSequence:
            self.finaleBrainstormSequence.finish()
            self.finaleBrainstormSequence = None
        
    def enterFinaleStompAttack(self, offset):
        self.finaleAttackJump = Sequence(
            ActorInterval(self, 'jump', startFrame=0, endFrame=18),
            Func(base.playSfx, self.quakeLiftSfx),
            ActorInterval(self, 'jump', startFrame=18, endFrame=20),
            ActorInterval(self, 'jump', startFrame=97, endFrame=111),
            Func(base.playSfx, self.quakeLandSfx),
            ActorInterval(self, 'jump', startFrame=112, endFrame=138),
        )
        self.finaleStompSequence = Sequence(
            Func(self.sayFaceoffTaunt, True, 'ENOUGH!', dialogue = self.speechGruntSfx),
            Wait(1.25),
            Func(self.finaleAttackJump.start, offset),
            Wait(1.5),
            Func(self.applyShakeAttack, base.localAvatar, SafezoneInvasionGlobals.FinaleSuitAttackDamage),
            )
        self.finaleStompSequence.setT(offset)
        self.finaleStompSequence.start()

    def exitFinaleStompAttack(self):
        self.finaleAttackJump.finish()
        self.finaleStompSequence.finish()