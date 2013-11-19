from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *

class DistributedDoomsdayEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDoomsdayEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DoomsdayFSM')

        self.stateTime = globalClockDelta.getRealNetworkTime()

    def enterOff(self):
        pass

    def enterIntro(self):
        pass

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


@magicWord()
def doomsday(state):
    event = simbase.air.doFind('DoomsdayEvent')
    if event is None:
        return 'No Doomsday event created'

    if not hasattr(event, 'enter'+state):
        return 'Invalid state'

    event.b_setState(state)

    return 'Doomsday event now in %r state' % state
