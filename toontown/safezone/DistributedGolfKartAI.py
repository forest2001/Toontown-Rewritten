from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM

class DistributedGolfKartAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfKartAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedGolfKartAI')
        self.air = air
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.startingPos = None
        self.startingHpr = None
    
    def announceGenerate(self):
        self.b_setState('WaitEmpty', globalClockDelta.networkToLocalTime(globalClockDelta.getRealNetworkTime()))
        #pass
    
    def setState(self, state, timeStamp):
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.request(state)
    
    def d_setState(self, state, timeStamp):
        self.sendUpdate('setState', [state, timeStamp])
    
    def b_setState(self, state, timeStamp):
        self.setState(state, timeStamp)
        self.d_setState(state, timeStamp)
    
    def getState(self):
        return [self.state, self.lastTime]

    def fillSlot0(self, todo0):
        pass

    def fillSlot1(self, todo0):
        pass

    def fillSlot2(self, todo0):
        pass

    def fillSlot3(self, todo0):
        pass

    def emptySlot0(self, todo0, todo1):
        pass

    def emptySlot1(self, todo0, todo1):
        pass

    def emptySlot2(self, todo0, todo1):
        pass

    def emptySlot3(self, todo0, todo1):
        pass

    def requestBoard(self):
        pass

    def requestBoard(self): #stolen from trolley, clean it
        avId = self.air.getAvatarIdFromSender()

        if avId in self.slots:
            self.air.writeServerEvent('suspicious', avId, 'Toon requested to board a trolley twice!')
            self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])
            return

        slot = self.getBoardingSlot()
        if slot == -1:
            self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])
            return

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.removeFromTrolley, extraArgs=[avId])

        self.sendUpdate('emptySlot%d' % slot, [0, globalClockDelta.getRealNetworkTime()])
        self.sendUpdate('fillSlot%d' % slot, [avId])
        self.slots[slot] = avId

        if self.state == 'WaitEmpty':
            self.b_setState('WaitCountdown')

    def requestExit(self): #stolen from trolley, clean it
        avId = self.air.getAvatarIdFromSender()

        if avId not in self.slots:
            self.air.writeServerEvent('suspicious', avId, 'Toon requested to exit a trolley they are not on!')
            return

        if not self.boardable:
            # Trolley's leaving, can't hop off!
            return

        self.removeFromTrolley(avId, True)
        
    def removeFromTrolley(self, avId, hopOff=False): #just guess...
        if avId not in self.slots:
            return

        self.ignore(self.air.getAvatarExitEvent(avId))

        slot = self.slots.index(avId)
        self.sendUpdate('fillSlot%d' % slot, [0])
        if hopOff:
            # FIXME: Is this the correct way to make sure that the emptySlot
            # doesn't persist, yet still animate the avId hopping off? There
            # should probably be a timer that sets the slot to 0 after the
            # hopoff animation finishes playing. (And such a timer will have to
            # be canceled if another Toon occpuies the same slot in that time.)
            self.sendUpdate('emptySlot%d' % slot, [avId, globalClockDelta.getRealNetworkTime()])
        self.sendUpdate('emptySlot%d' % slot, [0, globalClockDelta.getRealNetworkTime()])
        self.slots[slot] = None

        if self.state == 'WaitCountdown' and self.slots.count(None) == 4:
            self.b_setState('WaitEmpty')

    def setMinigameZone(self, todo0, todo1):
        pass

    def setGolfZone(self, golfZone):
        self.golfZone = golfZone
        
    def d_setGolfZone(self, golfZone):
        self.sendUpdate('setGolfZone', [golfZone])
        
    def b_setGolfZone(self, golfZone):
        self.setGolfZone(golfZone)
        self.d_setGolfZone(golfZone)
        
    def getGolfZone(self):
        return self.golfZone

    def setGolfCourse(self, golfCourse):
        self.golfCourse = golfCourse
        
    def d_setGolfCourse(self, golfCourse):
        self.sendUpdate('setGolfCourse', [golfCourse])
        
    def b_setGolfCourse(self, golfCourse):
        self.setGolfCourse(golfCourse)
        self.d_setGolfCourse(golfCourse)
        
    def getGolfCourse(self):
        return self.golfCourse

    def setPosHpr(self, x, y, z, h, p, r):
        self.startingPos = Vec3(x, y, z)
        self.enteringPos = Vec3(x, y, z - 10)
        self.startingHpr = Vec3(h, 0, 0)
        
    def d_setPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setPosHpr', [[x, y, z, h, p, r]])

    def b_setPosHpr(self, x, y, z, h, p, r):
        self.setPosHpr(x, y, z, h, p, r)
        self.d_setPosHpr(x, y, z, h, p, r)
        
    def getPosHpr(self):
        return [self.startingPos[0], self.startingPos[1], self.startingPos[2], self.startingHpr[0], self.startingHpr[1], self.startingHpr[2]]

    def setColor(self, todo0, todo1, todo2):
        pass
        
    def getColor(self):
        return [1,1,1] #lol dividing by 0 on the client
