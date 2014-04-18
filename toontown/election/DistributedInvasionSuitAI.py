from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from direct.task.Task import Task
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.suit import SuitTimings
from toontown.battle import SuitBattleGlobals
import SafezoneInvasionGlobals
from InvasionSuitBase import InvasionSuitBase
from InvasionSuitBrainAI import InvasionSuitBrainAI
import SafezoneInvasionGlobals
from random import random, choice

class DistributedInvasionSuitAI(DistributedSuitBaseAI, InvasionSuitBase, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedInvasionSuitAI")

    def __init__(self, air, invasion):
        DistributedSuitBaseAI.__init__(self, air)
        InvasionSuitBase.__init__(self)
        FSM.__init__(self, 'InvasionSuitFSM')
        self.invasion = invasion

        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.spawnPointId = 0

        self.brain = InvasionSuitBrainAI(self)

        self.lastMarchTime = 0.0
        self.__walkTimer = None
        self.finale = False
        self._explodeDelay = None

    def announceGenerate(self):
        if self.spawnPointId == 99:
            x, y, z, h = SafezoneInvasionGlobals.FirstSuitSpawnPoint
        elif self.spawnPointId == 100:
            x, y, z, h = SafezoneInvasionGlobals.FinaleSuitSpawnPoint
        else:
            x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.freezeLerp(x, y)

        if self.invasion.state == 'Finale':
            self.walkSpeed = ToontownGlobals.SuitWalkSpeed # The Boss should walk slower than other high-level cogs
        else:
            self.walkSpeed = (ToontownGlobals.SuitWalkSpeed *
                              SuitBattleGlobals.SuitSizes[self.dna.name] / 4.0)

    def delete(self):
        DistributedSuitBaseAI.delete(self)
        self.demand('Off')

        self.brain.stop()
        try:
            self.invasion.suitDied(self)
        except Exception, e:
            self.notify.debug('Exception: %s' % e)

        if self._explodeDelay:
            self._explodeDelay.remove()


    '''
     STANDARD COGS                                                                                         
       The cogs have three main states: March, Attack, and Idle.                                              
       Standard Cogs find a toon to attack, then March towards them until the toon is gone or they have died. 
    '''
    def start(self):
        # Start the brain, if it hasn't been started already:
        self.brain.start()

    def idle(self):
        self.b_setState('Idle')

    def enterIdle(self):
        # We do nothing. We wait for the invasion manager to shift into the
        # 'Wave' state, and we all begin marching at once.
        pass

    def enterFlyDown(self):
        # We set a delay to wait for the Cog to finish flying down, then switch
        # states.
        if self.invasion.state == 'Finale':
            self.b_setInvasionFinale(True)

        self._delay = taskMgr.doMethodLater((SuitTimings.fromSky + 1.0), self.__flyDownComplete,
                                            self.uniqueName('fly-down-animation'))

    def __flyDownComplete(self, task):
        if self.invasion.state == 'Finale':
            self.b_setState('FinalePhrases')
            self.finaleMarchDelay = taskMgr.doMethodLater(10, self.startFinaleMarch, self.uniqueName('FinaleMarch-Later'))
            return

        self.b_setState('Idle')
        if self.invasion.state != 'BeginWave':
            self.start()

    def exitFlyDown(self):
        self._delay.remove()

    def walkTo(self, x, y):
        # Begin walking to a given point. It's OK to call this before the suit
        # finishes reaching its old waypoint; if that happens, the AI will
        # calculate the suit's current position and walk from there.
        oldX, oldY = self.getCurrentPos()
        self.b_setMarchLerp(oldX, oldY, x, y)
        self.__startWalkTimer()

        if self.state != 'March':
            self.b_setState('March')

    def __startWalkTimer(self):
        self.__stopWalkTimer()
        self.__walkTimer = taskMgr.doMethodLater(self._lerpDelay, self.__walkTimerOver,
                                                 self.uniqueName('walkTimer'))

    def __stopWalkTimer(self):
        if self.__walkTimer:
            self.__walkTimer.remove()
            self.__walkTimer = None

    def __walkTimerOver(self, task):
        if self.state != 'March':
            self.notify.warning('Walk timer ran out, but not in March state!')
            return
        self.brain.suitFinishedWalking()

    def enterMarch(self):
        pass

    def exitMarch(self):
        x, y = self.getCurrentPos()
        self.d_setStaticPoint(x, y, self._idealH)
        self.freezeLerp(x, y)

        self.__stopWalkTimer()

    def attack(self, who):
        attacks = ['clip-on-tie', 'redtape', 'newspaper', 'pink-slip', 'power-tie']
        damage = round(float(self.getActualLevel())/2.0)
        if damage <= 0:
            damage = 1
        self.sendUpdate('setAttackInfo', [who, choice(attacks), damage])
        self.b_setState('Attack')

    def enterAttack(self):
        if self.brain.suit.dna.body in ['a', 'b']:
            self._delay = taskMgr.doMethodLater(4.6, self.__attackDone,
                                                self.uniqueName('attack'))
        else:
            self._delay = taskMgr.doMethodLater(3.3, self.__attackDone,
                                                self.uniqueName('attack'))

    def __attackDone(self, task):
        self.brain.suitFinishedAttacking()
        return task.done

    def exitAttack(self):
        self._delay.remove()

    def getAttackInfo(self):
        return (0, '', 0) # This is only set dynamically.

    def takeDamage(self, hp):
        if self.state == 'FlyDown':
            return # We can't/shouldn't take damage in this state.

        hp = min(hp, self.currHP) # Don't take more damage than we have...
        self.b_setHP(self.currHP - hp)

        if self.finale:
            self.b_setHP(self.currHP + hp) # We dont want to big guy to die
            return

        if self.state != 'Stunned':
            self.b_setState('Stunned')

    def enterStunned(self):
        self.brain.stop()
        self._delay = taskMgr.doMethodLater(SuitTimings.suitStun, self.__unstun,
                                            self.uniqueName('stunned'))

    def __unstun(self, task):
        if self.finale:
            if self.currHP < 1:
                self.b_setState('Explode') # Done with him
            return

        if self.currHP < 1:
            # We're dead!
            self.b_setState('Explode')
        else:
            # Not dead, we can go back to thinking:
            self.demand('Idle')
            self.brain.start()

        return task.done

    def exitStunned(self):
        self._delay.remove()

    def enterExplode(self):
        self._explodeDelay = taskMgr.doMethodLater(SuitTimings.suitDeath, self.__exploded,
                                            self.uniqueName('explode'))

    def __exploded(self, task):
        self.requestDelete()

    def exitExplode(self):
        pass

    def getCurrentPos(self):
        return self.getPosAt(globalClock.getRealTime() - self.lastMarchTime)

    def setSpawnPoint(self, pointId):
        self.spawnPointId = pointId

    def getSpawnPoint(self):
        return self.spawnPointId

    def setMarchLerp(self, x1, y1, x2, y2):
        self.setLerpPoints(x1, y1, x2, y2)
        self.lastMarchTime = globalClock.getRealTime()

    def d_setMarchLerp(self, x1, y1, x2, y2):
        self.sendUpdate('setMarchLerp', [x1, y1, x2, y2,
                                         globalClockDelta.getRealNetworkTime()])

    def b_setMarchLerp(self, x1, y1, x2, y2):
        self.setMarchLerp(x1, y1, x2, y2)
        self.d_setMarchLerp(x1, y1, x2, y2)

    def d_setStaticPoint(self, x, y, h):
        self.sendUpdate('setStaticPoint', [x, y, h])

    def d_sayFaceoffTaunt(self, custom = False, phrase = ""):
        self.sendUpdate('sayFaceoffTaunt', [custom, phrase])

    def d_makeSkelecog(self):
        self.sendUpdate('makeSkelecog', [])

    def setState(self, state):
        self.demand(state)

    def d_setState(self, state):
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.sendUpdate('setState', [state, self.stateTime])

    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)

    def getState(self):
        return (self.state, self.stateTime)


    '''
     MOVER AND SHAKERS
       Mover and Shakers are the same as standard cogs, though they stomp the ground as they march.
       Toons within a certain radius of them will lose laff, forcing them to hit them from a distance.
    '''
    def takeShakerDamage(self, damage):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)
        if not toon:
            self.air.writeServerEvent('suspicious', avId, 'Nonexistent Toon tried to get hit!')
            return
        if toon.getHp() > 0:
            toon.takeDamage(damage)


    '''
     THE INVASION FINALE
      To end the invasion, we send in the Boss of it. He brainstorms ideas and occasionally loses his temper.
      The appears to take damage but actually takes none, as his death is a scripted sequence.
    '''
    def b_setInvasionFinale(self, finale):
        self.setInvasionFinale(finale)
        self.d_setInvasionFinale(finale)
        
    def setInvasionFinale(self, finale):
        self.finale = finale
        
    def d_setInvasionFinale(self, finale):
        self.sendUpdate('setInvasionFinale', [finale])
        
    def getInvasionFinale(self):
        return self.finale

    def startFinaleMarch(self, task):
        self.finaleMarch = taskMgr.add(self.enterFinaleMarch, self.uniqueName('FinaleMarch'))
        self.finaleDestinationPoint = 0
        self.finaleX, self.finaleY = SafezoneInvasionGlobals.FinaleSuitDestinations[0]
        self.finaleNextX, self.finaleNextY = SafezoneInvasionGlobals.FinaleSuitDestinations[1]
        self.brain.navigateTo(self.finaleX, self.finaleY)
        self.finaleAttack = taskMgr.doMethodLater(3, self.doFinaleAttack, self.uniqueName('FinaleAttack-Later'))

    def enterFinaleMarch(self, task):
        oldX, oldY = self.getCurrentPos()
        finalX, finalY, = SafezoneInvasionGlobals.FinaleSuitDestinations[4]
        if (self.finaleX - 1.0 <= oldX <= self.finaleX + 1.0) and (self.finaleY - 1.0 <= oldY <= self.finaleY + 1.0): # Check if it hit its destination
            if (self.finaleX - 1.0 <= finalX <= self.finaleX + 1.0) and (self.finaleY - 1.0 <= finalY <= self.finaleY + 1.0): # Check if it hit the final destination
                self.invasion.election.b_setState('WrapUp')
                self.d_sayFaceoffTaunt(True, SafezoneInvasionGlobals.FinaleSuitPhrases[6])
                self.idle()
                self.finaleAttack.remove()
                taskMgr.remove('FinaleAttack-Later')
                return task.done
            else:
                self.finaleDestinationPoint = self.finaleDestinationPoint + 1
                self.finaleX, self.finaleY = SafezoneInvasionGlobals.FinaleSuitDestinations[self.finaleDestinationPoint]
                self.brain.navigateTo(self.finaleX, self.finaleY)
                return task.cont
        return task.cont

    def enterFinalePhrases(self):
        pass

    def doFinaleAttack(self, task):
        if random() < 0.5:
            self.b_setState('FinaleBrainstormAttack')
        else:
            self.b_setState('FinaleStompAttack')

    def enterFinaleBrainstormAttack(self):
        self.brain.stop()
        self._stormDelay = taskMgr.doMethodLater(10.0, self.__finaleAttackDone, self.uniqueName('BrainstormAttackExit'))

    def exitFinaleBrainstormAttack(self):
        self._stormDelay.remove()

    def enterFinaleStompAttack(self):
        self.brain.stop()
        self._stompDelay = taskMgr.doMethodLater(5.5, self.__finaleAttackDone, self.uniqueName('StompAttackExit'))

    def exitFinaleStompAttack(self):
        self._stompDelay.remove()

    def __finaleAttackDone(self, task):
        self.brain.navigateTo(self.finaleX, self.finaleY)
        self.finaleAttack = taskMgr.doMethodLater(SafezoneInvasionGlobals.FinaleSuitAttackDelay, self.doFinaleAttack, self.uniqueName('FinaleAttack-Later'))
        return task.done
