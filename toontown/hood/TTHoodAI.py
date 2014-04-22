from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.toon import NPCToons
#from toontown.election.DistributedElectionEventAI import DistributedElectionEventAI
from direct.task import Task
import time

class TTHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createZone(self):
        SZHoodAI.createZone(self)
        self.spawnObjects()
        self.butterflies = []
        self.createButterflies()

        if self.air.config.GetBool('want-doomsday', False):
            self.spawnElection()
    
    def spawnElection(self):
        election = self.air.doFind('ElectionEvent')
        if election is None:
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
        election.b_setState('Idle')
        # This is to make the election run every hour
        #self.__startElectionTick()
        
    def __startElectionTick(self):
        # Check seconds until next hour.
        ts = time.time()
        nextHour = 3600 - (ts % 3600)
        taskMgr.doMethodLater(nextHour, self.__electionTick, 'election-hourly')
        
    def __electionTick(self, task):
        # The next tick will occur in exactly an hour.
        task.delayTime = 3600
        # Check if we have toons in TTC...
        toons = self.air.doFindAll('DistributedToon')
        if not toons:
            # There are no toons online, just wait for the next hour.
            return task.again
        # Is there an invasion currently running?
        election = self.air.doFind('ElectionEvent')
        if election:
            state = election.getState()
            if state[0] == 'Idle':
                # There's already an Idle invasion, start it!
                taskMgr.doMethodLater(10, election.b_setState, 'election-start-delay', extraArgs=['Event'])
        if not election:
            # Create a new election object.
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
            election.b_setState('Idle')
            # Start the election after a 10 second delay.
            taskMgr.doMethodLater(10, election.b_setState, 'election-start-delay', extraArgs=['Event'])
        return task.again
            
    
    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                self.butterflies.append(butterfly)
