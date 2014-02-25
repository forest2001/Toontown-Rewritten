from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from direct.task import Task

class DistributedHotAirBalloonAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHotAirBalloonAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.avId = 0
        self.stateTime = globalClockDelta.getRealNetworkTime()

    def b_setState(self, state, avId=0):
        if avId != self.avId:
            self.avId = avId
        self.setState(state)
        self.d_setState(state)

    def setState(self, state):
        self.demand(state)

    def d_setState(self, state):
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.sendUpdate('setState', [state, self.stateTime, self.avId])

    def getState(self):
        return (self.state, self.stateTime, self.avId)

    def enterOff(self):
        self.requestDelete()

    def enterWaiting(self):
        # We don't need to do anything on the AI...
        pass

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Waiting':
            self.notify.warning('Received unexpected requestEnter from avId %d!' % avId)
            return
        if self.avId == avId:
            return # Duplicate request?
        self.b_setState('Occupied', avId)

    def enterOccupied(self):
        # After 3.5 seconds, we take off!
        taskMgr.doMethodLater(3.5, self.b_setState, 'balloon-startride-task', extraArgs=['StartRide', self.avId])

    def enterStartRide(self):
        # After 22 seconds, the ride is over!
        taskMgr.doMethodLater(22, self.b_setState, 'balloon-riding-task', extraArgs=['RideOver', self.avId])

    def enterRideOver(self):
        # So that the client can handle events without instantly switching to the "Waiting" state...
        taskMgr.doMethodLater(2, self.b_setState, 'balloon-cleaningup-task', extraArgs=['Waiting'])
