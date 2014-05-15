from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.building.DistributedTutorialInteriorAI import DistributedTutorialInteriorAI
from toontown.toon import NPCToons
from toontown.building import DoorTypes
from toontown.building import DistributedDoorAI
from toontown.building.DistributedBuildingAI import DistributedBuildingAI
from toontown.suit.DistributedTutorialSuitAI import DistributedTutorialSuitAI
from toontown.toonbase import ToontownBattleGlobals
from toontown.building.HQBuildingAI import HQBuildingAI
import types

class TZoneStruct:
    branch = 0
    street = 0
    shop = 0
    hq = 0

class TutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TutorialManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.avId2Zones = {}

    def requestTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        zones = TZoneStruct()

        zones.branch = self.air.allocateZone()
        zones.street = self.air.allocateZone()
        zones.shop = self.air.allocateZone()
        zones.hq = self.air.allocateZone()
        
        npcDesc = NPCToons.NPCToonDict.get(20000)
        npc = NPCToons.createNPC(self.air, 20000, npcDesc, zones.shop, 0)
        npc.setTutorial(1)
        
        int = DistributedTutorialInteriorAI(self.air, zones.shop, npc.getDoId())
        int.generateWithRequired(zones.shop)
        
        door0 = DistributedDoorAI.DistributedDoorAI(self.air, 2, DoorTypes.EXT_STANDARD, doorIndex=0)
        insideDoor0 = DistributedDoorAI.DistributedDoorAI(self.air, 0, DoorTypes.INT_STANDARD, doorIndex=0)
        door0.setOtherDoor(insideDoor0)
        insideDoor0.setOtherDoor(door0)
        door0.zoneId = zones.street
        insideDoor0.zoneId = zones.shop
        door0.generateWithRequired(zones.street)
        door0.sendUpdate('setDoorIndex', [door0.getDoorIndex()])
        insideDoor0.generateWithRequired(zones.shop)
        insideDoor0.sendUpdate('setDoorIndex', [insideDoor0.getDoorIndex()])
        
        hq = HQBuildingAI(self.air, zones.street, zones.hq, 1)
        
        
        suit = DistributedTutorialSuitAI(self.air)
        suit.generateWithRequired(zones.street)

        # Toontorial TODO list:
        #  spawn HQ Harry
        #  prevent access to zones early      
        #  Spawn Flippy after battle
        #  cleanup zones and objects
        #  visual fixes
        #  assign initial quest in QMAI rather than presenting choice
        
        self.d_enterTutorial(avId, zones.street, zones.street, zones.shop, zones.hq) #hackfix lololol        


    def rejectTutorial(self):
        pass

    def requestSkipTutorial(self):
        pass

    def d_skipTutorialResponse(self, avId, allOk):
        self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [allOk])

    def d_enterTutorial(self, avId, branchZone, streetZone, shopZone, hqZone):
        self.sendUpdateToAvatarId(avId, 'enterTutorial', [branchZone, streetZone, shopZone, hqZone])

    def allDone(self):
        pass

    def toonArrived(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do[avId]
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(0, [])
        av.setHp(15)
        if av.inventory.numItem(ToontownBattleGlobals.THROW_TRACK, 0) == 0:
            av.inventory.addItem(ToontownBattleGlobals.THROW_TRACK, 0)
        if av.inventory.numItem(ToontownBattleGlobals.SQUIRT_TRACK, 0) == 0:
            av.inventory.addItem(ToontownBattleGlobals.SQUIRT_TRACK, 0)
        av.d_setInventory(av.inventory.makeNetString())
