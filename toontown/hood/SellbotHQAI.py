from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit import DistributedSuitPlannerAI
from toontown.coghq import DistributedFactoryElevatorExtAI

class SellbotHQAI(HoodAI):
    HOOD = ToontownGlobals.SellbotHQ

    def __init__(self, air):
        HoodAI.__init__(self, air)

        self.createZone()
    
    def createZone(self):
        HoodAI.createZone(self)
        
        mins = ToontownGlobals.FactoryLaffMinimums[0]
        self.testElev0 = DistributedFactoryElevatorExtAI.DistributedFactoryElevatorExtAI(self.air, self.air.factoryMgr, ToontownGlobals.SellbotFactoryInt, 0, antiShuffle=0, minLaff=mins[0])
        self.testElev0.generateWithRequired(ToontownGlobals.SellbotFactoryExt)
        self.testElev1 = DistributedFactoryElevatorExtAI.DistributedFactoryElevatorExtAI(self.air, self.air.factoryMgr, ToontownGlobals.SellbotFactoryInt, 1, antiShuffle=0, minLaff=mins[1])
        self.testElev1.generateWithRequired(ToontownGlobals.SellbotFactoryExt)
        
        #TODO: spawn VP lobby
        
        self.sp = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, self.HOOD)
        self.sp.generateWithRequired(self.HOOD)
        self.sp.d_setZoneId(self.HOOD)
        self.sp.initTasks()
        self.air.suitPlanners[self.HOOD] = self.sp