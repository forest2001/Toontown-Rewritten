from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from toontown.golf.DistributedGolfCourseAI import DistributedGolfCourseAI
from toontown.golf.DistributedGolfHoleAI import DistributedGolfHoleAI
from TrolleyConstants import *

class DistributedGolfKartAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfKartAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedGolfKartAI')
        self.air = air
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.slots = [None, None, None, None]
        self.golfCountdownTime = simbase.config.GetFloat('golf-countdown-time', TROLLEY_COUNTDOWN_TIME)
        self.color = [255, 255 , 255]
        self.startingPos = None
        self.startingHpr = None
        self.boardable = True
    
    def announceGenerate(self):
        self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())
    
    def setState(self, state, timeStamp):
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.request(state)
    
    def d_setState(self, state, timeStamp):
        state = state[:1].lower() + state[1:]
        self.sendUpdate('setState', [state, timeStamp])
    
    def b_setState(self, state, timeStamp):
        self.setState(state, timeStamp)
        self.d_setState(state, timeStamp)
    
    def getState(self):
        return [self.state, self.lastTime]


    def requestBoard(self): #stolen from trolley, clean it
        avId = self.air.getAvatarIdFromSender()

        #TEMPORARY
        #for slot in self.slots:
        #    if slot:
        #        self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])
        #        return
        
        if avId in self.slots:
            self.air.writeServerEvent('suspicious', avId, 'Toon requested to board a trolley twice!')
            self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])
            return

        slot = self.getBoardingSlot()
        if slot == -1:
            self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])
            return

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.removeFromKart, extraArgs=[avId])

        self.sendUpdate('emptySlot%d' % slot, [0, globalClockDelta.getRealNetworkTime()])
        self.sendUpdate('fillSlot%d' % slot, [avId])
        self.slots[slot] = avId

        if self.state == 'WaitEmpty':
            self.b_setState('WaitCountdown', globalClockDelta.getRealNetworkTime())

    def requestExit(self): #stolen from trolley, clean it
        avId = self.air.getAvatarIdFromSender()

        if avId not in self.slots:
            self.air.writeServerEvent('suspicious', avId, 'Toon requested to exit a trolley they are not on!')
            return

        if not self.boardable:
            # Trolley's leaving, can't hop off!
            return

        self.removeFromKart(avId, True)
        
    def removeFromKart(self, avId, hopOff=False): #just guess...
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
            self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())

    def getBoardingSlot(self):
        if not self.boardable:
            print 'rejecting, not boardable'
            return -1

        if None not in self.slots:
            print 'rejecting, no slot available'
            return -1

        return self.slots.index(None)
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

    def setColor(self, r, g, b):
        self.color = [r, g, b]
    
    def enterOff(self):
        pass
    
    def exitOff(self):
        pass
        
    def getColor(self):
        return self.color #lol dividing by 0 on the client
    
    def enterWaitEmpty(self):
        self.boardable = True
    
    def exitWaitEmpty(self):
        self.boardable = False
        
    def enterWaitCountdown(self):
        self.boardable = True
        self.departureTask = taskMgr.doMethodLater(self.golfCountdownTime, self.__depart, 'kartDepartureTask')

    def __depart(self, task):
        self.b_setState('Leaving', globalClockDelta.getRealNetworkTime())
        return task.done

    def exitWaitCountdown(self):
        taskMgr.remove(self.departureTask)
        self.boardable = False

    def enterLeaving(self):
        self.leavingTask = taskMgr.doMethodLater(TROLLEY_EXIT_TIME, self.__activateGolf, 'kartLeaveTask')

    def __activateGolf(self, task):
        players = [player for player in self.slots if player is not None]

        if players:
            # If all players disconnected while the KART was departing, the
            # players array would be empty. Therefore, we should only attempt
            # to create a GOLF GAME if there are still players.
            
            gg = self.createGolfGame(players)
            for player in players:
                self.sendUpdateToAvatarId(player, 'setGolfZone', gg)
                self.removeFromKart(player)

        self.b_setState('Entering', globalClockDelta.getRealNetworkTime())
        return task.done

    def createGolfGame(self, players):
        gameZone = self.air.allocateZone(owner=self)
        
        course = DistributedGolfCourseAI(self.air)
        course.setGolferIds(players)
        course.setCourseId(self.index)
        course.zone = gameZone
        course.generateWithRequired(gameZone)
        
                
        return [gameZone, self.index]
        
    def exitLeaving(self):
        taskMgr.remove(self.leavingTask)

    def enterEntering(self):
        self.enteringTask = taskMgr.doMethodLater(TROLLEY_ENTER_TIME, self.__doneEntering, 'kartEnterTask')

    def __doneEntering(self, task):
        self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())
        return task.done

    def exitEntering(self):
        taskMgr.remove(self.enteringTask)

