from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from PartyGlobals import *
import time


"""
dclass DistributedParty : DistributedObject {
  setPartyClockInfo(uint8, uint8, uint8) required broadcast;
  setInviteeIds(uint32array) required broadcast;
  setPartyState(bool) required broadcast;
  setPartyInfoTuple(party) required broadcast;
  setAvIdsAtParty(uint32 []) required broadcast;
  setPartyStartedTime(string) required broadcast;
  setHostName(string) required broadcast;
  avIdEnteredParty(uint32) clsend airecv;
};
"""
class DistributedPartyAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyAI")

    def __init__(self, air, hostId, zoneId, info):
        DistributedObjectAI.__init__(self, air)
        self.hostId = hostId
        self.zoneId = zoneId
        self.info = info
        # buncha required crap
        PARTY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.startedAt = time.strftime(PARTY_TIME_FORMAT)
        self.partyClockInfo = (0,0,0)
        self.partyState = 0
        self.avIdsAtParty = []

        # We'll need to inform the UD later of the host's name so other public parties know the host. Maybe we know who he is..
        self.hostName = ''
        host = self.air.doId2do.get(self.hostId, None)
        if host:
            self.hostName = host.getName()

    def generate(self):
        DistributedObjectAI.generate(self)
        print 'regular generate called####'

    def getPartyClockInfo(self):
        return self.partyClockInfo

    def getInviteeIds(self):
        return self.info.get('inviteeIds', [])

    def getPartyState(self):
        return self.partyState

    def b_setPartyState(self, partyState):
        self.partyState = partyState
        self.sendUpdate('setPartyState', [partyState])

    def _formatParty(self, partyDict):
        start = partyDict['start']
        end = partyDict['end']
        return [partyDict['partyId'],
                partyDict['hostId'],
                start.tm_year,
                start.tm_mon,
                start.tm_mday,
                start.tm_hour,
                start.tm_min,
                end.tm_year,
                end.tm_mon,
                end.tm_mday,
                end.tm_hour,
                end.tm_min,
                partyDict['isPrivate'],
                partyDict['inviteTheme'],
                partyDict['activities'],
                partyDict['decorations'],
                PartyStatus.Started]

    def getPartyInfoTuple(self):
        return self._formatParty(self.info)

    def getAvIdsAtParty(self):
        return self.avIdsAtParty

    def getPartyStartedTime(self):
        return self.startedAt

    def getHostName(self):
        return self.hostName

    def avIdEnteredParty(self, avId):
        # Sent as the client DistributedParty announces generate
        pass

