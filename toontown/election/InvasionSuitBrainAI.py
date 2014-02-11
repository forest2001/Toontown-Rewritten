import random
from direct.fsm.FSM import FSM

class InvasionSuitBrainAI(FSM):
    def __init__(self, suit):
        FSM.__init__(self, 'InvasionSuitBrainFSM')
        self.suit = suit

        self.__started = False

    def start(self):
        if self.state != 'Off':
            return

        self.demand('Walking')

    def stop(self):
        if self.state == 'Off':
            return
        self.demand('Off')

    def enterWalking(self):
        self.chooseNewWalkPoint()
        self._timeout = taskMgr.doMethodLater(50, self.demand,
                                              self.suit.uniqueName('brainwalk'),
                                              extraArgs=['Waiting'])

    def exitWalking(self):
        self._timeout.remove()

    def enterWaiting(self):
        self.suit.idle()
        self._timeout = taskMgr.doMethodLater(50, self.demand,
                                              self.suit.uniqueName('brainwait'),
                                              extraArgs=['Walking'])

    def exitWaiting(self):
        self._timeout.remove()

    def suitFinishedWalking(self):
        # The suit finished walking. The brain is expected to perform another
        # action.
        self.chooseNewWalkPoint()

    def chooseNewWalkPoint(self):
        x = random.randrange(-30, 30)
        y = random.randrange(-30, 30)
        self.suit.walkTo(x, y)
