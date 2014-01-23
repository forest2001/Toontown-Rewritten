from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.fsm.FSM import FSM

class DistributedAnimatedPropAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedAnimatedPropAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'AnimProp')
        self.state = 'Attract'
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.propId = 0
        self.currentAvatar = 0
        

    def setPropId(self, propId):
        self.propId = propId
        
    def getPropId(self):
        return self.propId

    def setAvatarInteract(self, avId):
        self.currentAvatar = avId
        
    def d_setAvatarInteract(self, avId):
        self.sendUpdate('setAvatarInteract', [avId])

    def b_setAvatarInteract(self, avId):
        self.setAvatarInteract(avId)
        self.d_setAvatarInteract(avId)
        
    def getAvatarInteract(self):
        return self.currentAvatar
        
    def requestInteract(self):
        avId = self.air.getAvatarIdFromSender()
        if self.currentAvatar != 0:
            self.sendUpdateToAvatarId(avId, 'rejectInteract', [])
            return
        elif self.state != 'Attract':
            self.sendUpdateToAvatarId(avId, 'rejectInteract', [])
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to interact with a non-attractive prop!')
            return
        self.b_setAvatarInteract(avId)
        self.b_setState('Playing')

    def rejectInteract(self):
        pass

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if self.currentAvatar != avId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to exit an animated prop they\'re not interacting with!')
            return
        self.sendUpdate('avatarExit', [avId])
        self.b_setState('Attract')
        
    def avatarExit(self, avId):
        pass

    def setState(self, state):
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.demand(state)
        
    def d_setState(self, state):
        self.sendUpdate('setState', [state.lower(), self.lastTime])
        
    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)
        
    def getState(self):
        return [self.state, self.lastTime]
    
    def enterPlaying(self):
        taskMgr.doMethodLater(8, self.b_setState, 'setState%d' % self.doId, ['Attract'])
    
    def enterAttract(self):
        self.b_setAvatarInteract(0)        

