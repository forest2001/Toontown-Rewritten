from CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedBossbotBossAI import DistributedBossbotBossAI
from toontown.building.DistributedBBElevatorAI import DistributedBBElevatorAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.coghq import DistributedCogKartAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes

class BossbotHQAI(CogHoodAI):
    HOOD = ToontownGlobals.BossbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.createZone()
        
    def createDoor(self):
        interiorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, self.HOOD, doorIndex=0)
        exteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.BossbotLobby, doorIndex=0, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        exteriorDoor.setOtherDoor(interiorDoor)
        exteriorDoor.zoneId = self.HOOD
        exteriorDoor.generateWithRequired(self.HOOD)
        exteriorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(exteriorDoor)

        interiorDoor.setOtherDoor(exteriorDoor)
        interiorDoor.zoneId = ToontownGlobals.BossbotLobby
        interiorDoor.generateWithRequired(ToontownGlobals.BossbotLobby)
        interiorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(interiorDoor)
            
    
    def createZone(self):
        CogHoodAI.createZone(self)
        
        # Create lobby manager...
        self.createLobbyManager(DistributedBossbotBossAI, ToontownGlobals.BossbotLobby)
        
        # Create CEO elevator.
        self.ceoElevator = self.createElevator(DistributedBBElevatorAI, self.lobbyMgr, ToontownGlobals.BossbotLobby, ToontownGlobals.BossbotLobby, boss=True)
        
        # Make our doors.
        self.createDoor()
        
        # Create Cog Golf Courses.
        # kartPos = ((154.762, 37.169, 0), (141.403, -81.887, 0), (-48.44, 15.308, 0))
        # hprList = ((110.815, 0, 0), (61.231, 0, 0), (-105.481, 0, 0))

        # mins = ToontownGlobals.FactoryLaffMinimums[3]
        # self.frontThree = self.createKart(DistributedCogKartAI, self.air.mintMgr, self.HOOD, ToontownGlobals.BossbotCountryClubIntA, 0, minLaff=mins[0])
        # self.middleSix = self.createKart(DistributedCogKartAI, self.air.mintMgr, self.HOOD, ToontownGlobals.BossbotCountryClubIntB, 1, minLaff=mins[1])
        # self.backNine = self.createKart(DistributedCogKartAI, self.air.mintMgr, self.HOOD, ToontownGlobals.BossbotCountryClubIntC, 2, minLaff=mins[2])

        # Enable boarding groups
        if simbase.config.GetBool('want-boarding-groups', True):
            # CEO Boarding Group
            self.createBoardingGroup(self.air, [self.ceoElevator.doId], ToontownGlobals.BossbotLobby, 8)

            # Cog Golf Boarding Group's
            # self.cogGolfCources = [self.frontThree.doId, self.middleSix.doId, self.backNine.doId]
            # self.createBoardingGroup(self.air, self.cogGolfCources, ToontownGlobals.BossbotHQ)
