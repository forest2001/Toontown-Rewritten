from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI

class DistributedElectionEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElectionEventAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ElectionFSM')
        self.air = air
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.pieTypeAmount = [4, 20, 1]

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
        self.sendUpdate('flippySpeech', [avId, 1]) # 1 = Pie Request
        
    def phraseSaidToFlippy(self, phraseId):
        # Someone said something (relavent) to Flippy!
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Someone tried to talk to Flippy while they aren\'t on the district!')
            return
        self.sendUpdate('flippySpeech', [avId, phraseId])
            
    def enterIntro(self):
        # Generate Slappy's Hot Air Balloon!
        self.balloon = DistributedHotAirBalloonAI(self.air)
        self.balloon.generateWithRequired(self.zoneId)
        self.balloon.b_setState('Waiting')

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
