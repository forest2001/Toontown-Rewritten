from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.racing.DistributedVehicleAI import DistributedVehicleAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM

class DistributedRaceAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedRaceAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedRaceAI')
        self.air = air
        self.zoneId = 0
        self.trackId = 0
        self.raceType = 0
        self.circuitLoop = []
        self.avatars = []
        self.startingPlaces = []
        self.avatarKarts = []
        self.lapCount = 1
    
    def generate(self):
        self.request('Join')
        
    def enterJoin(self):
        self.beginBarrier('waitingForJoin', self.avatars, 60, self.joinBarrierCallback)
        self.d_waitingForJoin()
        
    def exitJoin(self):
        pass
        
    def enterPrep(self):
        self.beginBarrier('waitingForReady', self.avatars, 60, self.readyBarrierCallback)
        self.d_prepForRace()
        
    def exitPrep(self):
        pass
        
    def enterTutorial(self):
        self.beginBarrier('readRules', self.avatars, 30, self.readRulesCallback)
        self.d_startTutorial()
    
    def exitTutorial(self):
        pass
        
    def enterStart(self):
        self.d_startRace()
        for avatarKart in self.avatarKarts:
            kart = self.air.doId2do[avatarKart[1]]
            kart.sendUpdate('setInput', [1])
    
    def exitStart(self):
        pass
    
    def readyBarrierCallback(self, avatars):
        self.request('Tutorial')
        
    def readRulesCallback(self, avatars):
        self.request('Start')
    
    def joinBarrierCallback(self, avatars):
        self.avatars = avatars
        for av in avatars:
            kart = DistributedVehicleAI(self.air, av)
            kart.generateWithRequired(self.zoneId)
            self.avatarKarts.append([av, kart.getDoId()])
        self.beginBarrier('waitingForPrep', self.avatars, 60, self.prepBarrierCallback)
        self.sendUpdate('setEnteredRacers', [self.avatarKarts])
        
    def prepBarrierCallback(self, avatars):
        self.request('Prep')

    
    def setZoneId(self, zoneId):
        self.zoneId = zoneId
        
    def d_setZoneId(self, zoneId):
        self.sendUpdate('setZoneId', [zoneId])
    
    def b_setZoneId(self, zoneId):
        self.setZoneId(zoneId)
        self.d_setZoneId(zoneId)
    
    def getZoneId(self):
        return self.zoneId

    def setTrackId(self, trackId):
        self.trackId = trackId
        
    def getTrackId(self):
        return self.trackId

    def setRaceType(self, raceType):
        self.raceType = raceType
    
    def getRaceType(self):
        return self.raceType
    
    def setCircuitLoop(self, circuitLoop):
        self.circuitLoop = circuitLoop
        
    def getCircuitLoop(self):
        return self.circuitLoop

    def setAvatars(self, avatarList):
        self.avatars = avatarList
        
    def getAvatars(self):
        return self.avatars

    def setStartingPlaces(self, startingPlaces):
        self.startingPlaces = startingPlaces
        
    def getStartingPlaces(self):
        return self.startingPlaces

    def setLapCount(self, lapCount):
        self.lapCount = lapCount
        
    def getLapCount(self):
        return self.lapCount

    def waitingForJoin(self):
        self.beginBarrier('waitingForJoin', self.avatars, 60, self.b_prepForRace)
    
    def d_waitingForJoin(self):
        self.sendUpdate('waitingForJoin', [])
        
    def b_waitingForJoin(self):
        self.waitingForJoin()
        self.d_waitingForJoin()

    def setEnteredRacers(self, todo0):
        pass
    
    
    def d_prepForRace(self):
        self.sendUpdate('prepForRace', [])
    
    def b_prepForRace(self, avatars):
        self.prepForRace()
        self.d_prepForRace()
    
    def startTutorial(self):
        self.beginBarrier('readRules', self.avatars, 60, self.raceStart)
    
    def d_startTutorial(self):
        self.sendUpdate('startTutorial', [])
    
    def b_startTutorial(self, avatars):
        self.startTutorial()
        self.d_startTutorial()

    def startRace(self, startTime):
        pass
    
    
    def d_startRace(self):
        self.sendUpdate('startRace', [globalClockDelta.getRealNetworkTime()])
    
    def goToSpeedway(self, todo0, todo1):
        pass

    def genGag(self, todo0, todo1, todo2):
        pass

    def dropAnvilOn(self, todo0, todo1, todo2):
        pass

    def shootPiejectile(self, todo0, todo1, todo2):
        pass

    def racerDisconnected(self, todo0):
        pass

    def setPlace(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9):
        pass

    def setCircuitPlace(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def endCircuitRace(self):
        pass

    def setRaceZone(self, todo0, todo1):
        pass

    def hasGag(self, todo0, todo1, todo2):
        pass

    def racerLeft(self, todo0):
        pass

    def heresMyT(self, todo0, todo1, todo2, todo3):
        pass

    def requestThrow(self, todo0, todo1, todo2):
        pass

    def requestKart(self):
        pass
        avId = self.air.getAvatarIdFromSender()
        accId = self.air.getAccountIdFromSender()
        if not avId in self.avatars:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to request kart in race they\'re not in!')
            return
        for i in range(len(self.avatarKarts)):
            if self.avatarKarts[i][0] == avId:
                self.air.doId2do[self.avatarKarts[i][1]].request('Controlled', avId, accId)
