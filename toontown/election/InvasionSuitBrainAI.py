import random
from pandac.PandaModules import *
from direct.fsm.FSM import FSM
from InvasionPathDataAI import pathfinder

# Individual suit behaviors...

# Attack a specific Toon.
class AttackBehavior(FSM):
    REASSESS_INTERVAL = 2.0

    def __init__(self, brain, toonId):
        FSM.__init__(self, 'AttackFSM')
        self.brain = brain
        self.toonId = toonId

        self._walkingTo = None
        self._walkTask = None

    def getToon(self):
        # Convenience function to get the Toon, or None if they're gone.
        return self.brain.suit.air.doId2do.get(self.toonId)

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

        if distance < self.brain.getAttackRange():
            self.demand('Attack')
        elif self._walkingTo and (self._walkingTo - toonPos).length() < self.brain.getAttackRange():
            return
        else:
            self.demand('Walk', toonPos.getX(), toonPos.getY())

    def enterAttack(self):
        # Attack the Toon. TODO! For now, just exit silently.
        self.brain.suit.idle()
        self._attackDelay = taskMgr.doMethodLater(5.0, self.onAttackCompleted,
                                                  self.brain.suit.uniqueName('attack'),
                                                  extraArgs=[])

    def exitAttack(self):
        self._attackDelay.remove()

    def enterWalk(self, x, y):
        # Walk state -- we try to get closer to the Toon. When we're
        # close enough, we switch to 'Attack'
        if not self.brain.navigateTo(x, y, self.brain.getAttackRange()):
            # Can't get there, Captain!
            self.brain.master.toonUnreachable(self.toonId)
            self.brain.demand('Idle')
            return

        self._walkingTo = Point2(x, y)
        if self._walkTask:
            self._walkTask.remove()
        self._walkTask = taskMgr.doMethodLater(self.REASSESS_INTERVAL, self.__reassess,
                                               self.brain.suit.uniqueName('reassess-walking'))

    def __reassess(self, task):
        self.assessDistance()
        return task.again

    def exitWalk(self):
        self._walkingTo = None
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


class InvasionSuitBrainAI(FSM):
    def __init__(self, suit):
        FSM.__init__(self, 'InvasionSuitBrainFSM')
        self.suit = suit
        self.master = self.suit.invasion.master

        self.behavior = None

        # For the nav system:
        self.__waypoints = []

    def start(self):
        if self.state != 'Off':
            return

        self.demand('Idle')

    def stop(self):
        if self.state == 'Off':
            return
        self.demand('Off')

    def getAttackRange(self):
        return 20.0

    def enterIdle(self):
        # Brain has nothing to do -- ask the master for orders:
        self.suit.idle()
        self.master.requestOrders(self)

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

    def suitFinishedNavigating(self):
        if self.behavior:
            self.behavior.onArrive()

    # Navigation:
    def navigateTo(self, x, y, closeEnough=0):
        self.__waypoints = pathfinder.planPath(self.suit.getCurrentPos(),
                                               (x, y), closeEnough)
        if self.__waypoints:
            self.__walkToNextWaypoint()
            return True
        else:
            return False

    def suitFinishedWalking(self):
        # The suit finished walking. If there's another waypoint, go to it.
        # Otherwise, elevate the callback to suitFinishedNavigating.
        if self.__waypoints:
            self.__walkToNextWaypoint()
        else:
            self.suitFinishedNavigating()

    def __walkToNextWaypoint(self):
        x, y = self.__waypoints.pop(0)
        self.suit.walkTo(x, y)
