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
import random

class DistributedInvasionSuit(DistributedSuitBase, InvasionSuitBase, FSM):
    def __init__(self, cr):
        DistributedSuitBase.__init__(self, cr)
        InvasionSuitBase.__init__(self)
        FSM.__init__(self, 'InvasionSuitFSM')

        self.spawnPointId = 0
        self.moveTask = None

        self._lerpTimestamp = 0
        self._turnInterval = None
        self._staticPoint = (0, 0, 0)

        self.attackTarget = 0
        self.attackProp = ''
        self.attackDamage = 0
        self.msStompLoop = None

    def delete(self):
        self.demand('Off')

        self.stopMoveTask()
        DistributedSuitBase.delete(self)

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

        if self.style.name == 'ms':
            taskMgr.add(self.__checkToonsInRadius, 'ShakerAttack', extraArgs=[])

    def generateAnimDict(self):
        animDict = DistributedSuitBase.generateAnimDict(self)

        # Movers and Shakers should stomp when walking
        if self.style.name == 'ms':
            animDict['walk'] = 'phase_5/models/char/suitB-stomp'
        # Suit C's throw animation is in a different phase
        if self.style.body == 'c':
            animDict['throw-paper'] = 'phase_3.5/models/char/suitC-throw-paper'
        else:
            animDict['throw-paper'] = 'phase_5/models/char/suit%s-throw-paper' % (self.style.body.upper())
        return animDict

    def setSpawnPoint(self, spawnPointId):
        self.spawnPointId = spawnPointId
        if self.spawnPointId == 99:
            x, y, z, h = SafezoneInvasionGlobals.FirstSuitSpawnPoint
        else:
            x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.freezeLerp(x, y)
        self.setPos(x, y, z)
        self.setH(h)
        

    def setHP(self, hp):
        currHP = getattr(self, 'currHP', 0)
        if currHP > hp:
            self.showHpText(hp - currHP)

        DistributedSuitBase.setHP(self, hp)

        self.updateHealthBar(0, 1)

    def setState(self, state, timestamp):
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def setStaticPoint(self, x, y, h):
        self._staticPoint = (x, y, h)
        if self.state != 'March':
            self.__moveToStaticPoint()

    def sayFaceoffTaunt(self, custom = False, phrase = ""):
        if custom == True:
            self.setChatAbsolute(phrase, CFSpeech | CFTimeout)
        elif custom == False:
            if random.random() < 0.2:
                taunt = SuitBattleGlobals.getFaceoffTaunt(self.getStyleName(), self.doId, randomChoice = True)
                self.setChatAbsolute(taunt, CFSpeech | CFTimeout)

    def makeSkelecog(self):
        self.setSkelecog(1)
        self.corpMedallion.hide()
        self.healthBar.show()

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

    def enterIdle(self, time):
        self.loop('neutral', 0)

    def enterMarch(self, time):
        if self.style.name == 'ms':
            self.msStartWalk = Sequence(
                Func(self.play, 'walk', fromFrame=0, toFrame=22),
                Wait(0.9),
                Parallel(Func(self.startMoveTask), Func(self.loop, 'walk', fromFrame=22, toFrame=62)))
            self.msStartWalk.start()
            stompSfx = loader.loadSfx('phase_5/audio/sfx/SA_tremor.ogg')
            self.msStompLoop = Sequence(SoundInterval(stompSfx, duration=1.6, startTime=0.3, volume=0.4, node=self))
            self.msStompLoop.loop()
        else:
            self.loop('walk', 0)
            self.startMoveTask()

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

    def enterStunned(self, time):
        self._stunInterval = ActorInterval(self, 'pie-small-react')
        self._stunInterval.start(time)

    def exitStunned(self):
        self._stunInterval.finish()

    def enterExplode(self, time):
        # We're done with our suit. Let's get rid of him and load an actor for the explosion
        loseActor = self.getLoseActor()
        loseActor.reparentTo(render)
        spinningSound = base.loadSfx('phase_3.5/audio/sfx/Cog_Death.ogg')
        deathSound = base.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')
        self.stash()

        # Oh boy, time to load all of our explosion effects!
        explosionInterval = ActorInterval(loseActor, 'lose', startFrame=0, endFrame=150)
        deathSoundTrack = Sequence(Wait(0.6), SoundInterval(spinningSound, duration=1.2, startTime=1.5, volume=0.2, node=loseActor), SoundInterval(spinningSound, duration=3.0, startTime=0.6, volume=0.8, node=loseActor), SoundInterval(deathSound, volume=0.32, node=loseActor))
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
        explosionTrack = Sequence()
        explosionTrack.append(Wait(5.4))
        explosionTrack.append(self.createKapowExplosionTrack(loseActor))
        gears1Track = Sequence(Wait(2.0), ParticleInterval(smallGears, loseActor, worldRelative=0, duration=4.3, cleanup=True), name='gears1Track')
        gears2MTrack = Track((0.0, explosionTrack), (0.7, ParticleInterval(singleGear, loseActor, worldRelative=0, duration=5.7, cleanup=True)), (5.2, ParticleInterval(smallGearExplosion, loseActor, worldRelative=0, duration=1.2, cleanup=True)), (5.4, ParticleInterval(bigGearExplosion, loseActor, worldRelative=0, duration=1.0, cleanup=True)), name='gears2MTrack')
        cleanupTrack = Track((6.5, Func(self.cleanupLoseActor))) # Better delete the poor guy when we're done
        explodeTrack = Parallel(explosionInterval, deathSoundTrack, gears1Track, gears2MTrack, cleanupTrack)
        explodeTrack.start(time)

    def enterAttack(self, time):
        if self.style.name == 'ms':
            self._attackInterval = self.makeShakerAttackTrack()
            self._attackInterval.start(time)
            return
        self._attackInterval = self.makeAttackTrack()
        self._attackInterval.start(time)

    def makeAttackTrack(self):
        # TODO: Add more props than the tie. Possibly more animations.
        prop = BattleProps.globalPropPool.getProp(self.attackProp)

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
        self.lookAtToon(self.attackTarget)

        if self.style.body in ['a', 'b']:
            throwDelay = 3
        elif self.style.body == 'c':
            throwDelay = 2.3

        def throwProp():
            toon = self.cr.doId2do.get(toonId)
            if not toon:
                prop.cleanup()
                prop.removeNode()
                return

            prop.wrtReparentTo(render)

            hitPos = toon.getPos() + Vec3(0, 0, 2.5)
            distance = (prop.getPos() - hitPos).length()
            speed = 50.0

            Sequence(prop.posInterval(distance/speed, hitPos),
                     Func(prop.cleanup),
                     Func(prop.removeNode)).start()

        track = Parallel(
            ActorInterval(self, 'throw-paper'),
            Track(
                (0.4, Func(prop.reparentTo, self.getRightHand())),
                (0.0, Func(prop.setPosHpr, 0.1, 0.2, -0.35, 0, 336, 0)),
                (0.0, Func(self.sayFaceoffTaunt)),
                (throwDelay, Func(throwProp)),
                (10.0, Func(prop.cleanup)),
                (10.0, Func(prop.removeNode)) # Ensure cleanup
            ),
        )

        return track

    def makeShakerAttackTrack(self):
        self.lookAtToon(self.attackTarget)
        track = Parallel(
            ActorInterval(self, 'walk'),
            Track(
                (0.0, Func(self.sayFaceoffTaunt))
            ),
        )

        return track

    def lookAtToon(self, toonId):
        toon = self.cr.doId2do.get(toonId)
        if toon:
            self.lookAt(toon)

    def exitAttack(self):
        self._attackInterval.finish()

    def setAttackInfo(self, targetId, attackProp, attackDamage):
        self.attackTarget = targetId
        self.attackProp = attackProp
        self.attackDamage = attackDamage

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

    def exitMarch(self):
        self.loop('neutral', 0)
        self.stopMoveTask()
        if self.msStompLoop:
            self.msStompLoop.finish()
        self.__moveToStaticPoint()

    def startMoveTask(self):
        if self.moveTask:
            return
        self.moveTask = taskMgr.add(self.__move, self.uniqueName('move-task'))

    def stopMoveTask(self):
        if self.moveTask:
            self.moveTask.remove()
            self.moveTask = None

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

    # Move Shaker
    def __checkToonsInRadius(self):
        toon = base.localAvatar
        if toon:
            toonDistance = toon.getPos().length()
            if self.getPos().length() < toonDistance < (self.getPos().length() + SafezoneInvasionGlobals.MoveShakerRadius):
                if toon.hp > -1:
                    if not toon.isStunned:
                        self.d_takeShakerDamage(SafezoneInvasionGlobals.MoveShakerDamageRadius, toon)
                        self.setToonStunned(toon, True)
                else:
                    # Dont try and enable avatar controls if a toon is sad
                    taskMgr.remove('EnableAvatarControls')
        return Task.cont

    def d_takeShakerDamage(self, damage, toon):
        if toon.isStunned:
            return
        if toon.hp > -1:
            if toon is base.localAvatar:
                base.localAvatar.disableAvatarControls()
                taskMgr.doMethodLater(1.5, base.localAvatar.enableAvatarControls, 'EnableAvatarControls', extraArgs = [])

            toon.b_setEmoteState(12, 1.0)
            
            self.sendUpdate('takeShakerDamage', [toon.doId, damage])

            taskMgr.doMethodLater(SafezoneInvasionGlobals.MoveShakerStunTime, self.setToonStunned, 'ToonStunned', extraArgs = [toon, False])

    def setToonStunned(self, toon, stunned = False):
        toon.isStunned = stunned
        if stunned == False:
            taskMgr.remove('ToonStunned')

