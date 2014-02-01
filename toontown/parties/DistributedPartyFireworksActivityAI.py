from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM
import PartyGlobals

class DistributedPartyFireworksActivityAI(DistributedPartyActivityAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyFireworksActivityAI")
    
    def __init__(self, air, parent, activityTuple):
        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)
        FSM.__init__(self, 'DistributedPartyActivityAI')
        self.state = 'Idle'

    def setEventId(self, todo0):
        return
        
    def getEventId(self):
        return PartyGlobals.FireworkShows.Summer

    def setShowStyle(self, todo0):
        pass
        
    def getShowStyle(self):
        return 0

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        host = self.air.doId2do[self.parent].hostId
        if avId == host and self.state == 'Idle':
            self.request('Active')
            return
        self.sendUpdateToAvatarId(avId, 'joinRequestDenied', [1])

    def enterActive(self):
        self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])
        
    def enterIdle(self):
        self.sendUpdate('setState', ['Idle', globalClockDelta.getRealNetworkTime()])