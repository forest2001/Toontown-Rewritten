import random
from direct.fsm.FSM import FSM

class InvasionSuitBrainAI(FSM):
    def __init__(self, suit):
        FSM.__init__(self, 'InvasionSuitBrainFSM')
        self.suit = suit

        self.__started = False

    def start(self):
        if self.__started:
            return
        self.__started = True

        self.demand('Walking')

    def enterWalking(self):
        self.chooseNewWalkPoint()
        taskMgr.doMethodLater(50, self.demand, self.suit.uniqueName('brainwalk'),
                              extraArgs=['Waiting'])

    def enterWaiting(self):
        self.suit.idle()
        taskMgr.doMethodLater(50, self.demand, self.suit.uniqueName('brainwait'),
                              extraArgs=['Walking'])

    def suitFinishedWalking(self):
        # The suit finished walking. The brain is expected to perform another
        # action.
        self.chooseNewWalkPoint()

    def chooseNewWalkPoint(self):
        x = random.randrange(-30, 30)
        y = random.randrange(-30, 30)
        self.suit.walkTo(x, y)
