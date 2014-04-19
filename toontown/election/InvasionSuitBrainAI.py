import random
from pandac.PandaModules import *
from direct.fsm.FSM import FSM
from PathPlannerPoolAI import pool

# Individual suit behaviors...

# Attack a specific Toon.
class AttackBehavior(FSM):
    REASSESS_INTERVAL = 1.0

    def __init__(self, brain, toonId):
        FSM.__init__(self, 'AttackFSM')
        self.brain = brain
        self.toonId = toonId

        self._walkTask = None

    def getToon(self):
        # Convenience function to get the Toon, or None if they're gone.
        return self.brain.suit.invasion.getToon(self.toonId)

    def start(self):
        self.assessDistance()

    def assessDistance(self):
        # Check if we're within attacking distance away from the Toon. If so, we
        # can attack. Otherwise, we need to walk closer.
        toon = self.getToon()
        if toon is None:
            # No good! Toon is gone.
            self.brain.demand('Idle')
            return

        toonPos = Point2(toon.getComponentX(), toon.getComponentY())
        distance = (toonPos - self.brain.suit.getCurrentPos()).length()

        attackPrefer, attackMax = self.brain.getAttackRange()
        if distance < attackPrefer:
            self.demand('Attack')
        elif distance < attackMax:
            # We're close enough that we *could* attack, but let's try to get
            # within the preferred attacking distance. If this is not possible,
            # just attack now.

            # We can only update our walk-to if we're walking to begin with:
            if self.state == 'Walk':
                nav = True
                self.brain.navigateTo(toonPos.getX(), toonPos.getY(), attackPrefer)
            else:
                nav = False

            if not nav:
                # Yeah, can't get close. Attack!
                self.demand('Attack')
        elif self.state == 'Walk' and self.brain.finalWaypoint and \
             (self.brain.finalWaypoint - toonPos).length() < attackMax:
            return
        else:
            self.demand('Walk', toonPos.getX(), toonPos.getY())

    def onNavFailed(self):
        if self.state == 'Walk':
            self.demand('Attack')
        else:
            # Can't get there, Captain!
            self.brain.master.toonUnreachable(self.toonId)
            self.brain.demand('Idle')
            return


    def enterAttack(self):
        # Attack the Toon.
        self.brain.suit.attack(self.toonId)

    def enterWalk(self, x, y):
        # Walk state -- we try to get closer to the Toon. When we're
        # close enough, we switch to 'Attack'
        attackPrefer, attackMax = self.brain.getAttackRange()
        self.brain.navigateTo(x, y, attackMax)

        if self._walkTask:
            self._walkTask.remove()
        self._walkTask = taskMgr.doMethodLater(self.REASSESS_INTERVAL, self.__reassess,
                                               self.brain.suit.uniqueName('reassess-walking'))

    def __reassess(self, task):
        self.assessDistance()
        return task.again

    def exitWalk(self):
        if self._walkTask:
            self._walkTask.remove()

    def onArrive(self):
        if self.state != 'Walk':
            return
        # We've finished walking -- let's see if we're close enough to attack.
        self.assessDistance()

    def onAttackCompleted(self):
        if self.state != 'Attack':
            return
        self.brain.demand('Idle')

# Chase after a Toon relentlessly and keep attacking them.
# This behavior is used when a Toon manages to royally piss off the master.
class HarassBehavior(AttackBehavior):
    ATTACK_COOLDOWN = 3.0

    def onAttackCompleted(self):
        self.demand('AttackCooldown')

    def enterAttackCooldown(self):
        # Wait a little bit, then hunt them again.
        self.brain.suit.idle()
        self.__wait = taskMgr.doMethodLater(self.ATTACK_COOLDOWN, self.__waitOver,
                                            self.brain.suit.uniqueName('harass-cooldown'))

    def __waitOver(self, task):
        self.assessDistance()
        return task.done

    def exitAttackCooldown(self):
        self.__wait.remove()

# We got too close to another Cog and have to spread out a little...
class UnclumpBehavior(FSM):
    UNCLUMP_SCAN_RADIUS = 30
    UNCLUMP_MOVE_DISTANCE = 5
    UNCLUMP_WAIT_TIME = 1.0

    def __init__(self, brain):
        FSM.__init__(self, 'UnclumpFSM')

        self.brain = brain

    def start(self):
        moveVector = Vec2()

        # Scan for who else is where...
        ourSuit = self.brain.suit
        ourPos = ourSuit.getCurrentPos()
        for otherSuit in self.brain.suit.invasion.suits:
            if otherSuit == ourSuit:
                continue # It's us!

            otherPos = otherSuit.getCurrentPos()

            moveAway = ourPos - otherPos

            if moveAway.length() > self.UNCLUMP_SCAN_RADIUS:
                continue # Too far away to consider them.

            # Use an inverse square law to scale the "move away" vector.
            moveMag = 1.0/max(moveAway.lengthSquared(), 0.1)
            moveAway.normalize()
            moveAway *= moveMag

            # Add it to to our overall move direction.
            moveVector += moveAway

        # Which direction do we go?
        moveVector.normalize()
        x, y = ourPos + (moveVector * self.UNCLUMP_MOVE_DISTANCE)

        self.brain.navigateTo(x, y)
        # And we're walking!
        self.demand('Walking')

    def onNavFailed(self):
        # Hmm... Can't walk there. Let's just idle for a bit instead.
        self.demand('Wait')

    def enterWalking(self):
        pass # Do nothing, we just wait for onArrive and exit the behavior.

    def onArrive(self):
        if self.state == 'Walking':
            # Ah, here we are!
            self.brain.demand('Idle')

    def enterWait(self):
        self.brain.suit.idle()
        self._waitDelay = \
            taskMgr.doMethodLater(self.UNCLUMP_WAIT_TIME, self._doneWaiting,
                                  self.brain.suit.uniqueName('unclump-wait'))

    def _doneWaiting(self, task):
        self.brain.demand('Idle')
        return task.done

    def exitWait(self):
        self._waitDelay.remove()

