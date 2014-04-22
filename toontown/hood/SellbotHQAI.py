from CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit import DistributedSuitPlannerAI
from toontown.coghq.DistributedFactoryElevatorExtAI import DistributedFactoryElevatorExtAI

class SellbotHQAI(CogHoodAI):
    HOOD = ToontownGlobals.SellbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.createZone()
    
    def createZone(self):
        CogHoodAI.createZone(self)
        
        # Create factory elevators.
        mins = ToontownGlobals.FactoryLaffMinimums[0]
        self.createElevator(DistributedFactoryElevatorExtAI, self.air.factoryMgr, ToontownGlobals.SellbotFactoryExt, ToontownGlobals.SellbotFactoryInt, 0, minLaff=mins[0])
        self.createElevator(DistributedFactoryElevatorExtAI, self.air.factoryMgr, ToontownGlobals.SellbotFactoryExt, ToontownGlobals.SellbotFactoryInt, 1, minLaff=mins[0])
        
        # TODO: VP boss battle.
        
        # Create Suit Planners in the cog playground and factory waiting area.
        self.createSuitPlanner(self.HOOD)
        # TODO: SuitPlanner doesn't spawn cogs correctly in factory waiting area.
        #self.createSuitPlanner(ToontownGlobals.SellbotFactoryExt)
