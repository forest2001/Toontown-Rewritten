from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.suit import SuitTimings
import SafezoneInvasionConstants
from InvasionSuitBase import InvasionSuitBase

class DistributedInvasionSuitAI(DistributedSuitBaseAI, InvasionSuitBase, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedInvasionSuitAI")

    def __init__(self, air, invasion):
        DistributedSuitBaseAI.__init__(self, air)
        InvasionSuitBase.__init__(self)
        FSM.__init__(self, 'InvasionSuitFSM')
        self.invasion = invasion

        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.spawnPointId = 0

    def announceGenerate(self):
        x, y, z, h = SafezoneInvasionConstants.SuitSpawnPoints[self.spawnPointId]
        self.freezeLerp(x, y)

    def enterFlyDown(self):
        # We set a delay to wait for the Cog to finish flying down, then switch
        # states.
        self._delay = taskMgr.doMethodLater(SuitTimings.fromSky, self.__flyDownComplete,
                                            self.uniqueName('fly-down-animation'))

    def __flyDownComplete(self, task):
        if self.invasion.state == 'BeginWave':
            self.b_setState('Idle')
        else:
            self.b_setState('March')

    def exitFlyDown(self):
        self._delay.remove()

    def enterIdle(self):
        # We do nothing. We wait for the invasion manager to shift into the
        # 'Wave' state, and we all begin marching at once.
        pass

    def enterMarch(self):
        # Right now, no AI logic for this... Instead, we'll move at a diagonal for debugging.
        x, y = self.getPosAt(0)
        self.sendUpdate('setMarchLerp', [x, y, x-50, y+25, globalClockDelta.getRealNetworkTime()])

    def setSpawnPoint(self, pointId):
        self.spawnPointId = pointId

    def getSpawnPoint(self):
        return self.spawnPointId

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