class InvasionSuitBrainAI(FSM):
    PROXEMICS_INTERVAL = 0.5
    PERSONAL_SPACE = 5

    def __init__(self, suit):
        FSM.__init__(self, 'InvasionSuitBrainFSM')
        self.suit = suit
        self.master = self.suit.invasion.master

        self.behavior = None

        self.__proxemicsTask = None

        # For the nav system:
        self.__waypoints = []
        self.finalWaypoint = None

    def start(self):
        if self.state != 'Off':
            return

        self.demand('Idle')

    def stop(self):
        if self.state == 'Off':
            return
        self.demand('Off')

    def getAttackRange(self):
        # Returns a tuple: Preferred attack distance, maximum distance for an attack to work
        return 15.0, 25.0

    def enterOff(self):
        self.__stopProxemics()

    def exitOff(self):
        self.__startProxemics()

    def enterUnclump(self):
        self.__stopProxemics()

        self.behavior = UnclumpBehavior(self)
        self.behavior.start()

    def exitUnclump(self):
        self.__startProxemics()

        self.behavior.demand('Off')
        self.behavior = None

    def __startProxemics(self):
        if not self.__proxemicsTask:
            self.__proxemicsTask = \
                taskMgr.doMethodLater(self.PROXEMICS_INTERVAL, self.__proxemics,
                                      self.suit.uniqueName('proxemics'))

    def __stopProxemics(self):
        if self.__proxemicsTask:
            self.__proxemicsTask.remove()
            self.__proxemicsTask = None

    def __proxemics(self, task):
        # Proxemics: Maintain personal space. This works by yielding to the
        # higher-leveled (or, in the event of the same level, lower-ID'd) Cog.

        for otherSuit in self.suit.invasion.suits:
            if otherSuit == self.suit:
                continue # It's us!

            if otherSuit.getActualLevel() < self.suit.getActualLevel():
                # We outrank them, and do not yield to subordinates!
                continue
            elif (otherSuit.getActualLevel() == self.suit.getActualLevel() and
                  otherSuit.doId > self.suit.doId):
                # We may not outrank them, but our ID is lower - we were first!
                continue

            # Okay, we have to consider yielding to them. Are we too close?
            ourPos = self.suit.getCurrentPos()
            otherPos = otherSuit.getCurrentPos()

            if (ourPos - otherPos).length() < self.PERSONAL_SPACE:
                # Yeah, too close...
                self.demand('Unclump')
                return task.done

        return task.again

    def enterIdle(self):
        # Brain has nothing to do -- ask the master for orders:
        self.suit.idle()
        self.master.requestOrders(self)

    def enterAskAgain(self):
        # Brain has absolutely nothing to do. Let's ask the master again in a few seconds in case any toons become available.
        self.suit.idle()
        self._askDelay = \
        taskMgr.doMethodLater(10.0, self.demand,
                              self.suit.uniqueName('askingAgain'),
                              extraArgs=['Idle'])

    def exitAskAgain(self):
        self._askDelay.remove()

    def enterAttack(self, toonId):
        self.behavior = AttackBehavior(self, toonId)
        self.behavior.start()

    def exitAttack(self):
        self.behavior.demand('Off')
        self.behavior = None

    def enterHarass(self, toonId):
        self.behavior = HarassBehavior(self, toonId)
        self.behavior.start()

    def exitHarass(self):
        self.behavior.demand('Off')
        self.behavior = None

    # Attacks:
    def suitFinishedAttacking(self):
        if hasattr(self.behavior, 'onAttackCompleted'):
            self.behavior.onAttackCompleted()

    # Navigation:
    def navigateTo(self, x, y, closeEnough=0):
        pool.plan(self.__navCallback, self.suit.getCurrentPos(), (x, y),
                  closeEnough)

    def __navCallback(self, result):
        self.__waypoints = result
        if self.__waypoints:
            self.finalWaypoint = Point2(self.__waypoints[-1])
            self.__walkToNextWaypoint()
        else:
            self.finalWaypoint = None
            if hasattr(self.behavior, 'onNavFailed'):
                self.behavior.onNavFailed()

    def suitFinishedWalking(self):
        # The suit finished walking. If there's another waypoint, go to it.
        # Otherwise, elevate the callback to suitFinishedNavigating.
        if self.__waypoints:
            self.__walkToNextWaypoint()
        else:
            self.suitFinishedNavigating()

    def suitFinishedNavigating(self):
        if hasattr(self.behavior, 'onArrive'):
            self.behavior.onArrive()

    def __walkToNextWaypoint(self):
        x, y = self.__waypoints.pop(0)
        self.suit.walkTo(x, y)
