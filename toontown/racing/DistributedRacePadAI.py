from direct.directnotify import DirectNotifyGlobal
from toontown.racing.DistributedKartPadAI import DistributedKartPadAI
from toontown.racing.DistributedRaceAI import DistributedRaceAI
from toontown.racing import RaceGlobals
from direct.fsm.FSM import FSM
from direct.distributed.ClockDelta import *
from direct.task import *

#TODO - change race type

class DistributedRacePadAI(DistributedKartPadAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedRacePadAI")
    defaultTransitions = {'Off': ['WaitEmpty'],
     'WaitEmpty': ['WaitCountdown', 'Off'],
     'WaitCountdown': ['WaitEmpty',
                       'WaitBoarding',
                       'Off',
                       'AllAboard'],
     'WaitBoarding': ['AllAboard', 'WaitEmpty', 'Off'],
     'AllAboard': ['Off', 'WaitEmpty', 'WaitCountdown']}
    
    def __init__(self, air):
        DistributedKartPadAI.__init__(self, air)
        FSM.__init__(self, 'DistributedRacePadAI')
        self.air = air
        self.trackId, self.trackType = [None, None]
        self.lastTime = globalClockDelta.getRealNetworkTime()
        self.shouldStart = False
        self.index = -1
        self.nameType = 'urban'
        
    def generate(self):
        DistributedKartPadAI.generate(self) 
        self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())
        
    def enterOff(self):
        pass
    
    def exitOff(self):
        pass
    
    def enterWaitEmpty(self):
        for block in self.startingBlocks:
            block.b_setOccupied(0)
        self.shouldStart = False
        taskMgr.doMethodLater(30, DistributedRacePadAI.changeTrack, 'changeTrack%i' % self.doId, [self])
    
    def exitWaitEmpty(self):
        taskMgr.remove('changeTrack%i' % self.doId)
        
    def enterWaitCountdown(self):
        taskMgr.doMethodLater(2, DistributedRacePadAI.startRace, 'startRace%i' % self.doId, [self])
    
    def exitWaitCountdown(self):
        if self.newState != 'WaitBoarding':
            taskMgr.remove('startRace%i' % self.doId)
        
    def enterWaitBoarding(self):
        pass
    
    def exitWaitBoarding(self):
        pass
        
    def enterAllAboard(self):
        taskMgr.doMethodLater(2, DistributedRacePadAI.createRace, 'createRace%i' % self.doId, [self])
    
    def exitAllAboard(self):
        pass
    
    def changeTrack(self):
        nri = RaceGlobals.getNextRaceInfo(self.trackId, self.nameType, self.index)
        self.b_setTrackInfo([nri[0], nri[1]])
        taskMgr.doMethodLater(30, DistributedRacePadAI.changeTrack, 'changeTrack%i' % self.doId, [self])
    
    def updateTimer(self):
        hasAvatars = False
        for block in self.startingBlocks:
            if block.avId != 0:
                hasAvatars = True
                break
        if hasAvatars and self.state == 'WaitEmpty':
            self.b_setState('WaitCountdown', globalClockDelta.getRealNetworkTime())
        elif not hasAvatars and self.state == 'WaitCountdown':
            self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())
    
    def updateMovieState(self):
        if self.state == 'WaitBoarding' and self.shouldStart:
            for block in self.startingBlocks:
                if block.currentMovie != 0:
                    return
            self.startRace(True)
        else:
            for block in self.startingBlocks:
                if block.currentMovie != 0:
                    self.request('WaitBoarding')
                    return
            
    def startRace(self, ignore = False):
        if self.state != 'WaitCountdown' and not ignore:
            self.shouldStart = True
            return
        self.b_setState('AllAboard', globalClockDelta.getRealNetworkTime())
        
    def createRace(self):
        self.raceZone = self.air.allocateZone()
        avatars = []
        for block in self.startingBlocks:
            if block.avId != 0:
                avatars.append(block.avId)
                self.sendUpdateToAvatarId(block.avId, 'setRaceZone', [self.raceZone])
        race = DistributedRaceAI(self.air)
        race.setZoneId(self.raceZone)
        race.setTrackId(self.trackId)
        race.setRaceType(self.trackType)
        race.setCircuitLoop([])
        race.setAvatars(avatars)
        race.setStartingPlaces(range(len(avatars)))
        race.setLapCount(1)
        race.generateWithRequired(self.raceZone)
        self.b_setState('WaitEmpty', globalClockDelta.getRealNetworkTime())

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
        
    def setRaceZone(self, todo0):
        pass
        
    def getTrackInfo(self):
        return [self.trackId, self.trackType]
        
    def setTrackInfo(self, trackInfo):
        self.trackId, self.trackType = trackInfo
        
    def d_setTrackInfo(self, trackInfo):
        self.sendUpdate('setTrackInfo',  [trackInfo])
    
    def b_setTrackInfo(self, trackInfo):
        self.setTrackInfo(trackInfo)
        self.d_setTrackInfo(trackInfo)

