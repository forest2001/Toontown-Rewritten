from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from direct.distributed.ClockDelta import *
import PartyGlobals

class DistributedPartyDanceActivityBaseAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyDanceActivityBaseAI")
    
    def __init__(self, air, parent, activityTuple):
        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)
        self.toons = []
        self.headings = []
        
    def generate(self):
        DistributedPartyActivityAI.generate(self)
        self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])

    def updateDancingToon(self, state, anim):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.toons:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to update their state while not dancing!')
            return
        self.sendUpdate('setDancingToonState', [avId, state, anim])

        
    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.toons:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to enter dance activity twice!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to interact with a party activity from a different district!')
            return
        self.toons.append(avId)
        self.headings.append(av.getH())
        self.sendUpdate('setToonsPlaying', [self.toons, self.headings])
        
    def toonExitRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.toons:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to exit a dance floor they\'re not on!')
            return
        index = self.toons.index(avId)
        self.toons.remove(avId)
        self.headings.pop(index)
        self.sendUpdate('setToonsPlaying', [self.toons, self.headings])