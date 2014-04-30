from CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedSellbotBossAI import DistributedSellbotBossAI
from toontown.coghq.DistributedFactoryElevatorExtAI import DistributedFactoryElevatorExtAI
from toontown.building.DistributedVPElevatorAI import DistributedVPElevatorAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes


class SellbotHQAI(CogHoodAI):
    HOOD = ToontownGlobals.SellbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.createZone()
        
    def createDoor(self):
        interiorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.SellbotHQ, doorIndex=0)
        for i in range(4):
            exteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.SellbotLobby, doorIndex=i, lockValue=FADoorCodes.SB_DISGUISE_INCOMPLETE)
            exteriorDoor.setOtherDoor(interiorDoor)
            exteriorDoor.zoneId = ToontownGlobals.SellbotHQ
            exteriorDoor.generateWithRequired(ToontownGlobals.SellbotHQ)
            exteriorDoor.sendUpdate('setDoorIndex', [i])
            self.doors.append(exteriorDoor)
        interiorDoor.setOtherDoor(self.doors[0])
        interiorDoor.zoneId = ToontownGlobals.SellbotLobby
        interiorDoor.generateWithRequired(ToontownGlobals.SellbotLobby)
        interiorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(interiorDoor)
            
    
    def createZone(self):
        CogHoodAI.createZone(self)
        
        # Create lobby manager...
        self.createLobbyManager(DistributedSellbotBossAI, ToontownGlobals.SellbotLobby)
        
        # Create VP elevator.
        self.createElevator(DistributedVPElevatorAI, self.lobbyMgr, ToontownGlobals.SellbotLobby, ToontownGlobals.SellbotLobby, boss=True)
        
        # Make our doors.
        self.createDoor()
        
        # Create Suit Planners in the cog playground and factory waiting area.
        self.createSuitPlanner(self.HOOD)
        self.createSuitPlanner(ToontownGlobals.SellbotFactoryExt)
        
        # Create factory elevators.
        mins = ToontownGlobals.FactoryLaffMinimums[0]
        self.createElevator(DistributedFactoryElevatorExtAI, self.air.factoryMgr, ToontownGlobals.SellbotFactoryExt, ToontownGlobals.SellbotFactoryInt, 0, minLaff=mins[0])
        self.createElevator(DistributedFactoryElevatorExtAI, self.air.factoryMgr, ToontownGlobals.SellbotFactoryExt, ToontownGlobals.SellbotFactoryInt, 1, minLaff=mins[0])
