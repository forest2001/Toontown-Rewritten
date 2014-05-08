from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from direct.task import Task
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.toonbase import TTLocalizer
import PartyGlobals

class DistributedPartyTrampolineActivityAI(DistributedPartyActivityAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyTrampolineActivityAI")
    
    def __init__(self, air, parent, activityTuple):
        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)
        FSM.__init__(self, 'DistributedPartyTrampolineActivityAI')
        self.currentAv = 0
        self.record = 0
        self.jellybeans = []
        self.collected = 0
        
    def generate(self):
        self.demand('Idle')

    def awardBeans(self, numBeans, height):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currentAv:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to give beans while not using the trampoline!')
            return
        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to award beans while the game wasn\'t running!')
            return
        if numBeans != self.collected:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon reported incorrect number of collected jellybeans!')
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to award beans while not in district!')
            return
        reward = self.collected*2
        message = TTLocalizer.PartyTrampolineBeanResults % self.collected
        if self.collected == PartyGlobals.TrampolineNumJellyBeans:
            reward += PartyGlobals.TrampolineJellyBeanBonus
            message = TTLocalizer.PartyTrampolineBonusBeanResults % (self.collected, PartyGlobals.TrampolineJellyBeanBonus)
        message += '\n\n' + TTLocalizer.PartyTrampolineTopHeightResults % height
        # TODO: Pass a msgId(?) to the client so the client can use whatever localizer it chooses.
        # Ideally, we shouldn't even be passing strings that *should* be localized.
        self.sendUpdateToAvatarId(avId, 'showJellybeanReward', [reward, av.getMoney(), message])
        av.addMoney(reward)
        

    def reportHeightInformation(self, height):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to report height without being on the district!')
            return
        if height > self.record:
            self.record = height
            self.sendUpdate('setBestHeightInfo', [av.getName(), height])
        else:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon incorrectly reported height!')
            
    def enterActive(self):
        self.jellybeans = range(PartyGlobals.TrampolineNumJellyBeans)
        taskMgr.doMethodLater(PartyGlobals.TrampolineDuration, self.sendUpdate, 'exitTrampoline%d' % self.doId, extraArgs=['leaveTrampoline', []])
        self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])
        self.collected = 0
                        
    def enterIdle(self):
        self.sendUpdate('setState', ['Idle', globalClockDelta.getRealNetworkTime()])
        self.currentAv = 0
        self.updateToonsPlaying()
        
    def enterRules(self):
        self.sendUpdate('setState', ['Rules', globalClockDelta.getRealNetworkTime()])
        
    def requestAnim(self, anim):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to request an animation while not playing!')
            return
        if self.currentAv != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to request an anim for someone else!')
            return
        self.sendUpdate('requestAnimEcho', [anim])

    def removeBeans(self, beans):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to collect jellybeans while not playing!')
            return
        if self.currentAv != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to collect jellybeans while someone else was playing!')
            return
        for bean in beans:
            if not bean in self.jellybeans:
                self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to collect non-existent bean!')
                beans.remove(bean)
            else:
                self.collected += 1
        self.sendUpdate('removeBeansEcho', [beans])
        
    def updateToonsPlaying(self):
        if self.currentAv == 0:
            self.sendUpdate('setToonsPlaying', [[]])
            return
        self.sendUpdate('setToonsPlaying', [[self.currentAv]])

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if self.state == 'Active':
            self.sendUpdateToAvatarId(avId, 'joinRequestDenied', [1])
            return
        self.currentAv = avId
        self.updateToonsPlaying()
        self.demand('Rules')

    def toonExitRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to leave a trampoline that was not running!')
            return
        if self.currentAv != avId:  
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to exit trampoline for someone else!')
            return
        taskMgr.remove('exitTrampoline'%self.doId)
        self.sendUpdate('leaveTrampoline', [])

    def toonExitDemand(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currentAv:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to exit trampoline they\'re not using!')
            return
        self.demand('Idle')
        
    def toonReady(self):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Rules':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to verify rules while the rules were not running!')
            return
        if avId != self.currentAv:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to verify rules for someone else!')
            return
        self.demand('Active')
        


