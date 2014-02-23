from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from direct.task import Task

class HotAirBalloonFSM(FSM):
    def __init__(self, election):
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.election = election
        self.currentToon = 0
        self.stateTime = globalClockDelta.getRealNetworkTime()
    
    def enterWaiting(self):
        pass
        
    def enterStartBalloon(self):
        # The total duration of the travel + an extra few seconds.
        taskMgr.doMethodLater(26, self.election.b_setBalloonState, 'balloon-finish-timer', extraArgs=['Finished'])
        
    def enterFinished(self):
        self.currentToon = 0
        self.demand('Waiting')

class DistributedElectionEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElectionEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ElectionFSM')
        self.air = air
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.pieTypeAmount = [4, 20, 1]
        self.balloon = HotAirBalloonFSM(self)

    def enterOff(self):
        self.requestDelete()
    
    def setPieTypeAmount(self, type, num):
        # This is more for the invasion than the pre-invasion elections.
        self.pieTypeAmount = [type, num]
    
    def wheelbarrowAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Got a request for pies from a toon that isn\'t on the district!')
            return
        av.b_setPieType(self.pieTypeAmount[0])
        av.b_setNumPies(self.pieTypeAmount[1])
        av.b_setPieThrowType(self.pieTypeAmount[2])
    
    # All the HotAirBalloonFSM shit...
    def balloonAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Got a request to enter balloon from a toon that isn\'t on the district!')
            return
        if self.balloon.state != 'Waiting':
            # We aren't waiting for a toon. This can happen as a result of a race condition... 
            # e.g. high latency. Therefore it's not suspicious.
            print "cannot start: state currently %s" % self.balloon.state
            return
        self.balloon.currentToon = avId
        print "current avatar: %d" % avId
        self.b_setBalloonState('StartBalloon')
        
    def b_setBalloonState(self, state):
        print "setting state %s" % state
        self.setBalloonState(state)
        self.d_setBalloonState(state)
    
    def setBalloonState(self, state):
        self.balloon.demand(state)
       
    def d_setBalloonState(self, state):
        self.balloon.stateTime = globalClockDelta.getRealNetworkTime()
        if state == 'StartBalloon':
            self.sendUpdate('setBalloonStart', [self.balloon.currentToon, self.balloon.stateTime])
        else:
            self.sendUpdate('setBalloonState', [state, self.balloon.stateTime])
        
    def getBalloonState(self):
        return (self.balloon.state, self.balloon.stateTime)
        
    # Continue with DistributedElectionEventAI
            
    def enterIntro(self):
        pass

    def enterFlippyRunning(self):
        pass

    def enterFlippyWaving(self):
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
def election(state):
    event = simbase.air.doFind('ElectionEvent')
    if event is None:
        event = DistributedElectionEventAI(simbase.air)
        event.generateWithRequired(2000)

    if not hasattr(event, 'enter'+state):
        return 'Invalid state'

    event.b_setState(state)

    return 'Election event now in %r state' % state
