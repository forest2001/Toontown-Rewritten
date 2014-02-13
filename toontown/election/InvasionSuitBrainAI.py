import random
from direct.fsm.FSM import FSM
from InvasionPathDataAI import pathfinder

class InvasionSuitBrainAI(FSM):
    def __init__(self, suit):
        FSM.__init__(self, 'InvasionSuitBrainFSM')
        self.suit = suit
        self.master = self.suit.invasion.master

        self.__started = False

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

    def enterIdle(self):
        # Brain has nothing to do -- ask the master for orders:
        self.suit.idle()
        self.master.requestOrders(self)

    def enterOff(self):
        # Brain is shutting down -- tell the master.
        pass # TODO

    def suitFinishedNavigating(self):
        pass

    # Navigation:
    def navigateTo(self, x, y):
        self.__waypoints = pathfinder.planPath(self.suit.getCurrentPos(),
                                               (x, y))
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
