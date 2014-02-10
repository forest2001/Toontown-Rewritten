from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.suit import SuitTimings

class DistributedInvasionSuitAI(DistributedSuitBaseAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedInvasionSuitAI")

    def __init__(self, air):
        DistributedSuitBaseAI.__init__(self, air)
        FSM.__init__(self, 'InvasionSuitFSM')

        self.stateTime = globalClockDelta.getRealNetworkTime()

    def enterFlyDown(self):
        # We set a delay to wait for the Cog to finish flying down, then switch
        # states.
        self._delay = taskMgr.doMethodLater(SuitTimings.fromSky, self.__flyDownComplete,
                                            self.uniqueName('fly-down-animation'))

    def __flyDownComplete(self, task):
        self.demand('March')

    def exitFlyDown(self):
        self._delay.remove()

    def enterMarch(self):
        pass # Right now, no AI logic for this...

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
