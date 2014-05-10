from CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedLawbotBossAI import DistributedLawbotBossAI
from toontown.coghq.DistributedLawOfficeElevatorExtAI import DistributedLawOfficeElevatorExtAI
from toontown.building.DistributedCJElevatorAI import DistributedCJElevatorAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building import FADoorCodes


class LawbotHQAI(CogHoodAI):
    HOOD = ToontownGlobals.LawbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.createZone()
        
    def createDoor(self):
        daInteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, self.HOOD)
        daExteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.LawbotOfficeExt)
        daExteriorDoor.setOtherDoor(daInteriorDoor)
        daExteriorDoor.zoneId = self.HOOD
        daExteriorDoor.generateWithRequired(self.HOOD)
        daExteriorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(daExteriorDoor)
        daInteriorDoor.setOtherDoor(daExteriorDoor)
        daInteriorDoor.zoneId = ToontownGlobals.LawbotOfficeExt
        daInteriorDoor.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
        daInteriorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(daInteriorDoor)
        
        interiorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, self.HOOD, doorIndex=0)
        exteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.LawbotLobby, doorIndex=1, lockValue=FADoorCodes.LB_DISGUISE_INCOMPLETE)
        exteriorDoor.setOtherDoor(interiorDoor)
        exteriorDoor.zoneId = self.HOOD
        exteriorDoor.generateWithRequired(self.HOOD)
        exteriorDoor.sendUpdate('setDoorIndex', [1])
        self.doors.append(exteriorDoor)
        interiorDoor.setOtherDoor(exteriorDoor)
        interiorDoor.zoneId = ToontownGlobals.LawbotLobby
        interiorDoor.generateWithRequired(ToontownGlobals.LawbotLobby)
        interiorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(interiorDoor)
            
    
    def createZone(self):
        CogHoodAI.createZone(self)
        
        # Create lobby manager...
        self.createLobbyManager(DistributedLawbotBossAI, ToontownGlobals.LawbotLobby)
        
        # Create CFO elevator.
        self.createElevator(DistributedCJElevatorAI, self.lobbyMgr, ToontownGlobals.LawbotLobby, ToontownGlobals.LawbotLobby, boss=True)
        
        # Make our doors.
        self.createDoor()
        
        # Create Suit Planners in the cog playground
        self.createSuitPlanner(self.HOOD)
        
        # Create mint elevators.
        mins = ToontownGlobals.FactoryLaffMinimums[2]
        self.createElevator(DistributedLawOfficeElevatorExtAI, self.air.lawOfficeMgr, ToontownGlobals.LawbotOfficeExt, ToontownGlobals.LawbotOfficeInt, 0, minLaff=mins[0])
        self.createElevator(DistributedLawOfficeElevatorExtAI, self.air.lawOfficeMgr, ToontownGlobals.LawbotOfficeExt, ToontownGlobals.LawbotOfficeInt, 1, minLaff=mins[1])
        self.createElevator(DistributedLawOfficeElevatorExtAI, self.air.lawOfficeMgr, ToontownGlobals.LawbotOfficeExt, ToontownGlobals.LawbotOfficeInt, 2, minLaff=mins[2])
        self.createElevator(DistributedLawOfficeElevatorExtAI, self.air.lawOfficeMgr, ToontownGlobals.LawbotOfficeExt, ToontownGlobals.LawbotOfficeInt, 3, minLaff=mins[3])