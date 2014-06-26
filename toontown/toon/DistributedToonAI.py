from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from direct.directnotify import DirectNotifyGlobal
import ToonDNA
from toontown.suit import SuitDNA
import InventoryBase
import Experience
from otp.avatar import DistributedAvatarAI
from otp.avatar import DistributedPlayerAI
from otp.otpbase import OTPLocalizer
from direct.distributed import DistributedSmoothNodeAI
from toontown.toonbase import ToontownGlobals
from toontown.quest import QuestRewardCounter
from toontown.quest import Quests
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import SuitBattleGlobals
from direct.task import Task
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from direct.showbase import PythonUtil
from direct.distributed.ClockDelta import *
from toontown.toonbase.ToontownGlobals import *
import types
from toontown.fishing import FishGlobals
from toontown.fishing import FishCollection
from toontown.fishing import FishTank
from NPCToons import npcFriends, isZoneProtected
from toontown.coghq import CogDisguiseGlobals
import random
import re
from toontown.chat import ResistanceChat
from toontown.racing import RaceGlobals
from toontown.hood import ZoneUtil
from toontown.toon import NPCToons
from toontown.estate import FlowerCollection
from toontown.estate import FlowerBasket
from toontown.estate import GardenGlobals
from toontown.golf import GolfGlobals
from toontown.parties import PartyGlobals
from toontown.parties.PartyInfo import PartyInfoAI
from toontown.parties.InviteInfo import InviteInfoBase
from toontown.parties.PartyReplyInfo import PartyReplyInfoBase
from toontown.parties.PartyGlobals import InviteStatus
from toontown.toonbase import ToontownAccessAI
from toontown.toonbase import TTLocalizer
from toontown.catalog import CatalogAccessoryItem
from toontown.minigame import MinigameCreatorAI
import ModuleListAI

# Magic Word imports
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
import shlex

if simbase.wantPets:
    from toontown.pets import PetLookerAI, PetObserve
else:
    class PetLookerAI:
        class PetLookerAI:
            pass

if simbase.wantKarts:
    from toontown.racing.KartDNA import *

class DistributedToonAI(DistributedPlayerAI.DistributedPlayerAI, DistributedSmoothNodeAI.DistributedSmoothNodeAI, PetLookerAI.PetLookerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonAI')
    maxCallsPerNPC = 100
    partTypeIds = {ToontownGlobals.FT_FullSuit: (CogDisguiseGlobals.leftLegIndex,
                                   CogDisguiseGlobals.rightLegIndex,
                                   CogDisguiseGlobals.torsoIndex,
                                   CogDisguiseGlobals.leftArmIndex,
                                   CogDisguiseGlobals.rightArmIndex),
     ToontownGlobals.FT_Leg: (CogDisguiseGlobals.leftLegIndex, CogDisguiseGlobals.rightLegIndex),
     ToontownGlobals.FT_Arm: (CogDisguiseGlobals.leftArmIndex, CogDisguiseGlobals.rightArmIndex),
     ToontownGlobals.FT_Torso: (CogDisguiseGlobals.torsoIndex,)}
    lastFlagAvTime = globalClock.getFrameTime()
    flagCounts = {}
    WantTpTrack = simbase.config.GetBool('want-tptrack', False)
    DbCheckPeriodPaid = simbase.config.GetInt('toon-db-check-period-paid', 10 * 60)
    DbCheckPeriodUnpaid = simbase.config.GetInt('toon-db-check-period-unpaid', 1 * 60)
    BanOnDbCheckFail = simbase.config.GetBool('want-ban-dbcheck', 0)
    DbCheckAccountDateEnable = config.GetBool('account-blackout-enable', 1)
    DbCheckAccountDateBegin = config.GetString('account-blackout-start', '2013-08-20 12:30:00')
    DbCheckAccountDateDisconnect = config.GetBool('account-blackout-disconnect', 0)
    WantOldGMNameBan = simbase.config.GetBool('want-old-gm-name-ban', 1)

    def __init__(self, air):
        DistributedPlayerAI.DistributedPlayerAI.__init__(self, air)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.__init__(self, air)
        if simbase.wantPets:
            PetLookerAI.PetLookerAI.__init__(self)
        self.air = air
        self.dna = ToonDNA.ToonDNA()
        self.mwDNABackup = {}
        self.inventory = None
        self.fishCollection = None
        self.fishTank = None
        self.experience = None
        self.quests = []
        self.cogs = []
        self.cogCounts = []
        self.NPCFriendsDict = {}
        self.clothesTopsList = []
        self.clothesBottomsList = []
        self.hatList = []
        self.glassesList = []
        self.backpackList = []
        self.shoesList = []
        self.hat = (0, 0, 0)
        self.glasses = (0, 0, 0)
        self.backpack = (0, 0, 0)
        self.shoes = (0, 0, 0)
        self.cogTypes = [0,
         0,
         0,
         0]
        self.cogLevel = [0,
         0,
         0,
         0]
        self.cogParts = [0,
         0,
         0,
         0]
        self.cogRadar = [0,
         0,
         0,
         0]
        self.cogIndex = -1
        self.disguisePageFlag = 0
        self.sosPageFlag = 0
        self.buildingRadar = [0,
         0,
         0,
         0]
        self.fishingRod = 0
        self.fishingTrophies = []
        self.trackArray = []
        self.emoteAccess = [0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0]
        self.maxBankMoney = ToontownGlobals.DefaultMaxBankMoney
        self.gardenSpecials = []
        self.houseId = 0
        self.posIndex = 0
        self.savedCheesyEffect = ToontownGlobals.CENormal
        self.savedCheesyHoodId = 0
        self.savedCheesyExpireTime = 0
        self.ghostMode = 0
        self.immortalMode = 0
        self.unlimitedGags = 0
        self.numPies = 0
        self.pieType = 0
        self._isGM = False
        self._gmType = None
        self.hpOwnedByBattle = 0
        if simbase.wantPets:
            self.petTrickPhrases = []
        if simbase.wantBingo:
            self.bingoCheat = False
        self.customMessages = []
        self.catalogNotify = ToontownGlobals.NoItems
        self.mailboxNotify = ToontownGlobals.NoItems
        self.catalogScheduleCurrentWeek = 0
        self.catalogScheduleNextTime = 0
        self.monthlyCatalog = CatalogItemList.CatalogItemList()
        self.weeklyCatalog = CatalogItemList.CatalogItemList()
        self.backCatalog = CatalogItemList.CatalogItemList()
        self.onOrder = CatalogItemList.CatalogItemList(store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.onGiftOrder = CatalogItemList.CatalogItemList(store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.mailboxContents = CatalogItemList.CatalogItemList(store=CatalogItem.Customization)
        self.awardMailboxContents = CatalogItemList.CatalogItemList(store=CatalogItem.Customization)
        self.onAwardOrder = CatalogItemList.CatalogItemList(store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.kart = None
        if simbase.wantKarts:
            self.kartDNA = [-1] * getNumFields()
            self.tickets = 200
            self.allowSoloRace = False
            self.allowRaceTimeout = True
        self.setBattleId(0)
        self.gardenStarted = False
        self.flowerCollection = None
        self.shovel = 0
        self.shovelSkill = 0
        self.wateringCan = 0
        self.wateringCanSkill = 0
        self.hatePets = 1
        self.golfHistory = None
        self.golfHoleBest = None
        self.golfCourseBest = None
        self.unlimitedSwing = False
        self.previousAccess = None
        self.numMailItems = 0
        self.simpleMailNotify = ToontownGlobals.NoItems
        self.inviteMailNotify = ToontownGlobals.NoItems
        self.invites = []
        self.hostedParties = []
        self.partiesInvitedTo = []
        self.partyReplyInfoBases = []
        self.modulelist = ModuleListAI.ModuleList()
        self._dbCheckDoLater = None
        self.teleportOverride = 0
        self.wantBetaKeyQuest = 0
        self.magicWordTeleportRequests = []
        self.webAccountId = 0
        self.hasQuests = False
        return

    def generate(self):
        DistributedPlayerAI.DistributedPlayerAI.generate(self)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.generate(self)

    def announceGenerate(self):
        DistributedPlayerAI.DistributedPlayerAI.announceGenerate(self)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.announceGenerate(self)
        if self.isPlayerControlled():
            if self.WantOldGMNameBan:
                self._checkOldGMName()
            messenger.send('avatarEntered', [self])
        if hasattr(self, 'gameAccess') and self.gameAccess != 2:
            if self.hat[0] != 0:
                self.replaceItemInAccessoriesList(ToonDNA.HAT, 0, 0, 0, self.hat[0], self.hat[1], self.hat[2])
                self.b_setHatList(self.hatList)
                self.b_setHat(0, 0, 0)
            if self.glasses[0] != 0:
                self.replaceItemInAccessoriesList(ToonDNA.GLASSES, 0, 0, 0, self.glasses[0], self.glasses[1], self.glasses[2])
                self.b_setGlassesList(self.glassesList)
                self.b_setGlasses(0, 0, 0)
            if self.backpack[0] != 0:
                self.replaceItemInAccessoriesList(ToonDNA.BACKPACK, 0, 0, 0, self.backpack[0], self.backpack[1], self.backpack[2])
                self.b_setBackpackList(self.backpackList)
                self.b_setBackpack(0, 0, 0)
            if self.shoes[0] != 0:
                self.replaceItemInAccessoriesList(ToonDNA.SHOES, 0, 0, 0, self.shoes[0], self.shoes[1], self.shoes[2])
                self.b_setShoesList(self.shoesList)
                self.b_setShoes(0, 0, 0)
        from toontown.toon.DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
        if not isinstance(self, DistributedNPCToonBaseAI):
            self.sendUpdate('setDefaultShard', [self.air.districtId])
        # Begin ping-pong.
        if self.isPlayerControlled():
            self.ping()

    def setLocation(self, parentId, zoneId):
        messenger.send('toon-left-%s' % self.zoneId, [self])
        messenger.send('toon-entered-%s' % zoneId, [self])

        DistributedPlayerAI.DistributedPlayerAI.setLocation(self, parentId, zoneId)

        from toontown.toon.DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
        if not isinstance(self, DistributedNPCToonBaseAI):
            # Do we want to start the playground toonup tick?
            self.considerToonUp(zoneId)

            # Teleportation access stuff.
            if 100 <= zoneId < ToontownGlobals.DynamicZonesBegin:
                hood = ZoneUtil.getHoodId(zoneId)
                if not simbase.config.GetBool('want-doomsday', False):
                    self.sendUpdate('setLastHood', [hood])
                    self.b_setDefaultZone(hood)

                hoodsVisited = list(self.getHoodsVisited())
                if not hood in hoodsVisited:
                    hoodsVisited.append(hood)
                    self.b_setHoodsVisited(hoodsVisited)
                    # TODO: REMOVE THIS AFTER ARG IS OVER.
                    if hood == ToontownGlobals.LawbotHQ:
                        self.air.writeServerEvent("arg-complete", avId=self.getDoId(), message="%s has unlocked LBHQ!" % self.getName())

                if zoneId == ToontownGlobals.GoofySpeedway:
                    tpAccess = self.getTeleportAccess()
                    if not ToontownGlobals.GoofySpeedway in tpAccess:
                        tpAccess.append(ToontownGlobals.GoofySpeedway)
                        self.b_setTeleportAccess(tpAccess)

    def _renewDoLater(self, renew = True):
        if renew:
            delay = self.DbCheckPeriodUnpaid
            if self.gameAccess == OTPGlobals.AccessFull:
                delay = self.DbCheckPeriodPaid
            self._dbCheckDoLater = taskMgr.doMethodLater(delay, self._doDbCheck, 'dbCheck-%s' % self.doId)

    def sendDeleteEvent(self):
        if simbase.wantPets:
            isInEstate = self.isInEstate()
            wasInEstate = self.wasInEstate()
            if isInEstate or wasInEstate:
                PetObserve.send(self.estateZones, PetObserve.PetActionObserve(PetObserve.Actions.LOGOUT, self.doId))
                if wasInEstate:
                    self.cleanupEstateData()
        DistributedAvatarAI.DistributedAvatarAI.sendDeleteEvent(self)

    def delete(self):
        self.notify.debug('----Deleting DistributedToonAI %d ' % self.doId)
        if self._dbCheckDoLater:
            taskMgr.remove(self._dbCheckDoLater)
            self._dbCheckDoLater = None
        if self.isPlayerControlled():
            messenger.send('avatarExited', [self])
        if simbase.wantPets:
            if self.isInEstate():
                print 'ToonAI - Exit estate toonId:%s' % self.doId
                self.exitEstate()
            if self.zoneId != ToontownGlobals.QuietZone:
                self.announceZoneChange(ToontownGlobals.QuietZone, self.zoneId)
        taskName = self.uniqueName('cheesy-expires')
        taskMgr.remove(taskName)
        taskName = self.uniqueName('next-catalog')
        taskMgr.remove(taskName)
        taskName = self.uniqueName('next-delivery')
        taskMgr.remove(taskName)
        taskName = self.uniqueName('next-award-delivery')
        taskMgr.remove(taskName)
        taskName = 'next-bothDelivery-%s' % self.doId
        taskMgr.remove(taskName)
        taskMgr.remove(self.uniqueName('PingTimeout'))
        taskMgr.remove(self.uniqueName('PingCooldown'))
        self.stopToonUp()
        del self.dna
        if self.inventory:
            self.inventory.unload()
        del self.inventory
        del self.experience
        if simbase.wantPets:
            PetLookerAI.PetLookerAI.destroy(self)
        del self.kart
        self._sendExitServerEvent()
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)
        DistributedPlayerAI.DistributedPlayerAI.delete(self)
        return

    def deleteDummy(self):
        self.notify.debug('----deleteDummy DistributedToonAI %d ' % self.doId)
        if self.inventory:
            self.inventory.unload()
        del self.inventory
        self.experience = None
        taskName = self.uniqueName('next-catalog')
        taskMgr.remove(taskName)
        taskMgr.remove(self.uniqueName('PingTimeout'))
        taskMgr.remove(self.uniqueName('PingCooldown'))
        return

    def ban(self, comment):
        #simbase.air.banManager.ban(self.doId, self.DISLid, comment)
        pass

    def disconnect(self):
        self.requestDelete()

    def patchDelete(self):
        del self.dna
        if self.inventory:
            self.inventory.unload()
        del self.inventory
        del self.experience
        if simbase.wantPets:
            PetLookerAI.PetLookerAI.destroy(self)
        self.doNotDeallocateChannel = True
        self.zoneId = None
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)
        DistributedPlayerAI.DistributedPlayerAI.delete(self)
        return

    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        DistributedAvatarAI.DistributedAvatarAI.handleLogicalZoneChange(self, newZoneId, oldZoneId)
        if self.isPlayerControlled() and self.WantTpTrack:
            messenger.send(self.staticGetLogicalZoneChangeAllEvent(), [newZoneId, oldZoneId, self])
        if self.cogIndex != -1 and not ToontownAccessAI.canWearSuit(self.doId, newZoneId):
            if simbase.config.GetBool('cogsuit-hack-prevent', False):
                self.b_setCogIndex(-1)
            '''if not simbase.air.cogSuitMessageSent:
                self.notify.warning('%s handleLogicalZoneChange as a suit: %s' % (self.doId, self.cogIndex))
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon wearing a cog suit with index: %s in a zone they are not allowed to in. Zone: %s' % (self.cogIndex, newZoneId))
                simbase.air.cogSuitMessageSent = True
                if simbase.config.GetBool('want-ban-wrong-suit-place', False):
                    commentStr = 'Toon %s wearing a suit in a zone they are not allowed to in. Zone: %s' % (self.doId, newZoneId)
                    dislId = self.DISLid
                    #simbase.air.banManager.ban(self.doId, dislId, commentStr)'''

    def announceZoneChange(self, newZoneId, oldZoneId):
        from toontown.pets import PetObserve
        self.air.welcomeValleyManager.toonSetZone(self.doId, newZoneId)
        broadcastZones = [oldZoneId, newZoneId]
        if self.isInEstate() or self.wasInEstate():
            broadcastZones = union(broadcastZones, self.estateZones)
        PetObserve.send(broadcastZones, PetObserve.PetActionObserve(PetObserve.Actions.CHANGE_ZONE, self.doId, (oldZoneId, newZoneId)))

    def checkAccessorySanity(self, accessoryType, idx, textureIdx, colorIdx):
        if idx == 0 and textureIdx == 0 and colorIdx == 0:
            return 1
        if accessoryType == ToonDNA.HAT:
            stylesDict = ToonDNA.HatStyles
            accessoryTypeStr = 'Hat'
        elif accessoryType == ToonDNA.GLASSES:
            stylesDict = ToonDNA.GlassesStyles
            accessoryTypeStr = 'Glasses'
        elif accessoryType == ToonDNA.BACKPACK:
            stylesDict = ToonDNA.BackpackStyles
            accessoryTypeStr = 'Backpack'
        elif accessoryType == ToonDNA.SHOES:
            stylesDict = ToonDNA.ShoesStyles
            accessoryTypeStr = 'Shoes'
        else:
            return 0
        try:
            styleStr = stylesDict.keys()[stylesDict.values().index([idx, textureIdx, colorIdx])]
            accessoryItemId = 0
            for itemId in CatalogAccessoryItem.AccessoryTypes.keys():
                if styleStr == CatalogAccessoryItem.AccessoryTypes[itemId][CatalogAccessoryItem.ATString]:
                    accessoryItemId = itemId
                    break

            if accessoryItemId == 0:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon tried to wear invalid %s %d %d %d' % (accessoryTypeStr,
                 idx,
                 textureIdx,
                 colorIdx))
                return 0
            if not simbase.config.GetBool('want-check-accessory-sanity', False):
                return 1
            accessoryItem = CatalogAccessoryItem.CatalogAccessoryItem(accessoryItemId)
            result = self.air.catalogManager.isItemReleased(accessoryItem)
            if result == 0:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon wore unreleased accessoryItem %d' % accessoryItemId)
            return result
        except:
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon tried to wear invalid %s %d %d %d' % (accessoryTypeStr,
             idx,
             textureIdx,
             colorIdx))
            return 0

    def b_setHat(self, idx, textureIdx, colorIdx):
        self.d_setHat(idx, textureIdx, colorIdx)
        self.setHat(idx, textureIdx, colorIdx)

    def d_setHat(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.HAT, idx, textureIdx, colorIdx):
            pass
        self.sendUpdate('setHat', [idx, textureIdx, colorIdx])

    def setHat(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.HAT, idx, textureIdx, colorIdx):
            pass
        self.hat = (idx, textureIdx, colorIdx)

    def getHat(self):
        return self.hat

    def b_setGlasses(self, idx, textureIdx, colorIdx):
        self.d_setGlasses(idx, textureIdx, colorIdx)
        self.setGlasses(idx, textureIdx, colorIdx)

    def d_setGlasses(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.GLASSES, idx, textureIdx, colorIdx):
            pass
        self.sendUpdate('setGlasses', [idx, textureIdx, colorIdx])

    def setGlasses(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.GLASSES, idx, textureIdx, colorIdx):
            pass
        self.glasses = (idx, textureIdx, colorIdx)

    def getGlasses(self):
        return self.glasses

    def b_setBackpack(self, idx, textureIdx, colorIdx):
        self.d_setBackpack(idx, textureIdx, colorIdx)
        self.setBackpack(idx, textureIdx, colorIdx)

    def d_setBackpack(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.BACKPACK, idx, textureIdx, colorIdx):
            pass
        self.sendUpdate('setBackpack', [idx, textureIdx, colorIdx])

    def setBackpack(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.BACKPACK, idx, textureIdx, colorIdx):
            pass
        self.backpack = (idx, textureIdx, colorIdx)

    def getBackpack(self):
        return self.backpack

    def b_setShoes(self, idx, textureIdx, colorIdx):
        self.d_setShoes(idx, textureIdx, colorIdx)
        self.setShoes(idx, textureIdx, colorIdx)

    def d_setShoes(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.SHOES, idx, textureIdx, colorIdx):
            pass
        self.sendUpdate('setShoes', [idx, textureIdx, colorIdx])

    def setShoes(self, idx, textureIdx, colorIdx):
        if not self.checkAccessorySanity(ToonDNA.SHOES, idx, textureIdx, colorIdx):
            pass
        self.shoes = (idx, textureIdx, colorIdx)

    def getShoes(self):
        return self.shoes

    def b_setDNAString(self, string):
        self.d_setDNAString(string)
        self.setDNAString(string)

    def d_setDNAString(self, string):
        self.sendUpdate('setDNAString', [string])

    def setDNAString(self, string):
        self.dna.makeFromNetString(string)
        if simbase.config.GetBool('adjust-dna', True) and self.verifyDNA() == False:
            logStr = 'AvatarHackWarning! invalid dna colors for %s old: %s new: %s' % (self.doId, str(ToonDNA.ToonDNA(string).asTuple()), str(self.dna.asTuple()))
            self.notify.warning(logStr)
            self.air.writeServerEvent('suspicious', avId=self.doId, issue=logStr)

    def verifyDNA(self):
        changed = False
        if self.isPlayerControlled():
            allowedColors = []
            if self.dna.gender == 'm':
                allowedColors = ToonDNA.defaultBoyColorList
            else:
                allowedColors = ToonDNA.defaultGirlColorList

            # No idea why this wasn't done by disney, but add sanity checks for black (and now white) toons.
            if self.dna.getAnimal() == 'bear':
                allowedColors = allowedColors + [0]
            if self.dna.getAnimal() == 'cat':
                allowedColors = allowedColors + [26]

            if self.dna.legColor not in allowedColors:
                self.dna.legColor = allowedColors[0]
                changed = True
            if self.dna.armColor not in allowedColors:
                self.dna.armColor = allowedColors[0]
                changed = True
            if self.dna.headColor not in allowedColors:
                self.dna.headColor = allowedColors[0]
                changed = True
            if changed:
                self.d_setDNAString(self.dna.makeNetString())
        return not changed

    def getDNAString(self):
        return self.dna.makeNetString()

    def getStyle(self):
        return self.dna

    def b_setExperience(self, experience):
        self.d_setExperience(experience)
        self.setExperience(experience)

    def d_setExperience(self, experience):
        self.sendUpdate('setExperience', [experience])

    def setExperience(self, experience):
        self.experience = Experience.Experience(experience, self)

    def getExperience(self):
        return self.experience.makeNetString()

    def b_setInventory(self, inventory):
        self.setInventory(inventory)
        self.d_setInventory(self.getInventory())

    def d_setInventory(self, inventory):
        self.sendUpdate('setInventory', [inventory])

    def setInventory(self, inventoryNetString):
        if self.inventory:
            self.inventory.updateInvString(inventoryNetString)
        else:
            self.inventory = InventoryBase.InventoryBase(self, inventoryNetString)
        emptyInv = InventoryBase.InventoryBase(self)
        emptyString = emptyInv.makeNetString()
        lengthMatch = len(inventoryNetString) - len(emptyString)
        if lengthMatch != 0:
            if len(inventoryNetString) == 42:
                oldTracks = 7
                oldLevels = 6
            elif len(inventoryNetString) == 49:
                oldTracks = 7
                oldLevels = 7
            else:
                oldTracks = 0
                oldLevels = 0
            if oldTracks == 0 and oldLevels == 0:
                self.notify.warning('reseting invalid inventory to MAX on toon: %s' % self.doId)
                self.inventory.zeroInv()
                self.inventory.maxOutInv(1, 1)
            else:
                newInventory = InventoryBase.InventoryBase(self)
                oldList = emptyInv.makeFromNetStringForceSize(inventoryNetString, oldTracks, oldLevels)
                for indexTrack in range(0, oldTracks):
                    for indexGag in range(0, oldLevels):
                        newInventory.addItems(indexTrack, indexGag, oldList[indexTrack][indexGag])

                self.inventory.unload()
                self.inventory = newInventory
            self.d_setInventory(self.getInventory())

    def getInventory(self):
        return self.inventory.makeNetString()

    def doRestock(self, noUber = 1, noPaid = 1):
        self.inventory.zeroInv()
        self.inventory.maxOutInv(noUber, noPaid)
        self.d_setInventory(self.inventory.makeNetString())

    def setDefaultShard(self, shard):
        self.defaultShard = shard
        self.notify.debug('setting default shard to %s' % shard)

    def getDefaultShard(self):
        return self.defaultShard

    def setDefaultZone(self, zone):
        self.defaultZone = zone
        self.notify.debug('setting default zone to %s' % zone)

    def b_setDefaultZone(self, zone):
        if zone == self.defaultZone:
            return #reduces lag a shit ton
        self.sendUpdate('setDefaultZone', [zone])
        self.setDefaultZone(zone)

    def getDefaultZone(self):
        return self.defaultZone

    def setShtickerBook(self, string):
        self.notify.debug('setting shticker book to %s' % string)

    def getShtickerBook(self):
        return ''

    def d_setFriendsList(self, friendsList):
        self.sendUpdate('setFriendsList', [friendsList])
        return None

    def setFriendsList(self, friendsList):
        self.notify.debug('setting friends list to %s' % self.friendsList)
        self.friendsList = friendsList
        if friendsList:
            friendId = friendsList[-1]
            otherAv = self.air.doId2do.get(friendId)
            self.air.questManager.toonMadeFriend(self, otherAv)

    def getFriendsList(self):
        return self.friendsList

    def extendFriendsList(self, friendId, friendCode):
        for i in range(len(self.friendsList)):
            friendPair = self.friendsList[i]
            if friendPair[0] == friendId:
                self.friendsList[i] = (friendId, friendCode)
                return

        self.friendsList.append((friendId, friendCode))

    def d_setMaxNPCFriends(self, max):
        self.sendUpdate('setMaxNPCFriends', [max])

    def setMaxNPCFriends(self, max):
        if max & 32768:
            self.b_setSosPageFlag(1)
            max &= 32767
        configMax = simbase.config.GetInt('max-sos-cards', 16)
        if configMax != max:
            if self.sosPageFlag == 0:
                self.b_setMaxNPCFriends(configMax)
            else:
                self.b_setMaxNPCFriends(configMax | 32768)
        else:
            self.maxNPCFriends = max
        if self.maxNPCFriends != 8 and self.maxNPCFriends != 16:
            self.notify.warning('Wrong max SOS cards %s, %d' % (self.maxNPCFriends, self.doId))

    def b_setMaxNPCFriends(self, max):
        self.setMaxNPCFriends(max)
        self.d_setMaxNPCFriends(max)

    def getMaxNPCFriends(self):
        return self.maxNPCFriends

    def getBattleId(self):
        if self.battleId >= 0:
            return self.battleId
        else:
            return 0

    def b_setBattleId(self, battleId):
        self.setBattleId(battleId)
        self.d_setBattleId(battleId)

    def d_setBattleId(self, battleId):
        if self.battleId >= 0:
            self.sendUpdate('setBattleId', [battleId])
        else:
            self.sendUpdate('setBattleId', [0])

    def setBattleId(self, battleId):
        self.battleId = battleId

    def d_setNPCFriendsDict(self, NPCFriendsDict):
        NPCFriendsList = []
        for friend in NPCFriendsDict.keys():
            NPCFriendsList.append((friend, NPCFriendsDict[friend]))

        self.sendUpdate('setNPCFriendsDict', [NPCFriendsList])
        return None

    def setNPCFriendsDict(self, NPCFriendsList):
        self.NPCFriendsDict = {}
        for friendPair in NPCFriendsList:
            self.NPCFriendsDict[friendPair[0]] = friendPair[1]

        self.notify.debug('setting NPC friends dict to %s' % self.NPCFriendsDict)

    def getNPCFriendsDict(self):
        return self.NPCFriendsDict

    def b_setNPCFriendsDict(self, NPCFriendsList):
        self.setNPCFriendsDict(NPCFriendsList)
        self.d_setNPCFriendsDict(self.NPCFriendsDict)

    def resetNPCFriendsDict(self):
        self.b_setNPCFriendsDict([])

    def attemptAddNPCFriend(self, npcFriend, numCalls = 1):
        if numCalls <= 0:
            self.notify.warning('invalid numCalls: %d' % numCalls)
            return 0
        if self.NPCFriendsDict.has_key(npcFriend):
            self.NPCFriendsDict[npcFriend] += numCalls
        elif npcFriends.has_key(npcFriend):
            if len(self.NPCFriendsDict.keys()) >= self.maxNPCFriends:
                return 0
            self.NPCFriendsDict[npcFriend] = numCalls
        else:
            self.notify.warning('invalid NPC: %d' % npcFriend)
            return 0
        if self.NPCFriendsDict[npcFriend] > self.maxCallsPerNPC:
            self.NPCFriendsDict[npcFriend] = self.maxCallsPerNPC
        self.d_setNPCFriendsDict(self.NPCFriendsDict)
        if self.sosPageFlag == 0:
            self.b_setMaxNPCFriends(self.maxNPCFriends | 32768)
        return 1

    def attemptSubtractNPCFriend(self, npcFriend):
        if not self.NPCFriendsDict.has_key(npcFriend):
            self.notify.warning('attemptSubtractNPCFriend: invalid NPC %s' % npcFriend)
            return 0
        if hasattr(self, 'autoRestockSOS') and self.autoRestockSOS:
            cost = 0
        else:
            cost = 1
        self.NPCFriendsDict[npcFriend] -= cost
        if self.NPCFriendsDict[npcFriend] <= 0:
            del self.NPCFriendsDict[npcFriend]
        self.d_setNPCFriendsDict(self.NPCFriendsDict)
        return 1

    def restockAllNPCFriends(self, amt=1):
        desiredNpcFriends = [2001,
         2011,
         3112,
         4119,
         1116,
         3137,
         3135]
        self.resetNPCFriendsDict()
        for npcId in desiredNpcFriends:
            self.attemptAddNPCFriend(npcId, amt)

    def d_setMaxAccessories(self, max):
        self.sendUpdate('setMaxAccessories', [self.maxAccessories])

    def setMaxAccessories(self, max):
        self.maxAccessories = max

    def b_setMaxAccessories(self, max):
        self.setMaxAccessories(max)
        self.d_setMaxAccessories(max)

    def getMaxAccessories(self):
        return self.maxAccessories

    def isTrunkFull(self, extraAccessories = 0):
        numAccessories = (len(self.hatList) + len(self.glassesList) + len(self.backpackList) + len(self.shoesList)) / 3
        return numAccessories + extraAccessories >= self.maxAccessories

    def d_setHatList(self, clothesList):
        self.sendUpdate('setHatList', [clothesList])
        return None

    def setHatList(self, clothesList):
        self.hatList = clothesList

    def b_setHatList(self, clothesList):
        self.setHatList(clothesList)
        self.d_setHatList(clothesList)

    def getHatList(self):
        return self.hatList

    def d_setGlassesList(self, clothesList):
        self.sendUpdate('setGlassesList', [clothesList])
        return None

    def setGlassesList(self, clothesList):
        self.glassesList = clothesList

    def b_setGlassesList(self, clothesList):
        self.setGlassesList(clothesList)
        self.d_setGlassesList(clothesList)

    def getGlassesList(self):
        return self.glassesList

    def d_setBackpackList(self, clothesList):
        self.sendUpdate('setBackpackList', [clothesList])
        return None

    def setBackpackList(self, clothesList):
        self.backpackList = clothesList

    def b_setBackpackList(self, clothesList):
        self.setBackpackList(clothesList)
        self.d_setBackpackList(clothesList)

    def getBackpackList(self):
        return self.backpackList

    def d_setShoesList(self, clothesList):
        self.sendUpdate('setShoesList', [clothesList])
        return None

    def setShoesList(self, clothesList):
        self.shoesList = clothesList

    def b_setShoesList(self, clothesList):
        self.setShoesList(clothesList)
        self.d_setShoesList(clothesList)

    def getShoesList(self):
        return self.shoesList

    def addToAccessoriesList(self, accessoryType, geomIdx, texIdx, colorIdx):
        if self.isTrunkFull():
            return 0
        if accessoryType == ToonDNA.HAT:
            itemList = self.hatList
        elif accessoryType == ToonDNA.GLASSES:
            itemList = self.glassesList
        elif accessoryType == ToonDNA.BACKPACK:
            itemList = self.backpackList
        elif accessoryType == ToonDNA.SHOES:
            itemList = self.shoesList
        else:
            return 0
        index = 0
        for i in range(0, len(itemList), 3):
            if itemList[i] == geomIdx and itemList[i + 1] == texIdx and itemList[i + 2] == colorIdx:
                return 0

        if accessoryType == ToonDNA.HAT:
            self.hatList.append(geomIdx)
            self.hatList.append(texIdx)
            self.hatList.append(colorIdx)
        elif accessoryType == ToonDNA.GLASSES:
            self.glassesList.append(geomIdx)
            self.glassesList.append(texIdx)
            self.glassesList.append(colorIdx)
        elif accessoryType == ToonDNA.BACKPACK:
            self.backpackList.append(geomIdx)
            self.backpackList.append(texIdx)
            self.backpackList.append(colorIdx)
        elif accessoryType == ToonDNA.SHOES:
            self.shoesList.append(geomIdx)
            self.shoesList.append(texIdx)
            self.shoesList.append(colorIdx)
        return 1

    def replaceItemInAccessoriesList(self, accessoryType, geomIdxA, texIdxA, colorIdxA, geomIdxB, texIdxB, colorIdxB):
        if accessoryType == ToonDNA.HAT:
            itemList = self.hatList
        elif accessoryType == ToonDNA.GLASSES:
            itemList = self.glassesList
        elif accessoryType == ToonDNA.BACKPACK:
            itemList = self.backpackList
        elif accessoryType == ToonDNA.SHOES:
            itemList = self.shoesList
        else:
            return 0
        index = 0
        for i in range(0, len(itemList), 3):
            if itemList[i] == geomIdxA and itemList[i + 1] == texIdxA and itemList[i + 2] == colorIdxA:
                if accessoryType == ToonDNA.HAT:
                    self.hatList[i] = geomIdxB
                    self.hatList[i + 1] = texIdxB
                    self.hatList[i + 2] = colorIdxB
                elif accessoryType == ToonDNA.GLASSES:
                    self.glassesList[i] = geomIdxB
                    self.glassesList[i + 1] = texIdxB
                    self.glassesList[i + 2] = colorIdxB
                elif accessoryType == ToonDNA.BACKPACK:
                    self.backpackList[i] = geomIdxB
                    self.backpackList[i + 1] = texIdxB
                    self.backpackList[i + 2] = colorIdxB
                else:
                    self.shoesList[i] = geomIdxB
                    self.shoesList[i + 1] = texIdxB
                    self.shoesList[i + 2] = colorIdxB
                return 1

        return 0

    def hasAccessory(self, accessoryType, geomIdx, texIdx, colorIdx):
        if accessoryType == ToonDNA.HAT:
            itemList = self.hatList
            cur = self.hat
        elif accessoryType == ToonDNA.GLASSES:
            itemList = self.glassesList
            cur = self.glasses
        elif accessoryType == ToonDNA.BACKPACK:
            itemList = self.backpackList
            cur = self.backpack
        elif accessoryType == ToonDNA.SHOES:
            itemList = self.shoesList
            cur = self.shoes
        else:
            raise 'invalid accessory type %s' % accessoryType
        if cur == (geomIdx, texIdx, colorIdx):
            return True
        for i in xrange(0, len(itemList), 3):
            if itemList[i] == geomIdx and itemList[i + 1] == texIdx and itemList[i + 2] == colorIdx:
                return True

        return False

    def isValidAccessorySetting(self, accessoryType, geomIdx, texIdx, colorIdx):
        if not geomIdx and not texIdx and not colorIdx:
            return True
        return self.hasAccessory(accessoryType, geomIdx, texIdx, colorIdx)

    def removeItemInAccessoriesList(self, accessoryType, geomIdx, texIdx, colorIdx):
        if accessoryType == ToonDNA.HAT:
            itemList = self.hatList
        elif accessoryType == ToonDNA.GLASSES:
            itemList = self.glassesList
        elif accessoryType == ToonDNA.BACKPACK:
            itemList = self.backpackList
        elif accessoryType == ToonDNA.SHOES:
            itemList = self.shoesList
        else:
            return 0
        listLen = len(itemList)
        if listLen < 3:
            self.notify.warning('Accessory list is not long enough to delete anything')
            return 0
        index = 0
        for i in range(0, len(itemList), 3):
            if itemList[i] == geomIdx and itemList[i + 1] == texIdx and itemList[i + 2] == colorIdx:
                itemList = itemList[0:i] + itemList[i + 3:listLen]
                if accessoryType == ToonDNA.HAT:
                    self.hatList = itemList[:]
                    styles = ToonDNA.HatStyles
                    descDict = TTLocalizer.HatStylesDescriptions
                elif accessoryType == ToonDNA.GLASSES:
                    self.glassesList = itemList[:]
                    styles = ToonDNA.GlassesStyles
                    descDict = TTLocalizer.GlassesStylesDescriptions
                elif accessoryType == ToonDNA.BACKPACK:
                    self.backpackList = itemList[:]
                    styles = ToonDNA.BackpackStyles
                    descDict = TTLocalizer.BackpackStylesDescriptions
                elif accessoryType == ToonDNA.SHOES:
                    self.shoesList = itemList[:]
                    styles = ToonDNA.ShoesStyles
                    descDict = TTLocalizer.ShoesStylesDescriptions
                styleName = 'none'
                for style in styles.items():
                    if style[1] == [geomIdx, texIdx, colorIdx]:
                        styleName = style[0]
                        break

                if styleName == 'none' or not descDict.has_key(styleName):
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue=' tried to remove wrong accessory code %d %d %d' % (geomIdx, texIdx, colorIdx))
                else:
                    self.air.writeServerEvent('accessory', avId=self.doId, msg=' removed accessory %s' % descDict[styleName])
                return 1

        return 0

    def d_setMaxClothes(self, max):
        self.sendUpdate('setMaxClothes', [self.maxClothes])

    def setMaxClothes(self, max):
        self.maxClothes = max

    def b_setMaxClothes(self, max):
        self.setMaxClothes(max)
        self.d_setMaxClothes(max)

    def getMaxClothes(self):
        return self.maxClothes

    def isClosetFull(self, extraClothes = 0):
        numClothes = len(self.clothesTopsList) / 4 + len(self.clothesBottomsList) / 2
        return numClothes + extraClothes >= self.maxClothes

    def d_setClothesTopsList(self, clothesList):
        self.sendUpdate('setClothesTopsList', [clothesList])
        return None

    def setClothesTopsList(self, clothesList):
        self.clothesTopsList = clothesList

    def b_setClothesTopsList(self, clothesList):
        self.setClothesTopsList(clothesList)
        self.d_setClothesTopsList(clothesList)

    def getClothesTopsList(self):
        return self.clothesTopsList

    def addToClothesTopsList(self, topTex, topTexColor, sleeveTex, sleeveTexColor):
        if self.isClosetFull():
            return 0
        index = 0
        for i in range(0, len(self.clothesTopsList), 4):
            if self.clothesTopsList[i] == topTex and self.clothesTopsList[i + 1] == topTexColor and self.clothesTopsList[i + 2] == sleeveTex and self.clothesTopsList[i + 3] == sleeveTexColor:
                return 0

        self.clothesTopsList.append(topTex)
        self.clothesTopsList.append(topTexColor)
        self.clothesTopsList.append(sleeveTex)
        self.clothesTopsList.append(sleeveTexColor)
        return 1

    def replaceItemInClothesTopsList(self, topTexA, topTexColorA, sleeveTexA, sleeveTexColorA, topTexB, topTexColorB, sleeveTexB, sleeveTexColorB):
        index = 0
        for i in range(0, len(self.clothesTopsList), 4):
            if self.clothesTopsList[i] == topTexA and self.clothesTopsList[i + 1] == topTexColorA and self.clothesTopsList[i + 2] == sleeveTexA and self.clothesTopsList[i + 3] == sleeveTexColorA:
                self.clothesTopsList[i] = topTexB
                self.clothesTopsList[i + 1] = topTexColorB
                self.clothesTopsList[i + 2] = sleeveTexB
                self.clothesTopsList[i + 3] = sleeveTexColorB
                return 1

        return 0

    def removeItemInClothesTopsList(self, topTex, topTexColor, sleeveTex, sleeveTexColor):
        listLen = len(self.clothesTopsList)
        if listLen < 4:
            self.notify.warning('Clothes top list is not long enough to delete anything')
            return 0
        index = 0
        for i in range(0, listLen, 4):
            if self.clothesTopsList[i] == topTex and self.clothesTopsList[i + 1] == topTexColor and self.clothesTopsList[i + 2] == sleeveTex and self.clothesTopsList[i + 3] == sleeveTexColor:
                self.clothesTopsList = self.clothesTopsList[0:i] + self.clothesTopsList[i + 4:listLen]
                return 1

        return 0

    def d_setClothesBottomsList(self, clothesList):
        self.sendUpdate('setClothesBottomsList', [clothesList])
        return None

    def setClothesBottomsList(self, clothesList):
        self.clothesBottomsList = clothesList

    def b_setClothesBottomsList(self, clothesList):
        self.setClothesBottomsList(clothesList)
        self.d_setClothesBottomsList(clothesList)

    def getClothesBottomsList(self):
        return self.clothesBottomsList

    def addToClothesBottomsList(self, botTex, botTexColor):
        if self.isClosetFull():
            self.notify.warning('clothes bottoms list is full')
            return 0
        index = 0
        for i in range(0, len(self.clothesBottomsList), 2):
            if self.clothesBottomsList[i] == botTex and self.clothesBottomsList[i + 1] == botTexColor:
                return 0

        self.clothesBottomsList.append(botTex)
        self.clothesBottomsList.append(botTexColor)
        return 1

    def replaceItemInClothesBottomsList(self, botTexA, botTexColorA, botTexB, botTexColorB):
        index = 0
        for i in range(0, len(self.clothesBottomsList), 2):
            if self.clothesBottomsList[i] == botTexA and self.clothesBottomsList[i + 1] == botTexColorA:
                self.clothesBottomsList[i] = botTexB
                self.clothesBottomsList[i + 1] = botTexColorB
                return 1

        return 0

    def removeItemInClothesBottomsList(self, botTex, botTexColor):
        listLen = len(self.clothesBottomsList)
        if listLen < 2:
            self.notify.warning('Clothes bottoms list is not long enough to delete anything')
            return 0
        index = 0
        for i in range(0, len(self.clothesBottomsList), 2):
            if self.clothesBottomsList[i] == botTex and self.clothesBottomsList[i + 1] == botTexColor:
                self.clothesBottomsList = self.clothesBottomsList[0:i] + self.clothesBottomsList[i + 2:listLen]
                return 1

        return 0

    def d_catalogGenClothes(self):
        self.sendUpdate('catalogGenClothes', [self.doId])

    def d_catalogGenAccessories(self):
        self.sendUpdate('catalogGenAccessories', [self.doId])

    def takeDamage(self, hpLost, quietly = 0, sendTotal = 1):
        if not self.immortalMode:
            if not quietly:
                self.sendUpdate('takeDamage', [hpLost])
            if hpLost > 0 and self.hp > 0:
                self.hp -= hpLost
                if self.hp <= 0:
                    self.hp = -1
                    messenger.send(self.getGoneSadMessage())
        if not self.hpOwnedByBattle:
            self.hp = min(self.hp, self.maxHp)
            if sendTotal:
                self.d_setHp(self.hp)

    @staticmethod
    def getGoneSadMessageForAvId(avId):
        return 'goneSad-%s' % avId

    def getGoneSadMessage(self):
        return self.getGoneSadMessageForAvId(self.doId)

    def setHp(self, hp):
        DistributedPlayerAI.DistributedPlayerAI.setHp(self, hp)
        if hp <= 0:
            messenger.send(self.getGoneSadMessage())

    def b_setMaxHp(self, maxHp):
        if maxHp > ToontownGlobals.MaxHpLimit:
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon tried to go over 137 laff.')
        maxHp = min(maxHp, ToontownGlobals.MaxHpLimit)
        DistributedAvatarAI.DistributedAvatarAI.b_setMaxHp(self, maxHp)

    def b_setTutorialAck(self, tutorialAck):
        self.d_setTutorialAck(tutorialAck)
        self.setTutorialAck(tutorialAck)

    def d_setTutorialAck(self, tutorialAck):
        self.sendUpdate('setTutorialAck', [tutorialAck])

    def setTutorialAck(self, tutorialAck):
        self.tutorialAck = tutorialAck

    def getTutorialAck(self):
        return self.tutorialAck

    def d_setEarnedExperience(self, earnedExp):
        self.sendUpdate('setEarnedExperience', [earnedExp])

    def setInterface(self, string):
        self.notify.debug('setting interface to %s' % string)

    def getInterface(self):
        return ''

    def setZonesVisited(self, hoods):
        self.safeZonesVisited = hoods
        self.notify.debug('setting safe zone list to %s' % self.safeZonesVisited)

    def getZonesVisited(self):
        return self.safeZonesVisited

    def setHoodsVisited(self, hoods):
        self.hoodsVisited = hoods
        self.notify.debug('setting hood zone list to %s' % self.hoodsVisited)

    def getHoodsVisited(self):
        return self.hoodsVisited

    def setLastHood(self, hood):
        self.lastHood = hood

    def d_setLastHood(self, hood):
        self.sendUpdate('setLastHood', [hood])

    def b_setLastHood(self, hood):
        if self.lastHood == hood:
            return
        self.setLastHood(hood)
        self.d_setLastHood(hood)

    def getLastHood(self):
        return self.lastHood

    def b_setAnimState(self, animName, animMultiplier):
        self.setAnimState(animName, animMultiplier)
        self.d_setAnimState(animName, animMultiplier)

    def d_setAnimState(self, animName, animMultiplier):
        timestamp = globalClockDelta.getRealNetworkTime()
        self.sendUpdate('setAnimState', [animName, animMultiplier, timestamp])
        return None

    def setAnimState(self, animName, animMultiplier, timestamp = 0):
        if animName not in ToontownGlobals.ToonAnimStates:
            desc = 'tried to set invalid animState: %s' % (animName,)
            if config.GetBool('want-ban-animstate', 1):
                #simbase.air.banManager.ban(self.doId, self.DISLid, desc)
                pass
            else:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue=desc)
            return
        self.animName = animName
        self.animMultiplier = animMultiplier

    def b_setCogStatus(self, cogStatusList):
        self.setCogStatus(cogStatusList)
        self.d_setCogStatus(cogStatusList)

    def setCogStatus(self, cogStatusList):
        self.notify.debug('setting cogs to %s' % cogStatusList)
        self.cogs = cogStatusList

    def d_setCogStatus(self, cogStatusList):
        self.sendUpdate('setCogStatus', [cogStatusList])

    def getCogStatus(self):
        return self.cogs

    def b_setCogCount(self, cogCountList):
        self.setCogCount(cogCountList)
        self.d_setCogCount(cogCountList)

    def setCogCount(self, cogCountList):
        self.notify.debug('setting cogCounts to %s' % cogCountList)
        self.cogCounts = cogCountList

    def d_setCogCount(self, cogCountList):
        self.sendUpdate('setCogCount', [cogCountList])

    def getCogCount(self):
        return self.cogCounts

    def b_setCogRadar(self, radar):
        self.setCogRadar(radar)
        self.d_setCogRadar(radar)

    def setCogRadar(self, radar):
        if not radar:
            self.notify.warning('cogRadar set to bad value: %s. Resetting to [0,0,0,0]' % radar)
            self.cogRadar = [0,
             0,
             0,
             0]
        else:
            self.cogRadar = radar

    def d_setCogRadar(self, radar):
        self.sendUpdate('setCogRadar', [radar])

    def getCogRadar(self):
        return self.cogRadar

    def b_setBuildingRadar(self, radar):
        self.setBuildingRadar(radar)
        self.d_setBuildingRadar(radar)

    def setBuildingRadar(self, radar):
        if not radar:
            self.notify.warning('buildingRadar set to bad value: %s. Resetting to [0,0,0,0]' % radar)
            self.buildingRadar = [0,
             0,
             0,
             0]
        else:
            self.buildingRadar = radar

    def d_setBuildingRadar(self, radar):
        self.sendUpdate('setBuildingRadar', [radar])

    def getBuildingRadar(self):
        return self.buildingRadar

    def b_setCogTypes(self, types):
        self.setCogTypes(types)
        self.d_setCogTypes(types)

    def setCogTypes(self, types):
        if not types:
            self.notify.warning('cogTypes set to bad value: %s. Resetting to [0,0,0,0]' % types)
            self.cogTypes = [0,
             0,
             0,
             0]
        else:
            self.cogTypes = types

    def d_setCogTypes(self, types):
        self.sendUpdate('setCogTypes', [types])

    def getCogTypes(self):
        return self.cogTypes

    def b_setCogLevels(self, levels):
        self.setCogLevels(levels)
        self.d_setCogLevels(levels)

    def setCogLevels(self, levels):
        if not levels:
            self.notify.warning('cogLevels set to bad value: %s. Resetting to [0,0,0,0]' % levels)
            self.cogLevels = [0,
             0,
             0,
             0]
        else:
            self.cogLevels = levels

    def d_setCogLevels(self, levels):
        self.sendUpdate('setCogLevels', [levels])

    def getCogLevels(self):
        return self.cogLevels

    def incCogLevel(self, dept):
        newLevel = self.cogLevels[dept] + 1
        cogTypeStr = SuitDNA.suitHeadTypes[self.cogTypes[dept]]
        lastCog = self.cogTypes[dept] >= SuitDNA.suitsPerDept - 1
        if not lastCog:
            maxLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level'] + 4
        else:
            maxLevel = ToontownGlobals.MaxCogSuitLevel
        if newLevel > maxLevel:
            if not lastCog:
                self.cogTypes[dept] += 1
                self.d_setCogTypes(self.cogTypes)
                cogTypeStr = SuitDNA.suitHeadTypes[self.cogTypes[dept]]
                self.cogLevels[dept] = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']
                self.d_setCogLevels(self.cogLevels)
        else:
            self.cogLevels[dept] += 1
            self.d_setCogLevels(self.cogLevels)
            if lastCog:
                if self.cogLevels[dept] in ToontownGlobals.CogSuitHPLevels:
                    maxHp = self.getMaxHp()
                    maxHp = min(ToontownGlobals.MaxHpLimit, maxHp + 1)
                    self.b_setMaxHp(maxHp)
                    self.toonUp(maxHp)
        self.air.writeServerEvent('cogSuit', avId=self.doId, dept=dept, suitType=self.cogTypes[dept], level=self.cogLevels[dept])

    def getNumPromotions(self, dept):
        if dept not in SuitDNA.suitDepts:
            self.notify.warning('getNumPromotions: Invalid parameter dept=%s' % dept)
            return 0
        deptIndex = SuitDNA.suitDepts.index(dept)
        cogType = self.cogTypes[deptIndex]
        cogTypeStr = SuitDNA.suitHeadTypes[cogType]
        lowestCogLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']
        multiple = 5 * cogType
        additional = self.cogLevels[deptIndex] - lowestCogLevel
        numPromotions = multiple + additional
        return numPromotions

    def b_setCogParts(self, parts):
        self.setCogParts(parts)
        self.d_setCogParts(parts)

    def setCogParts(self, parts):
        if not parts:
            self.notify.warning('cogParts set to bad value: %s. Resetting to [0,0,0,0]' % parts)
            self.cogParts = [0,
             0,
             0,
             0]
        else:
            self.cogParts = parts

    def d_setCogParts(self, parts):
        self.sendUpdate('setCogParts', [parts])

    def getCogParts(self):
        return self.cogParts

    def giveCogPart(self, part, dept):
        dept = CogDisguiseGlobals.dept2deptIndex(dept)
        parts = self.getCogParts()
        parts[dept] = parts[dept] | part
        self.b_setCogParts(parts)

    def hasCogPart(self, part, dept):
        dept = CogDisguiseGlobals.dept2deptIndex(dept)
        if self.cogParts[dept] & part:
            return 1
        else:
            return 0

    def giveGenericCogPart(self, factoryType, dept):
        for partTypeId in self.partTypeIds[factoryType]:
            nextPart = CogDisguiseGlobals.getNextPart(self.getCogParts(), partTypeId, dept)
            if nextPart:
                break

        if nextPart:
            self.giveCogPart(nextPart, dept)
            return nextPart
        else:
            return None
        return None

    def takeCogPart(self, part, dept):
        dept = CogDisguiseGlobals.dept2deptIndex(dept)
        parts = self.getCogParts()
        if parts[dept] & part:
            parts[dept] = parts[dept] ^ part
            self.b_setCogParts(parts)

    def loseCogParts(self, dept):
        loseCount = random.randrange(CogDisguiseGlobals.MinPartLoss, CogDisguiseGlobals.MaxPartLoss + 1)
        parts = self.getCogParts()
        partBitmask = parts[dept]
        partList = range(17)
        while loseCount > 0 and partList:
            losePart = random.choice(partList)
            partList.remove(losePart)
            losePartBit = 1 << losePart
            if partBitmask & losePartBit:
                partBitmask &= ~losePartBit
                loseCount -= 1

        parts[dept] = partBitmask
        self.b_setCogParts(parts)

    def b_setCogMerits(self, merits):
        self.setCogMerits(merits)
        self.d_setCogMerits(merits)

    def setCogMerits(self, merits):
        if not merits:
            self.notify.warning('cogMerits set to bad value: %s. Resetting to [0,0,0,0]' % merits)
            self.cogMerits = [0,
             0,
             0,
             0]
        else:
            self.cogMerits = merits

    def d_setCogMerits(self, merits):
        self.sendUpdate('setCogMerits', [merits])

    def getCogMerits(self):
        return self.cogMerits

    def b_promote(self, dept):
        self.promote(dept)
        self.d_promote(dept)

    def promote(self, dept):
        if self.cogLevels[dept] < ToontownGlobals.MaxCogSuitLevel:
            self.cogMerits[dept] = 0
        self.incCogLevel(dept)

    def d_promote(self, dept):
        merits = self.getCogMerits()
        if self.cogLevels[dept] < ToontownGlobals.MaxCogSuitLevel:
            merits[dept] = 0
        self.d_setCogMerits(merits)

    def readyForPromotion(self, dept):
        merits = self.cogMerits[dept]
        totalMerits = CogDisguiseGlobals.getTotalMerits(self, dept)
        if merits >= totalMerits:
            return 1
        else:
            return 0

    def b_setCogIndex(self, index):
        self.setCogIndex(index)
        if simbase.config.GetBool('cogsuit-hack-prevent', False):
            self.d_setCogIndex(self.cogIndex)
        else:
            self.d_setCogIndex(index)

    def setCogIndex(self, index):
        '''if index != -1 and not ToontownAccessAI.canWearSuit(self.doId, self.zoneId):
            if not simbase.air.cogSuitMessageSent:
                self.notify.warning('%s setCogIndex invalid: %s' % (self.doId, index))
                if simbase.config.GetBool('want-ban-wrong-suit-place', False):
                    commentStr = 'Toon %s trying to set cog index to %s in Zone: %s' % (self.doId, index, self.zoneId)
                    #simbase.air.banManager.ban(self.doId, self.DISLid, commentStr)
        else:'''
        self.cogIndex = index

    def d_setCogIndex(self, index):
        self.sendUpdate('setCogIndex', [index])

    def getCogIndex(self):
        return self.cogIndex

    def b_setDisguisePageFlag(self, flag):
        self.setDisguisePageFlag(flag)
        self.d_setDisguisePageFlag(flag)

    def setDisguisePageFlag(self, flag):
        self.disguisePageFlag = flag

    def d_setDisguisePageFlag(self, flag):
        self.sendUpdate('setDisguisePageFlag', [flag])

    def getDisguisePageFlag(self):
        return self.disguisePageFlag

    def b_setSosPageFlag(self, flag):
        self.setSosPageFlag(flag)
        self.d_setSosPageFlag(flag)

    def setSosPageFlag(self, flag):
        self.sosPageFlag = flag

    def d_setSosPageFlag(self, flag):
        self.sendUpdate('setSosPageFlag', [flag])

    def getSosPageFlag(self):
        return self.sosPageFlag

    def b_setFishCollection(self, genusList, speciesList, weightList):
        self.setFishCollection(genusList, speciesList, weightList)
        self.d_setFishCollection(genusList, speciesList, weightList)

    def d_setFishCollection(self, genusList, speciesList, weightList):
        self.sendUpdate('setFishCollection', [genusList, speciesList, weightList])

    def setFishCollection(self, genusList, speciesList, weightList):
        self.fishCollection = FishCollection.FishCollection()
        self.fishCollection.makeFromNetLists(genusList, speciesList, weightList)

    def getFishCollection(self):
        return self.fishCollection.getNetLists()

    def b_setMaxFishTank(self, maxTank):
        self.d_setMaxFishTank(maxTank)
        self.setMaxFishTank(maxTank)

    def d_setMaxFishTank(self, maxTank):
        self.sendUpdate('setMaxFishTank', [maxTank])

    def setMaxFishTank(self, maxTank):
        self.maxFishTank = maxTank

    def getMaxFishTank(self):
        return self.maxFishTank

    def b_setFishTank(self, genusList, speciesList, weightList):
        self.setFishTank(genusList, speciesList, weightList)
        self.d_setFishTank(genusList, speciesList, weightList)

    def d_setFishTank(self, genusList, speciesList, weightList):
        self.sendUpdate('setFishTank', [genusList, speciesList, weightList])

    def setFishTank(self, genusList, speciesList, weightList):
        self.fishTank = FishTank.FishTank()
        self.fishTank.makeFromNetLists(genusList, speciesList, weightList)

    def getFishTank(self):
        return self.fishTank.getNetLists()

    def makeRandomFishTank(self):
        self.fishTank.generateRandomTank()
        self.d_setFishTank(*self.fishTank.getNetLists())

    def addFishToTank(self, fish):
        numFish = len(self.fishTank)
        if numFish >= self.maxFishTank:
            self.notify.warning('addFishToTank: cannot add fish, tank is full')
            return 0
        elif self.fishTank.addFish(fish):
            self.d_setFishTank(*self.fishTank.getNetLists())
            return 1
        else:
            self.notify.warning('addFishToTank: addFish failed')
            return 0

    def removeFishFromTankAtIndex(self, index):
        if self.fishTank.removeFishAtIndex(index):
            self.d_setFishTank(*self.fishTank.getNetLists())
            return 1
        else:
            self.notify.warning('removeFishFromTank: cannot find fish')
            return 0

    def b_setFishingRod(self, rodId):
        self.d_setFishingRod(rodId)
        self.setFishingRod(rodId)

    def d_setFishingRod(self, rodId):
        self.sendUpdate('setFishingRod', [rodId])

    def setFishingRod(self, rodId):
        self.fishingRod = rodId

    def getFishingRod(self):
        return self.fishingRod

    def b_setFishingTrophies(self, trophyList):
        self.setFishingTrophies(trophyList)
        self.d_setFishingTrophies(trophyList)

    def setFishingTrophies(self, trophyList):
        self.notify.debug('setting fishingTrophies to %s' % trophyList)
        self.fishingTrophies = trophyList

    def d_setFishingTrophies(self, trophyList):
        self.sendUpdate('setFishingTrophies', [trophyList])

    def getFishingTrophies(self):
        return self.fishingTrophies

    def b_setQuests(self, questList):
        flattenedQuests = []
        if len(questList) > self.getQuestCarryLimit():
            self.air.writeServerEvent('suspicious', avId=self.getDoId(), issue='Attempted to set %d quests on toon when limit is %d!' % (len(questList), self.getQuestCarryLimit()))
            return
        for quest in questList:
            flattenedQuests.extend(quest)

        self.setQuests(flattenedQuests)
        self.d_setQuests(flattenedQuests)

    def d_setQuests(self, flattenedQuests):
        self.sendUpdate('setQuests', [flattenedQuests])

    def setQuests(self, flattenedQuests):
        self.notify.debug('setting quests to %s' % flattenedQuests)
        questList = []
        questLen = 5
        for i in range(0, len(flattenedQuests), questLen):
            questList.append(flattenedQuests[i:i + questLen])

        self.quests = questList
        self.hasQuests = True

    def updateQuests(self):
        if self.hasQuests:
            self.d_setQuests(self.getQuests())

    def getQuests(self):
        flattenedQuests = []
        for quest in self.quests:
            flattenedQuests.extend(quest)

        return flattenedQuests

    def getQuest(self, questId, visitNpcId = None, rewardId = None):
        for quest in self.quests:
            if quest[0] != questId:
                continue
            if visitNpcId != None:
                if visitNpcId != quest[1] and visitNpcId != quest[2]:
                    continue
            if rewardId != None:
                if rewardId != quest[3]:
                    continue
            return quest

        return

    def hasQuest(self, questId, visitNpcId = None, rewardId = None):
        if self.getQuest(questId, visitNpcId=visitNpcId, rewardId=rewardId) == None:
            return False
        else:
            return True
        return

    def removeQuest(self, id, visitNpcId = None):
        index = -1
        for i in range(len(self.quests)):
            if self.quests[i][0] == id:
                if visitNpcId:
                    otherId = self.quests[i][2]
                    if visitNpcId == otherId:
                        index = i
                        break
                else:
                    index = i
                    break

        if index >= 0:
            del self.quests[i]
            self.b_setQuests(self.quests)
            return 1
        else:
            return 0

    def addQuest(self, quest, finalReward, recordHistory = 1):
        self.quests.append(quest)
        self.b_setQuests(self.quests)
        if recordHistory:
            if quest[0] != Quests.VISIT_QUEST_ID:
                newQuestHistory = self.questHistory + [quest[0]]
                while newQuestHistory.count(Quests.VISIT_QUEST_ID) != 0:
                    newQuestHistory.remove(Quests.VISIT_QUEST_ID)

                self.b_setQuestHistory(newQuestHistory)
                if finalReward:
                    newRewardHistory = self.rewardHistory + [finalReward]
                    self.b_setRewardHistory(self.rewardTier, newRewardHistory)

    def removeAllTracesOfQuest(self, questId, rewardId):
        self.notify.debug('removeAllTracesOfQuest: questId: %s rewardId: %s' % (questId, rewardId))
        self.notify.debug('removeAllTracesOfQuest: quests before: %s' % self.quests)
        removedQuest = self.removeQuest(questId)
        self.notify.debug('removeAllTracesOfQuest: quests after: %s' % self.quests)
        self.notify.debug('removeAllTracesOfQuest: questHistory before: %s' % self.questHistory)
        removedQuestHistory = self.removeQuestFromHistory(questId)
        self.notify.debug('removeAllTracesOfQuest: questHistory after: %s' % self.questHistory)
        self.notify.debug('removeAllTracesOfQuest: reward history before: %s' % self.rewardHistory)
        removedRewardHistory = self.removeRewardFromHistory(rewardId)
        self.notify.debug('removeAllTracesOfQuest: reward history after: %s' % self.rewardHistory)
        return (removedQuest, removedQuestHistory, removedRewardHistory)

    def requestDeleteQuest(self, questDesc):
        if len(questDesc) != 5:
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon tried to delete invalid questDesc %s' % str(questDesc))
            self.notify.warning('%s.requestDeleteQuest(%s) -- questDesc has incorrect params' % (self, str(questDesc)))
            return
        questId = questDesc[0]
        rewardId = questDesc[3]
        if not self.hasQuest(questId, rewardId=rewardId):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue="Toon tried to delete quest they don't have %s" % str(questDesc))
            self.notify.warning("%s.requestDeleteQuest(%s) -- Toon doesn't have that quest" % (self, str(questDesc)))
            return
        if not Quests.isQuestJustForFun(questId, rewardId):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon tried to delete non-Just For Fun quest %s' % str(questDesc))
            self.notify.warning('%s.requestDeleteQuest(%s) -- Tried to cancel non-Just For Fun quest' % (self, str(questDesc)))
            return
        removedStatus = self.removeAllTracesOfQuest(questId, rewardId)
        if 0 in removedStatus:
            self.notify.warning('%s.requestDeleteQuest(%s) -- Failed to remove quest, status=%s' % (self, str(questDesc), removedStatus))

    def b_setQuestCarryLimit(self, limit):
        self.setQuestCarryLimit(limit)
        self.d_setQuestCarryLimit(limit)

    def d_setQuestCarryLimit(self, limit):
        self.sendUpdate('setQuestCarryLimit', [limit])

    def setQuestCarryLimit(self, limit):
        self.notify.debug('setting questCarryLimit to %s' % limit)
        self.questCarryLimit = limit

    def getQuestCarryLimit(self):
        return self.questCarryLimit

    def b_setMaxCarry(self, maxCarry):
        self.setMaxCarry(maxCarry)
        self.d_setMaxCarry(maxCarry)

    def d_setMaxCarry(self, maxCarry):
        self.sendUpdate('setMaxCarry', [maxCarry])

    def setMaxCarry(self, maxCarry):
        self.maxCarry = maxCarry

    def getMaxCarry(self):
        return self.maxCarry

    def b_setCheesyEffect(self, effect, hoodId, expireTime):
        self.setCheesyEffect(effect, hoodId, expireTime)
        self.d_setCheesyEffect(effect, hoodId, expireTime)

    def d_setCheesyEffect(self, effect, hoodId, expireTime):
        self.sendUpdate('setCheesyEffect', [effect, hoodId, expireTime])

    def setCheesyEffect(self, effect, hoodId, expireTime):
        # We don't yet have a working holidayManager, and we want to keep snowman heads.
        #if simbase.air.holidayManager and ToontownGlobals.WINTER_CAROLING not in simbase.air.holidayManager.currentHolidays and ToontownGlobals.WACKY_WINTER_CAROLING not in simbase.air.holidayManager.currentHolidays and effect == ToontownGlobals.CESnowMan:
            #self.b_setCheesyEffect(ToontownGlobals.CENormal, hoodId, expireTime)
            #return
        self.savedCheesyEffect = effect
        self.savedCheesyHoodId = hoodId
        self.savedCheesyExpireTime = expireTime
        if config.GetBool('want-cheesy-expirations', self.air.doLiveUpdates):
            taskName = self.uniqueName('cheesy-expires')
            taskMgr.remove(taskName)
            if effect != ToontownGlobals.CENormal:
                duration = expireTime - time.time()
                if duration > 0:
                    taskMgr.doMethodLater(duration, self.__undoCheesyEffect, taskName)
                else:
                    self.__undoCheesyEffect(None)
        return

    def getCheesyEffect(self):
        return (self.savedCheesyEffect, self.savedCheesyHoodId, self.savedCheesyExpireTime)

    def __undoCheesyEffect(self, task):
        self.b_setCheesyEffect(ToontownGlobals.CENormal, 0, 0)
        return Task.cont

    def b_setTrackAccess(self, trackArray):
        self.setTrackAccess(trackArray)
        self.d_setTrackAccess(trackArray)

    def d_setTrackAccess(self, trackArray):
        self.sendUpdate('setTrackAccess', [trackArray])

    def setTrackAccess(self, trackArray):
        self.trackArray = trackArray

    def getTrackAccess(self):
        return self.trackArray

    def addTrackAccess(self, track):
        self.trackArray[track] = 1
        self.b_setTrackAccess(self.trackArray)

    def removeTrackAccess(self, track):
        self.trackArray[track] = 0
        self.b_setTrackAccess(self.trackArray)

    def hasTrackAccess(self, track):
        if self.trackArray and track < len(self.trackArray):
            return self.trackArray[track]
        else:
            return 0

    def fixTrackAccess(self):
        fixed = 0
        healExp, trapExp, lureExp, soundExp, throwExp, squirtExp, dropExp = self.experience.experience
        numTracks = reduce(lambda a, b: a + b, self.trackArray)
        if self.rewardTier in [0,
         1,
         2,
         3]:
            if numTracks != 2:
                self.notify.warning('bad num tracks in tier: %s, %s' % (self.rewardTier, self.trackArray))
                self.b_setTrackAccess([0, 0, 0, 0, 1, 1, 0])
                fixed = 1
        elif self.rewardTier in [4, 5, 6]:
            if numTracks != 3:
                self.notify.warning('bad num tracks in tier: %s, %s' % (self.rewardTier, self.trackArray))
                if self.trackArray[ToontownBattleGlobals.SOUND_TRACK] and not self.trackArray[ToontownBattleGlobals.HEAL_TRACK]:
                    self.b_setTrackAccess([0, 0, 0, 1, 1, 1, 0])
                elif self.trackArray[ToontownBattleGlobals.HEAL_TRACK] and not self.trackArray[ToontownBattleGlobals.SOUND_TRACK]:
                    self.b_setTrackAccess([1, 0, 0, 0, 1, 1, 0])
                elif soundExp >= healExp:
                    self.b_setTrackAccess([0, 0, 0, 1, 1, 1, 0])
                else:
                    self.b_setTrackAccess([1, 0, 0, 0, 1, 1, 0])
                fixed = 1
        elif self.rewardTier in [7, 8, 9, 10]:
            if numTracks != 4:
                self.notify.warning('bad num tracks in tier: %s, %s' % (self.rewardTier, self.trackArray))
                if self.trackArray[ToontownBattleGlobals.SOUND_TRACK] and not self.trackArray[ToontownBattleGlobals.HEAL_TRACK]:
                    if dropExp >= lureExp:
                        self.b_setTrackAccess([0, 0, 0, 1, 1, 1, 1])
                    else:
                        self.b_setTrackAccess([0, 0, 1, 1, 1, 1, 0])
                elif self.trackArray[ToontownBattleGlobals.HEAL_TRACK] and not self.trackArray[ToontownBattleGlobals.SOUND_TRACK]:
                    if dropExp >= lureExp:
                        self.b_setTrackAccess([1, 0, 0, 0, 1, 1, 1])
                    else:
                        self.b_setTrackAccess([1, 0, 1, 0, 1, 1, 0])
                elif soundExp >= healExp:
                    if dropExp >= lureExp:
                        self.b_setTrackAccess([0, 0, 0, 1, 1, 1, 1])
                    else:
                        self.b_setTrackAccess([0, 0, 1, 1, 1, 1, 0])
                elif dropExp >= lureExp:
                    self.b_setTrackAccess([1, 0, 0, 0, 1, 1, 1])
                else:
                    self.b_setTrackAccess([1, 0, 1, 0, 1, 1, 0])
                fixed = 1
        elif self.rewardTier in [11, 12, 13]:
            if numTracks != 5:
                self.notify.warning('bad num tracks in tier: %s, %s' % (self.rewardTier, self.trackArray))
                if self.trackArray[ToontownBattleGlobals.SOUND_TRACK] and not self.trackArray[ToontownBattleGlobals.HEAL_TRACK]:
                    if self.trackArray[ToontownBattleGlobals.DROP_TRACK] and not self.trackArray[ToontownBattleGlobals.LURE_TRACK]:
                        if healExp >= trapExp:
                            self.b_setTrackAccess([1, 0, 0, 1, 1, 1, 1])
                        else:
                            self.b_setTrackAccess([0, 1, 0, 1, 1, 1, 1])
                    elif healExp >= trapExp:
                        self.b_setTrackAccess([1, 0, 1, 1, 1, 1, 0])
                    else:
                        self.b_setTrackAccess([0, 1, 1, 1, 1, 1, 0])
                elif self.trackArray[ToontownBattleGlobals.HEAL_TRACK] and not self.trackArray[ToontownBattleGlobals.SOUND_TRACK]:
                    if self.trackArray[ToontownBattleGlobals.DROP_TRACK] and not self.trackArray[ToontownBattleGlobals.LURE_TRACK]:
                        if soundExp >= trapExp:
                            self.b_setTrackAccess([1, 0, 0, 1, 1, 1, 1])
                        else:
                            self.b_setTrackAccess([1, 1, 0, 0, 1, 1, 1])
                    elif soundExp >= trapExp:
                        self.b_setTrackAccess([1, 0, 1, 1, 1, 1, 0])
                    else:
                        self.b_setTrackAccess([1, 1, 1, 0, 1, 1, 0])
                fixed = 1
        elif numTracks != 6:
            self.notify.warning('bad num tracks in tier: %s, %s' % (self.rewardTier, self.trackArray))
            sortedExp = [healExp,
             trapExp,
             lureExp,
             soundExp,
             dropExp]
            sortedExp.sort()
            if trapExp == sortedExp[0]:
                self.b_setTrackAccess([1, 0, 1, 1, 1, 1, 1])
            elif lureExp == sortedExp[0]:
                self.b_setTrackAccess([1, 1, 0, 1, 1, 1, 1])
            elif dropExp == sortedExp[0]:
                self.b_setTrackAccess([1, 1, 1, 1, 1, 1, 0])
            elif soundExp == sortedExp[0]:
                self.b_setTrackAccess([1, 1, 1, 0, 1, 1, 1])
            elif healExp == sortedExp[0]:
                self.b_setTrackAccess([0, 1, 1, 1, 1, 1, 1])
            else:
                self.notify.warning('invalid exp?!: %s, %s' % (sortedExp, self.trackArray))
                self.b_setTrackAccess([1, 0, 1, 1, 1, 1, 1])
            fixed = 1
        if fixed:
            self.inventory.zeroInv()
            self.inventory.maxOutInv()
            self.d_setInventory(self.inventory.makeNetString())
            self.notify.info('fixed tracks: %s' % self.trackArray)
        return fixed

    def b_setTrackProgress(self, trackId, progress):
        self.setTrackProgress(trackId, progress)
        self.d_setTrackProgress(trackId, progress)

    def d_setTrackProgress(self, trackId, progress):
        self.sendUpdate('setTrackProgress', [trackId, progress])

    def setTrackProgress(self, trackId, progress):
        self.trackProgressId = trackId
        self.trackProgress = progress

    def addTrackProgress(self, trackId, progressIndex):
        if self.trackProgressId != trackId:
            self.notify.warning('tried to update progress on a track toon is not training')
        newProgress = self.trackProgress | 1 << progressIndex - 1
        self.b_setTrackProgress(self.trackProgressId, newProgress)

    def clearTrackProgress(self):
        self.b_setTrackProgress(-1, 0)

    def getTrackProgress(self):
        return [self.trackProgressId, self.trackProgress]

    def b_setHoodsVisited(self, hoodsVisitedArray):
        self.hoodsVisited = hoodsVisitedArray
        self.d_setHoodsVisited(hoodsVisitedArray)

    def d_setHoodsVisited(self, hoodsVisitedArray):
        self.sendUpdate('setHoodsVisited', [hoodsVisitedArray])

    def b_setTeleportAccess(self, teleportZoneArray):
        self.setTeleportAccess(teleportZoneArray)
        self.d_setTeleportAccess(teleportZoneArray)

    def d_setTeleportAccess(self, teleportZoneArray):
        self.sendUpdate('setTeleportAccess', [teleportZoneArray])

    def setTeleportAccess(self, teleportZoneArray):
        self.teleportZoneArray = teleportZoneArray

    def getTeleportAccess(self):
        return self.teleportZoneArray

    def hasTeleportAccess(self, zoneId):
        return zoneId in self.teleportZoneArray

    def addTeleportAccess(self, zoneId):
        if zoneId not in self.teleportZoneArray:
            self.teleportZoneArray.append(zoneId)
            self.b_setTeleportAccess(self.teleportZoneArray)

    def removeTeleportAccess(self, zoneId):
        if zoneId in self.teleportZoneArray:
            self.teleportZoneArray.remove(zoneId)
            self.b_setTeleportAccess(self.teleportZoneArray)

    def checkTeleportAccess(self, zoneId):
        if zoneId not in self.getTeleportAccess() and self.teleportOverride != 1:
            simbase.air.writeServerEvent('suspicious', avId=self.doId, issue='Toon teleporting to zone %s they do not have access to.' % zoneId)
            if simbase.config.GetBool('want-ban-teleport', False):
                commentStr = 'Toon %s teleporting to a zone %s they do not have access to' % (self.doId, zoneId)
                #simbase.air.banManager.ban(self.doId, self.DISLid, commentStr)

    def setTeleportOverride(self, flag):
        self.teleportOverride = flag
        self.b_setHoodsVisited([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000])

    def b_setQuestHistory(self, questList):
        self.setQuestHistory(questList)
        self.d_setQuestHistory(questList)

    def d_setQuestHistory(self, questList):
        self.sendUpdate('setQuestHistory', [questList])

    def setQuestHistory(self, questList):
        self.notify.debug('setting quest history to %s' % questList)
        self.questHistory = questList

    def getQuestHistory(self):
        return self.questHistory

    def removeQuestFromHistory(self, questId):
        if questId in self.questHistory:
            self.questHistory.remove(questId)
            self.d_setQuestHistory(self.questHistory)
            return 1
        else:
            return 0

    def removeRewardFromHistory(self, rewardId):
        rewardTier, rewardHistory = self.getRewardHistory()
        if rewardId in rewardHistory:
            rewardHistory.remove(rewardId)
            self.b_setRewardHistory(rewardTier, rewardHistory)
            return 1
        else:
            return 0

    def b_setRewardHistory(self, tier, rewardList):
        self.setRewardHistory(tier, rewardList)
        self.d_setRewardHistory(tier, rewardList)

    def d_setRewardHistory(self, tier, rewardList):
        self.sendUpdate('setRewardHistory', [tier, rewardList])

    def setRewardHistory(self, tier, rewardList):
        self.air.writeServerEvent('questTier', avId=self.getDoId(), tier=str(tier))
        self.notify.debug('setting reward history to tier %s, %s' % (tier, rewardList))
        self.rewardTier = tier
        self.rewardHistory = rewardList

    def getRewardHistory(self):
        return (self.rewardTier, self.rewardHistory)

    def getRewardTier(self):
        return self.rewardTier

    def fixAvatar(self):
        anyChanged = 0
        qrc = QuestRewardCounter.QuestRewardCounter()
        if qrc.fixAvatar(self):
            self.notify.info("Fixed avatar %d's quest rewards." % self.doId)
            anyChanged = 1
        if self.hp > self.maxHp:
            self.notify.info('Changed avatar %d to have hp %d instead of %d, to fit with maxHp' % (self.doId, self.maxHp, self.hp))
            self.b_setHp(self.maxHp)
            anyChanged = 1
        inventoryChanged = 0
        carry = self.maxCarry
        for track in range(len(ToontownBattleGlobals.Tracks)):
            if not self.hasTrackAccess(track):
                for level in range(len(ToontownBattleGlobals.Levels[track])):
                    count = self.inventory.inventory[track][level]
                    if count != 0:
                        self.notify.info('Changed avatar %d to throw away %d items in track %d level %d; no access to track.' % (self.doId,
                         count,
                         track,
                         level))
                        self.inventory.inventory[track][level] = 0
                        inventoryChanged = 1

            else:
                curSkill = self.experience.getExp(track)
                for level in range(len(ToontownBattleGlobals.Levels[track])):
                    count = self.inventory.inventory[track][level]
                    if curSkill < ToontownBattleGlobals.Levels[track][level]:
                        if count != 0:
                            self.notify.info('Changed avatar %d to throw away %d items in track %d level %d; no access to level.' % (self.doId,
                             count,
                             track,
                             level))
                            self.inventory.inventory[track][level] = 0
                            inventoryChanged = 1
                    else:
                        newCount = min(count, carry)
                        newCount = min(count, self.inventory.getMax(track, level))
                        if count != newCount:
                            self.notify.info('Changed avatar %d to throw away %d items in track %d level %d; too many gags.' % (self.doId,
                             count - newCount,
                             track,
                             level))
                            self.inventory.inventory[track][level] = newCount
                            inventoryChanged = 1
                        carry -= newCount

        self.inventory.calcTotalProps()
        if inventoryChanged:
            self.d_setInventory(self.inventory.makeNetString())
            anyChanged = 1
        if len(self.quests) > self.questCarryLimit:
            self.notify.info('Changed avatar %d to throw out %d quests; too many quests.' % (self.doId, len(self.quests) - self.questCarryLimit))
            self.b_setQuests(self.quests[:self.questCarryLimit])
            self.fixAvatar()
            anyChanged = 1
        if not (self.emoteAccess[0] and self.emoteAccess[1] and self.emoteAccess[2] and self.emoteAccess[3] and self.emoteAccess[4]):
            self.emoteAccess[0] = 1
            self.emoteAccess[1] = 1
            self.emoteAccess[2] = 1
            self.emoteAccess[3] = 1
            self.emoteAccess[4] = 1
            self.b_setEmoteAccess(self.emoteAccess)
            self.notify.info('Changed avatar %d to have emoteAccess: %s' % (self.doId, self.emoteAccess))
            anyChanged = 1
        return anyChanged

    def b_setEmoteAccess(self, bits):
        self.setEmoteAccess(bits)
        self.d_setEmoteAccess(bits)

    def d_setEmoteAccess(self, bits):
        self.sendUpdate('setEmoteAccess', [bits])

    def setEmoteAccess(self, bits):
        if len(bits) == 20:
            bits.extend([0,
             0,
             0,
             0,
             0])
            self.b_setEmoteAccess(bits)
        elif len(bits) != len(self.emoteAccess):
            self.notify.warning('New emote access list must be the same size as the old one.')
            return
        self.emoteAccess = bits

    def getEmoteAccess(self):
        return self.emoteAccess

    def setEmoteAccessId(self, id, bit):
        self.emoteAccess[id] = bit
        self.d_setEmoteAccess(self.emoteAccess)

    def b_setHouseId(self, id):
        self.setHouseId(id)
        self.d_setHouseId(id)

    def d_setHouseId(self, id):
        self.sendUpdate('setHouseId', [id])

    def setHouseId(self, id):
        self.houseId = id

    def getHouseId(self):
        return self.houseId

    def setPosIndex(self, index):
        self.posIndex = index

    def getPosIndex(self):
        return self.posIndex

    def b_setCustomMessages(self, customMessages):
        self.d_setCustomMessages(customMessages)
        self.setCustomMessages(customMessages)

    def d_setCustomMessages(self, customMessages):
        self.sendUpdate('setCustomMessages', [customMessages])

    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages

    def getCustomMessages(self):
        return self.customMessages

    def b_setResistanceMessages(self, resistanceMessages):
        self.d_setResistanceMessages(resistanceMessages)
        self.setResistanceMessages(resistanceMessages)

    def d_setResistanceMessages(self, resistanceMessages):
        self.sendUpdate('setResistanceMessages', [resistanceMessages])

    def setResistanceMessages(self, resistanceMessages):
        self.resistanceMessages = resistanceMessages

    def getResistanceMessages(self):
        return self.resistanceMessages

    def addResistanceMessage(self, textId):
        msgs = self.getResistanceMessages()
        for i in range(len(msgs)):
            if msgs[i][0] == textId:
                msgs[i][1] += 1
                self.b_setResistanceMessages(msgs)
                return

        msgs.append([textId, 1])
        self.b_setResistanceMessages(msgs)

    def removeResistanceMessage(self, textId):
        msgs = self.getResistanceMessages()
        for i in range(len(msgs)):
            if msgs[i][0] == textId:
                msgs[i][1] -= 1
                if msgs[i][1] <= 0:
                    del msgs[i]
                self.b_setResistanceMessages(msgs)
                return 1

        self.notify.warning("Toon %s doesn't have resistance message %s" % (self.doId, textId))
        return 0

    def restockAllResistanceMessages(self, charges = 1):
        from toontown.chat import ResistanceChat
        msgs = []
        for menuIndex in ResistanceChat.resistanceMenu:
            for itemIndex in ResistanceChat.getItems(menuIndex):
                textId = ResistanceChat.encodeId(menuIndex, itemIndex)
                msgs.append([textId, charges])

        self.b_setResistanceMessages(msgs)

    def b_setCatalogSchedule(self, currentWeek, nextTime):
        self.setCatalogSchedule(currentWeek, nextTime)
        self.d_setCatalogSchedule(currentWeek, nextTime)

    def d_setCatalogSchedule(self, currentWeek, nextTime):
        self.sendUpdate('setCatalogSchedule', [currentWeek, nextTime])

    def setCatalogSchedule(self, currentWeek, nextTime):
        self.catalogScheduleCurrentWeek = currentWeek
        self.catalogScheduleNextTime = nextTime
        if self.air.doLiveUpdates:
            taskName = self.uniqueName('next-catalog')
            taskMgr.remove(taskName)
            duration = max(10.0, nextTime * 60 - time.time())
            taskMgr.doMethodLater(duration, self.__deliverCatalog, taskName)

    def getCatalogSchedule(self):
        return (self.catalogScheduleCurrentWeek, self.catalogScheduleNextTime)

    def __deliverCatalog(self, task):
        self.air.catalogManager.deliverCatalogFor(self)
        return Task.done

    def b_setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)
        self.d_setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)

    def d_setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.sendUpdate('setCatalog', [monthlyCatalog.getBlob(), weeklyCatalog.getBlob(), backCatalog.getBlob()])

    def setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.monthlyCatalog = CatalogItemList.CatalogItemList(monthlyCatalog)
        self.weeklyCatalog = CatalogItemList.CatalogItemList(weeklyCatalog)
        self.backCatalog = CatalogItemList.CatalogItemList(backCatalog)

    def getCatalog(self):
        return (self.monthlyCatalog.getBlob(), self.weeklyCatalog.getBlob(), self.backCatalog.getBlob())

    def b_setCatalogNotify(self, catalogNotify, mailboxNotify):
        self.setCatalogNotify(catalogNotify, mailboxNotify)
        self.d_setCatalogNotify(catalogNotify, mailboxNotify)

    def d_setCatalogNotify(self, catalogNotify, mailboxNotify):
        self.sendUpdate('setCatalogNotify', [catalogNotify, mailboxNotify])

    def setCatalogNotify(self, catalogNotify, mailboxNotify):
        self.catalogNotify = catalogNotify
        self.mailboxNotify = mailboxNotify

    def getCatalogNotify(self):
        return (self.catalogNotify, self.mailboxNotify)

    def b_setDeliverySchedule(self, onOrder, doUpdateLater = True):
        self.setDeliverySchedule(onOrder, doUpdateLater)
        self.d_setDeliverySchedule(onOrder)

    def d_setDeliverySchedule(self, onOrder):
        self.sendUpdate('setDeliverySchedule', [onOrder.getBlob(store=CatalogItem.Customization | CatalogItem.DeliveryDate)])

    def setDeliverySchedule(self, onOrder, doUpdateLater = True):
        self.setBothSchedules(onOrder, None)
        return
        self.onOrder = CatalogItemList.CatalogItemList(onOrder, store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        if hasattr(self, 'name'):
            if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air'):
                taskName = self.uniqueName('next-delivery')
                taskMgr.remove(taskName)
                now = int(time.time() / 60 + 0.5)
                nextItem = None
                nextTime = self.onOrder.getNextDeliveryDate()
                nextItem = self.onOrder.getNextDeliveryItem()
                if nextItem != None:
                    pass
                if nextTime != None:
                    duration = max(10.0, nextTime * 60 - time.time())
                    taskMgr.doMethodLater(duration, self.__deliverPurchase, taskName)
        return

    def getDeliverySchedule(self):
        return self.onOrder.getBlob(store=CatalogItem.Customization | CatalogItem.DeliveryDate)

    def b_setBothSchedules(self, onOrder, onGiftOrder, doUpdateLater = True):
        self.setBothSchedules(onOrder, onGiftOrder, doUpdateLater)
        self.d_setDeliverySchedule(onOrder)

    def setBothSchedules(self, onOrder, onGiftOrder, doUpdateLater = True):
        if onOrder != None:
            self.onOrder = CatalogItemList.CatalogItemList(onOrder, store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        if onGiftOrder != None:
            self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        if not hasattr(self, 'air') or self.air == None:
            return
        if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'name'):
            taskName = 'next-bothDelivery-%s' % self.doId
            now = int(time.time() / 60 + 0.5)
            nextItem = None
            nextGiftItem = None
            nextTime = None
            nextGiftTime = None
            if self.onOrder:
                nextTime = self.onOrder.getNextDeliveryDate()
                nextItem = self.onOrder.getNextDeliveryItem()
            if self.onGiftOrder:
                nextGiftTime = self.onGiftOrder.getNextDeliveryDate()
                nextGiftItem = self.onGiftOrder.getNextDeliveryItem()
            if nextItem:
                pass
            if nextGiftItem:
                pass
            if nextTime == None:
                nextTime = nextGiftTime
            if nextGiftTime == None:
                nextGiftTime = nextTime
            if nextGiftTime < nextTime:
                nextTime = nextGiftTime
            existingDuration = None
            checkTaskList = taskMgr.getTasksNamed(taskName)
            if checkTaskList:
                currentTime = globalClock.getFrameTime()
                checkTask = checkTaskList[0]
                existingDuration = checkTask.wakeTime - currentTime
            if nextTime:
                newDuration = max(10.0, nextTime * 60 - time.time())
                if existingDuration and existingDuration >= newDuration:
                    taskMgr.remove(taskName)
                    taskMgr.doMethodLater(newDuration, self.__deliverBothPurchases, taskName)
                elif existingDuration and existingDuration < newDuration:
                    pass
                else:
                    taskMgr.doMethodLater(newDuration, self.__deliverBothPurchases, taskName)
        return

    def __deliverBothPurchases(self, task):
        now = int(time.time() / 60 + 0.5)
        delivered, remaining = self.onOrder.extractDeliveryItems(now)
        deliveredGifts, remainingGifts = self.onGiftOrder.extractDeliveryItems(now)
        simbase.air.deliveryManager.sendDeliverGifts(self.getDoId(), now)
        giftItem = CatalogItemList.CatalogItemList(deliveredGifts, store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        if len(giftItem) > 0:
            self.air.writeServerEvent('Getting Gift', avId=self.doId, msg='sender %s receiver %s gift %s' % (giftItem[0].giftTag, self.doId, giftItem[0].getName()))
        self.b_setMailboxContents(self.mailboxContents + delivered + deliveredGifts)
        self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NewItems)
        self.b_setBothSchedules(remaining, remainingGifts)
        return Task.done

    def setGiftSchedule(self, onGiftOrder, doUpdateLater = True):
        self.setBothSchedules(None, onGiftOrder)
        return
        self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air') and hasattr(self, 'name'):
            taskName = self.uniqueName('next-gift')
            taskMgr.remove(taskName)
            now = int(time.time() / 60 + 0.5)
            nextItem = None
            nextTime = self.onGiftOrder.getNextDeliveryDate()
            nextItem = self.onGiftOrder.getNextDeliveryItem()
            if nextItem != None:
                pass
            if nextTime != None:
                duration = max(10.0, nextTime * 60 - time.time())
                duration += 30
                taskMgr.doMethodLater(duration, self.__deliverGiftPurchase, taskName)
        return

    def getGiftSchedule(self):
        return self.onGiftOrder.getBlob(store=CatalogItem.Customization | CatalogItem.DeliveryDate)

    def __deliverGiftPurchase(self, task):
        now = int(time.time() / 60 + 0.5)
        delivered, remaining = self.onGiftOrder.extractDeliveryItems(now)
        self.notify.info('Gift Delivery for %s: %s.' % (self.doId, delivered))
        self.b_setMailboxContents(self.mailboxContents + delivered)
        simbase.air.deliveryManager.sendDeliverGifts(self.getDoId(), now)
        self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NewItems)
        return Task.done

    def __deliverPurchase(self, task):
        now = int(time.time() / 60 + 0.5)
        delivered, remaining = self.onOrder.extractDeliveryItems(now)
        self.notify.info('Delivery for %s: %s.' % (self.doId, delivered))
        self.b_setMailboxContents(self.mailboxContents + delivered)
        self.b_setDeliverySchedule(remaining)
        self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NewItems)
        return Task.done

    def b_setMailboxContents(self, mailboxContents):
        self.setMailboxContents(mailboxContents)
        self.d_setMailboxContents(mailboxContents)

    def d_setMailboxContents(self, mailboxContents):
        self.sendUpdate('setMailboxContents', [mailboxContents.getBlob(store=CatalogItem.Customization)])
        if len(mailboxContents) == 0:
            self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NoItems)
        self.checkMailboxFullIndicator()

    def checkMailboxFullIndicator(self):
        if self.houseId and hasattr(self, 'air'):
            if self.air:
                house = self.air.doId2do.get(self.houseId)
                if house and house.mailbox:
                    house.mailbox.b_setFullIndicator(len(self.mailboxContents) != 0 or self.numMailItems or self.getNumInvitesToShowInMailbox() or len(self.awardMailboxContents) != 0)

    def setMailboxContents(self, mailboxContents):
        self.notify.debug('Setting mailboxContents to %s.' % mailboxContents)
        self.mailboxContents = CatalogItemList.CatalogItemList(mailboxContents, store=CatalogItem.Customization)
        self.notify.debug('mailboxContents is %s.' % self.mailboxContents)

    def getMailboxContents(self):
        return self.mailboxContents.getBlob(store=CatalogItem.Customization)

    def b_setGhostMode(self, flag):
        self.setGhostMode(flag)
        self.d_setGhostMode(flag)

    def d_setGhostMode(self, flag):
        self.sendUpdate('setGhostMode', [flag])

    def setGhostMode(self, flag):
        self.ghostMode = flag

    def setImmortalMode(self, flag):
        self.immortalMode = flag

    def setUnlimitedGags(self, flag):
        self.unlimitedGags = flag

    def b_setSpeedChatStyleIndex(self, index):
        self.setSpeedChatStyleIndex(index)
        self.d_setSpeedChatStyleIndex(index)

    def d_setSpeedChatStyleIndex(self, index):
        self.sendUpdate('setSpeedChatStyleIndex', [index])

    def setSpeedChatStyleIndex(self, index):
        self.speedChatStyleIndex = index

    def getSpeedChatStyleIndex(self):
        return self.speedChatStyleIndex

    def b_setMaxMoney(self, maxMoney):
        self.d_setMaxMoney(maxMoney)
        self.setMaxMoney(maxMoney)
        if self.getMoney() > maxMoney:
            self.b_setBankMoney(self.bankMoney + (self.getMoney() - maxMoney))
            self.b_setMoney(maxMoney)

    def d_setMaxMoney(self, maxMoney):
        self.sendUpdate('setMaxMoney', [maxMoney])

    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    def addMoney(self, deltaMoney):
        money = deltaMoney + self.money
        pocketMoney = min(money, self.maxMoney)
        self.b_setMoney(pocketMoney)
        overflowMoney = money - self.maxMoney
        if overflowMoney > 0:
            bankMoney = self.bankMoney + overflowMoney
            self.b_setBankMoney(bankMoney)

    def takeMoney(self, deltaMoney, bUseBank = True):
        totalMoney = self.money
        if bUseBank:
            totalMoney += self.bankMoney
        if deltaMoney > totalMoney:
            self.notify.warning('Not enough money! AvId: %s Has:%s Charged:%s' % (self.doId, totalMoney, deltaMoney))
            return False
        if bUseBank and deltaMoney > self.money:
            self.b_setBankMoney(self.bankMoney - (deltaMoney - self.money))
            self.b_setMoney(0)
        else:
            self.b_setMoney(self.money - deltaMoney)
        return True

    def b_setMoney(self, money):
        if bboard.get('autoRich-%s' % self.doId, False):
            money = self.getMaxMoney()
        self.setMoney(money)
        self.d_setMoney(money)

    def d_setMoney(self, money):
        self.sendUpdate('setMoney', [money])

    def setMoney(self, money):
        if money < 0:
            simbase.air.writeServerEvent('suspicious', avId=self.doId, issue='toon has invalid money %s, forcing to zero' % money)
            money = 0
            commentStr = 'User %s has negative money %s' % (self.doId, money)
            dislId = self.DISLid
            if simbase.config.GetBool('want-ban-negative-money', False):
                #simbase.air.banManager.ban(self.doId, dislId, commentStr)
                pass
        self.money = money

    def getMoney(self):
        return self.money

    def getTotalMoney(self):
        return self.money + self.bankMoney

    def b_setMaxBankMoney(self, maxMoney):
        self.d_setMaxBankMoney(maxMoney)
        self.setMaxBankMoney(maxMoney)

    def d_setMaxBankMoney(self, maxMoney):
        self.sendUpdate('setMaxBankMoney', [maxMoney])

    def setMaxBankMoney(self, maxMoney):
        self.maxBankMoney = maxMoney

    def getMaxBankMoney(self):
        return self.maxBankMoney

    def b_setBankMoney(self, money):
        bankMoney = min(money, self.maxBankMoney)
        self.setBankMoney(bankMoney)
        self.d_setBankMoney(bankMoney)

    def d_setBankMoney(self, money):
        self.sendUpdate('setBankMoney', [money])

    def setBankMoney(self, money):
        self.bankMoney = money

    def getBankMoney(self):
        return self.bankMoney

    def b_setEmblems(self, emblems):
        self.setEmblems(emblems)
        self.d_setEmblems(emblems)

    def setEmblems(self, emblems):
        self.emblems = emblems

    def d_setEmblems(self, emblems):
        if simbase.air.wantEmblems:
            self.sendUpdate('setEmblems', [emblems])

    def getEmblems(self):
        return self.emblems

    def addEmblems(self, emblemsToAdd):
        newEmblems = self.emblems[:]
        for i in xrange(ToontownGlobals.NumEmblemTypes):
            newEmblems[i] += emblemsToAdd[i]

        self.b_setEmblems(newEmblems)

    def subtractEmblems(self, emblemsToSubtract):
        newEmblems = self.emblems[:]
        for i in xrange(ToontownGlobals.NumEmblemTypes):
            newEmblems[i] -= emblemsToSubtract[i]

        self.b_setEmblems(newEmblems)

    def isEnoughEmblemsToBuy(self, itemEmblemPrices):
        for emblemIndex, emblemPrice in enumerate(itemEmblemPrices):
            if emblemIndex >= len(self.emblems):
                return False
            if self.emblems[emblemIndex] < emblemPrice:
                return False

        return True

    def tossPie(self, x, y, z, h, p, r, sequence, power, timestamp32):
        if not self.validate(self.doId, self.numPies > 0, 'tossPie with no pies available'):
            return
        if self.numPies != ToontownGlobals.FullPies:
            self.b_setNumPies(self.numPies - 1)

    def b_setNumPies(self, numPies):
        self.setNumPies(numPies)
        self.d_setNumPies(numPies)

    def d_setNumPies(self, numPies):
        self.sendUpdate('setNumPies', [numPies])

    def setNumPies(self, numPies):
        self.numPies = numPies

    def b_setPieType(self, pieType):
        self.setPieType(pieType)
        self.d_setPieType(pieType)

    def d_setPieType(self, pieType):
        self.sendUpdate('setPieType', [pieType])

    def setPieType(self, pieType):
        self.pieType = pieType

    def b_setPieThrowType(self, pieThrowType):
        self.setPieThrowType(pieThrowType)
        self.d_setPieThrowType(pieThrowType)

    def d_setPieThrowType(self, pieThrowType):
        self.sendUpdate('setPieThrowType', [pieThrowType])

    def setPieThrowType(self, pieThrowType):
        self.pieThrowType = pieThrowType

    def b_setHealthDisplay(self, mode):
        self.setHealthDisplay(mode)
        self.d_setHealthDisplay(mode)

    def d_setHealthDisplay(self, mode):
        self.sendUpdate('setHealthDisplay', [mode])

    def setHealthDisplay(self, mode):
        pass

    def d_setTrophyScore(self, score):
        self.sendUpdate('setTrophyScore', [score])

    def stopToonUp(self):
        taskMgr.remove(self.uniqueName('safeZoneToonUp'))
        self.ignore(self.air.getAvatarExitEvent(self.getDoId()))

    def shouldToonUp(self, zoneId):
        if zoneId == OTPGlobals.QuietZone:
            return None
        if ToontownGlobals.safeZoneCountMap.has_key(ZoneUtil.getBranchZone(zoneId)):
            return True
        else:
            zoneOwner = self.air.zoneId2owner.get(zoneId)
            if not zoneOwner:
                return False
            else:
                from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
                from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI
                from DistributedNPCPartyPersonAI import DistributedNPCPartyPersonAI
                if isinstance(zoneOwner, (DistributedRacePadAI, DistributedGolfKartAI, DistributedNPCPartyPersonAI)):
                    return True
                elif zoneOwner in [self.air.estateManager, 'MinigameCreatorAI']:
                    return True
                elif config.GetBool('want-parties'):
                    if zoneOwner in [self.air.partyManager]:
                        return True
                else:
                    return False
        # Incase for whatever reason we even get to this stage...
        return False

    def considerToonUp(self, zoneId):
        if zoneId == OTPGlobals.QuietZone:
            # Don't consider anything, we're in the QuietZone. Shh!
            return
        if self.shouldToonUp(zoneId):
            if taskMgr.hasTaskNamed(self.uniqueName('safeZoneToonUp')):
                # Do nothing, we were already in a safezone!
                return
            self.startToonUp(ToontownGlobals.SafezoneToonupFrequency)
        else:
            self.stopToonUp()

    def startToonUp(self, healFrequency):
        self.stopToonUp()
        self.healFrequency = healFrequency
        self.__waitForNextToonUp()

    def __waitForNextToonUp(self):
        taskMgr.doMethodLater(self.healFrequency, self.toonUpTask, self.uniqueName('safeZoneToonUp'))

    def toonUpTask(self, task):
        self.toonUp(1)
        self.__waitForNextToonUp()
        return Task.done

    def toonUp(self, hpGained, quietly = 0, sendTotal = 1):
        if hpGained > self.maxHp:
            hpGained = self.maxHp
        if not quietly:
            self.sendUpdate('toonUp', [hpGained])
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = max(self.hp, 0) + hpGained
        clampedHp = min(self.hp, self.maxHp)
        if not self.hpOwnedByBattle:
            self.hp = clampedHp
        if sendTotal and not self.hpOwnedByBattle:
            self.d_setHp(clampedHp)

    def isToonedUp(self):
        return self.hp >= self.maxHp

    def makeBlackCat(self):
        if self.dna.getAnimal() != 'cat':
            return 'not a cat'
        self.air.writeServerEvent('blackCat', avId=self.doId)
        newDna = ToonDNA.ToonDNA()
        newDna.makeFromNetString(self.dna.makeNetString())
        black = 26
        newDna.updateToonProperties(armColor=black, legColor=black, headColor=black)
        self.b_setDNAString(newDna.makeNetString())
        return None

    def b_announceBingo(self):
        self.d_announceBingo()
        self.announceBingo

    def d_announceBingo(self):
        self.sendUpdate('announceBingo', [])

    def announceBingo(self):
        pass

    def incrementPopulation(self):
        if self.isPlayerControlled():
            DistributedPlayerAI.DistributedPlayerAI.incrementPopulation(self)

    def decrementPopulation(self):
        if self.isPlayerControlled():
            DistributedPlayerAI.DistributedPlayerAI.decrementPopulation(self)

    if __dev__:

        def _logGarbage(self):
            if self.isPlayerControlled():
                DistributedPlayerAI.DistributedPlayerAI._logGarbage(self)

    def reqSCResistance(self, msgIndex, nearbyPlayers):
        self.d_setSCResistance(msgIndex, nearbyPlayers)

    def d_setSCResistance(self, msgIndex, nearbyPlayers):
        if not ResistanceChat.validateId(msgIndex):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='said resistance %s, which is invalid.' % msgIndex)
            return
        if not self.removeResistanceMessage(msgIndex):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='said resistance %s, but does not have it.' % msgIndex)
            return
        if hasattr(self, 'autoResistanceRestock') and self.autoResistanceRestock:
            self.restockAllResistanceMessages(1)
        affectedPlayers = []
        for toonId in nearbyPlayers:
            toon = self.air.doId2do.get(toonId)
            if not toon:
                self.notify.warning('%s said resistance %s for %s; not on server' % (self.doId, msgIndex, toonId))
            elif toon.__class__ != DistributedToonAI:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='said resistance %s for %s; object of type %s' % (msgIndex, toonId, toon.__class__.__name__))
            elif toonId in affectedPlayers:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='said resistance %s for %s twice in same message.' % (msgIndex, toonId))
            else:
                toon.doResistanceEffect(msgIndex)
                affectedPlayers.append(toonId)

        if len(affectedPlayers) > 50:
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='said resistance %s for %s toons.' % (msgIndex, len(affectedPlayers)))
            self.notify.warning('%s said resistance %s for %s toons: %s' % (self.doId,
             msgIndex,
             len(affectedPlayers),
             affectedPlayers))
        self.sendUpdate('setSCResistance', [msgIndex, affectedPlayers])
        chattype = ResistanceChat.getMenuName(msgIndex)
        value = ResistanceChat.getItemValue(msgIndex)
        self.air.writeServerEvent('resistanceChat', zoneId=self.zoneId, avId=self.doId, chatType=chattype, value=value, affectedPlayers=affectedPlayers)

    def doResistanceEffect(self, msgIndex):
        msgType, itemIndex = ResistanceChat.decodeId(msgIndex)
        msgValue = ResistanceChat.getItemValue(msgIndex)
        if msgType == ResistanceChat.RESISTANCE_TOONUP:
            if msgValue == -1:
                self.toonUp(self.maxHp)
            else:
                self.toonUp(msgValue)
            self.notify.debug('Toon-up for ' + self.name)
        elif msgType == ResistanceChat.RESISTANCE_RESTOCK:
            self.inventory.NPCMaxOutInv(msgValue)
            self.d_setInventory(self.inventory.makeNetString())
            self.notify.debug('Restock for ' + self.name)
        elif msgType == ResistanceChat.RESISTANCE_MONEY:
            if msgValue == -1:
                self.addMoney(999999)
            else:
                self.addMoney(msgValue)
            self.notify.debug('Money for ' + self.name)

    def squish(self, damage):
        self.takeDamage(damage)

    if simbase.wantKarts:

        def hasKart(self):
            return self.kartDNA[KartDNA.bodyType] != -1

        def b_setTickets(self, numTickets):
            if numTickets > RaceGlobals.MaxTickets:
                numTickets = RaceGlobals.MaxTickets
            self.d_setTickets(numTickets)
            self.setTickets(numTickets)

        def d_setTickets(self, numTickets):
            if numTickets > RaceGlobals.MaxTickets:
                numTickets = RaceGlobals.MaxTickets
            self.sendUpdate('setTickets', [numTickets])

        def setTickets(self, numTickets):
            if numTickets > RaceGlobals.MaxTickets:
                numTickets = RaceGlobals.MaxTickets
            self.tickets = numTickets

        def getTickets(self):
            return self.tickets

        def b_setKartingTrophies(self, trophyList):
            self.setKartingTrophies(trophyList)
            self.d_setKartingTrophies(trophyList)

        def setKartingTrophies(self, trophyList):
            self.notify.debug('setting kartingTrophies to %s' % trophyList)
            self.kartingTrophies = trophyList

        def d_setKartingTrophies(self, trophyList):
            self.sendUpdate('setKartingTrophies', [trophyList])

        def getKartingTrophies(self):
            return self.kartingTrophies

        def b_setKartingHistory(self, history):
            self.setKartingHistory(history)
            self.d_setKartingHistory(history)

        def setKartingHistory(self, history):
            self.notify.debug('setting kartingHistory to %s' % history)
            self.kartingHistory = history

        def d_setKartingHistory(self, history):
            self.sendUpdate('setKartingHistory', [history])

        def getKartingHistory(self):
            return self.kartingHistory

        def b_setKartingPersonalBest(self, bestTimes):
            best1 = bestTimes[0:6]
            best2 = bestTimes[6:]
            self.setKartingPersonalBest(best1)
            self.setKartingPersonalBest2(best2)
            self.d_setKartingPersonalBest(bestTimes)

        def d_setKartingPersonalBest(self, bestTimes):
            best1 = bestTimes[0:6]
            best2 = bestTimes[6:]
            self.sendUpdate('setKartingPersonalBest', [best1])
            self.sendUpdate('setKartingPersonalBest2', [best2])

        def setKartingPersonalBest(self, bestTimes):
            self.notify.debug('setting karting to %s' % bestTimes)
            self.kartingPersonalBest = bestTimes

        def setKartingPersonalBest2(self, bestTimes2):
            self.notify.debug('setting karting2 to %s' % bestTimes2)
            self.kartingPersonalBest2 = bestTimes2

        def getKartingPersonalBest(self):
            return self.kartingPersonalBest

        def getKartingPersonalBest2(self):
            return self.kartingPersonalBest2

        def getKartingPersonalBestAll(self):
            return self.kartingPersonalBest + self.kartingPersonalBest2

        def setKartDNA(self, kartDNA):
            self.b_setKartBodyType(kartDNA[KartDNA.bodyType])
            self.b_setKartBodyColor(kartDNA[KartDNA.bodyColor])
            self.b_setKartAccColor(kartDNA[KartDNA.accColor])
            self.b_setKartEngineBlockType(kartDNA[KartDNA.ebType])
            self.b_setKartSpoilerType(kartDNA[KartDNA.spType])
            self.b_setKartFrontWheelWellType(kartDNA[KartDNA.fwwType])
            self.b_setKartBackWheelWellType(kartDNA[KartDNA.bwwType])
            self.b_setKartRimType(kartDNA[KartDNA.rimsType])
            self.b_setKartDecalType(kartDNA[KartDNA.decalType])

        def b_setKartBodyType(self, bodyType):
            self.d_setKartBodyType(bodyType)
            self.setKartBodyType(bodyType)

        def d_setKartBodyType(self, bodyType):
            self.sendUpdate('setKartBodyType', [bodyType])

        def setKartBodyType(self, bodyType):
            self.kartDNA[KartDNA.bodyType] = bodyType

        def getKartBodyType(self):
            return self.kartDNA[KartDNA.bodyType]

        def b_setKartBodyColor(self, bodyColor):
            self.d_setKartBodyColor(bodyColor)
            self.setKartBodyColor(bodyColor)

        def d_setKartBodyColor(self, bodyColor):
            self.sendUpdate('setKartBodyColor', [bodyColor])

        def setKartBodyColor(self, bodyColor):
            self.kartDNA[KartDNA.bodyColor] = bodyColor

        def getKartBodyColor(self):
            return self.kartDNA[KartDNA.bodyColor]

        def b_setKartAccessoryColor(self, accColor):
            self.d_setKartAccessoryColor(accColor)
            self.setKartAccessoryColor(accColor)

        def d_setKartAccessoryColor(self, accColor):
            self.sendUpdate('setKartAccessoryColor', [accColor])

        def setKartAccessoryColor(self, accColor):
            self.kartDNA[KartDNA.accColor] = accColor

        def getKartAccessoryColor(self):
            return self.kartDNA[KartDNA.accColor]

        def b_setKartEngineBlockType(self, ebType):
            self.d_setKartEngineBlockType(ebType)
            self.setKartEngineBlockType(ebType)

        def d_setKartEngineBlockType(self, ebType):
            self.sendUpdate('setKartEngineBlockType', [ebType])

        def setKartEngineBlockType(self, ebType):
            self.kartDNA[KartDNA.ebType] = ebType

        def getKartEngineBlockType(self):
            return self.kartDNA[KartDNA.ebType]

        def b_setKartSpoilerType(self, spType):
            self.d_setKartSpoilerType(spType)
            self.setKartSpoilerType(spType)

        def d_setKartSpoilerType(self, spType):
            self.sendUpdate('setKartSpoilerType', [spType])

        def setKartSpoilerType(self, spType):
            self.kartDNA[KartDNA.spType] = spType

        def getKartSpoilerType(self):
            return self.kartDNA[KartDNA.spType]

        def b_setKartFrontWheelWellType(self, fwwType):
            self.d_setKartFrontWheelWellType(fwwType)
            self.setKartFrontWheelWellType(fwwType)

        def d_setKartFrontWheelWellType(self, fwwType):
            self.sendUpdate('setKartFrontWheelWellType', [fwwType])

        def setKartFrontWheelWellType(self, fwwType):
            self.kartDNA[KartDNA.fwwType] = fwwType

        def getKartFrontWheelWellType(self):
            return self.kartDNA[KartDNA.fwwType]

        def b_setKartBackWheelWellType(self, bwwType):
            self.d_setKartBackWheelWellType(bwwType)
            self.setKartBackWheelWellType(bwwType)

        def d_setKartBackWheelWellType(self, bwwType):
            self.sendUpdate('setKartBackWheelWellType', [bwwType])

        def setKartBackWheelWellType(self, bwwType):
            self.kartDNA[KartDNA.bwwType] = bwwType

        def getKartBackWheelWellType(self):
            return self.kartDNA[KartDNA.bwwType]

        def b_setKartRimType(self, rimsType):
            self.d_setKartRimType(rimsType)
            self.setKartRimType(rimsType)

        def d_setKartRimType(self, rimsType):
            self.sendUpdate('setKartRimType', [rimsType])

        def setKartRimType(self, rimsType):
            self.kartDNA[KartDNA.rimsType] = rimsType

        def getKartRimType(self):
            return self.kartDNA[KartDNA.rimsType]

        def b_setKartDecalType(self, decalType):
            self.d_setKartDecalType(decalType)
            self.setKartDecalType(decalType)

        def d_setKartDecalType(self, decalType):
            self.sendUpdate('setKartDecalType', [decalType])

        def setKartDecalType(self, decalType):
            self.kartDNA[KartDNA.decalType] = decalType

        def getKartDecalType(self):
            return self.kartDNA[KartDNA.decalType]

        def b_setKartAccessoriesOwned(self, accessories):
            self.d_setKartAccessoriesOwned(accessories)
            self.setKartAccessoriesOwned(accessories)

        def d_setKartAccessoriesOwned(self, accessories):
            self.sendUpdate('setKartAccessoriesOwned', [accessories])

        def setKartAccessoriesOwned(self, accessories):
            if (__debug__):
                import pdb
            self.accessories = accessories

        def getKartAccessoriesOwned(self):
            owned = copy.deepcopy(self.accessories)
            while InvalidEntry in owned:
                owned.remove(InvalidEntry)

            return owned

        def addOwnedAccessory(self, accessoryId):
            print 'in add owned accessory'
            if AccessoryDict.has_key(accessoryId):
                if self.accessories.count(accessoryId) > 0:
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to add accessory %s which is already owned!' % accessoryId)
                    return
                if self.accessories.count(InvalidEntry) > 0:
                    accList = list(self.accessories)
                    index = self.accessories.index(InvalidEntry)
                    accList[index] = accessoryId
                    self.b_setKartAccessoriesOwned(accList)
                else:
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to add accessory %s when accessory inventory is full!' % accessoryId)
                    return
            else:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to add accessory %s which is not a valid accessory.' % accessoryId)
                return

        def removeOwnedAccessory(self, accessoryId):
            if AccessoryDict.has_key(accessoryId):
                if self.accessories.count(accessoryId) == 0:
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to remove accessory %s which is not currently owned!' % accessoryId)
                    return
                else:
                    accList = list(self.accessories)
                    index = self.accessories.index(accessoryId)
                    accList[index] = InvalidEntry
                    self.air.writeServerEvent('deletedKartingAccessory', avId=self.doId, accessoryId='%s' % accessoryId)
                    self.b_setKartAccessoriesOwned(accList)
            else:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to remove accessory %s which is not a valid accessory.' % accessoryId)
                return

        def updateKartDNAField(self, dnaField, fieldValue):
            if not checkKartFieldValidity(dnaField):
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update to dna value  %s in the invalid field %s' % (fieldValue, dnaField))
                return
            if dnaField == KartDNA.bodyType:
                if fieldValue not in KartDict.keys() and fieldValue != InvalidEntry:
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update kart body to invalid body %s.' % fieldValue)
                    return
                self.b_setKartBodyType(fieldValue)
            else:
                accFields = [KartDNA.ebType,
                 KartDNA.spType,
                 KartDNA.fwwType,
                 KartDNA.bwwType,
                 KartDNA.rimsType,
                 KartDNA.decalType]
                colorFields = [KartDNA.bodyColor, KartDNA.accColor]
                if dnaField in accFields:
                    if fieldValue == InvalidEntry:
                        self.__updateKartDNAField(dnaField, fieldValue)
                    else:
                        if fieldValue not in self.accessories:
                            self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update to accessory %s which is not currently owned.' % fieldValue)
                            return
                        field = getAccessoryType(fieldValue)
                        if field == InvalidEntry:
                            self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update accessory %s in an illegal field %s' % (fieldValue, field))
                            return
                        elif field != dnaField:
                            self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update accessory %s in a field %s that does not match client specified field %s' % (fieldValue, field, dnaField))
                            return
                        self.__updateKartDNAField(dnaField, fieldValue)
                elif dnaField in colorFields:
                    if fieldValue == InvalidEntry:
                        self.__updateKartDNAField(dnaField, fieldValue)
                    else:
                        if fieldValue not in self.accessories:
                            if fieldValue != getDefaultColor():
                                self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update to color %s which is not owned!' % fieldValue)
                                return
                            elif fieldValue == getDefaultColor() and self.kartDNA[dnaField] != InvalidEntry:
                                self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update to default color %s which is not owned!' % fieldValue)
                                return
                        if getAccessoryType(fieldValue) != KartDNA.bodyColor:
                            self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to update invalid color %s for dna field %s' % (fieldValue, dnaField))
                            return
                        self.__updateKartDNAField(dnaField, fieldValue)
                else:
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue='attempt to udpate accessory %s in the invalid field %s' % (fieldValue, dnaField))
                    return

        def __updateKartDNAField(self, dnaField, fieldValue):
            if dnaField == KartDNA.bodyColor:
                self.b_setKartBodyColor(fieldValue)
            elif dnaField == KartDNA.accColor:
                self.b_setKartAccessoryColor(fieldValue)
            elif dnaField == KartDNA.ebType:
                self.b_setKartEngineBlockType(fieldValue)
            elif dnaField == KartDNA.spType:
                self.b_setKartSpoilerType(fieldValue)
            elif dnaField == KartDNA.fwwType:
                self.b_setKartFrontWheelWellType(fieldValue)
            elif dnaField == KartDNA.bwwType:
                self.b_setKartBackWheelWellType(fieldValue)
            elif dnaField == KartDNA.rimsType:
                self.b_setKartRimType(fieldValue)
            elif dnaField == KartDNA.decalType:
                self.b_setKartDecalType(fieldValue)

        def setAllowSoloRace(self, allowSoloRace):
            self.allowSoloRace = allowSoloRace

        def setAllowRaceTimeout(self, allowRaceTimeout):
            self.allowRaceTimeout = allowRaceTimeout

    if simbase.wantPets:

        def getPetId(self):
            return self.petId

        def b_setPetId(self, petId):
            self.d_setPetId(petId)
            self.setPetId(petId)

        def d_setPetId(self, petId):
            self.sendUpdate('setPetId', [petId])

        def setPetId(self, petId):
            self.petId = petId

        def getPetTrickPhrases(self):
            return self.petTrickPhrases

        def b_setPetTrickPhrases(self, tricks):
            self.setPetTrickPhrases(tricks)
            self.d_setPetTrickPhrases(tricks)

        def d_setPetTrickPhrases(self, tricks):
            self.sendUpdate('setPetTrickPhrases', [tricks])

        def setPetTrickPhrases(self, tricks):
            self.petTrickPhrases = tricks

        def deletePet(self):
            if self.petId == 0:
                self.notify.warning("this toon doesn't have a pet to delete!")
                return
            simbase.air.petMgr.deleteToonsPet(self.doId)

        def setPetMovie(self, petId, flag):
            self.notify.debug('setPetMovie: petId: %s, flag: %s' % (petId, flag))
            pet = simbase.air.doId2do.get(petId)
            if pet is not None:
                if pet.__class__.__name__ == 'DistributedPetAI':
                    pet.handleAvPetInteraction(flag, self.getDoId())
                else:
                    self.air.writeServerEvent('suspicious', avId=self.doId, issue='setPetMovie: playing pet movie %s on non-pet object %s' % (flag, petId))
            return

        def setPetTutorialDone(self, bDone):
            self.notify.debug('setPetTutorialDone')
            self.bPetTutorialDone = True

        def setFishBingoTutorialDone(self, bDone):
            self.notify.debug('setFishBingoTutorialDone')
            self.bFishBingoTutorialDone = True

        def setFishBingoMarkTutorialDone(self, bDone):
            self.notify.debug('setFishBingoMarkTutorialDone')
            self.bFishBingoMarkTutorialDone = True

        def enterEstate(self, ownerId, zoneId):
            DistributedToonAI.notify.debug('enterEstate: %s %s %s' % (self.doId, ownerId, zoneId))
            if self.wasInEstate():
                self.cleanupEstateData()
            collSphere = CollisionSphere(0, 0, 0, self.getRadius())
            collNode = CollisionNode('toonColl-%s' % self.doId)
            collNode.addSolid(collSphere)
            collNode.setFromCollideMask(BitMask32.allOff())
            collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
            self.collNodePath = self.attachNewNode(collNode)
            taskMgr.add(self._moveSphere, self._getMoveSphereTaskName(), priority=OTPGlobals.AICollMovePriority)
            self.inEstate = 1
            self.estateOwnerId = ownerId
            self.estateZones = simbase.air.estateMgr.getEstateZones(ownerId)
            self.estateHouseZones = simbase.air.estateMgr.getEstateHouseZones(ownerId)
            self.enterPetLook()

        def _getPetLookerBodyNode(self):
            return self.collNodePath

        def _getMoveSphereTaskName(self):
            return 'moveSphere-%s' % self.doId

        def _moveSphere(self, task):
            self.collNodePath.setZ(self.getRender(), 0)
            return Task.cont

        def isInEstate(self):
            return hasattr(self, 'inEstate') and self.inEstate

        def exitEstate(self, ownerId = None, zoneId = None):
            DistributedToonAI.notify.debug('exitEstate: %s %s %s' % (self.doId, ownerId, zoneId))
            DistributedToonAI.notify.debug('current zone: %s' % self.zoneId)
            self.exitPetLook()
            taskMgr.remove(self._getMoveSphereTaskName())
            self.collNodePath.removeNode()
            del self.collNodePath
            del self.estateOwnerId
            del self.estateHouseZones
            del self.inEstate
            self._wasInEstate = 1

        def wasInEstate(self):
            return hasattr(self, '_wasInEstate') and self._wasInEstate

        def cleanupEstateData(self):
            del self.estateZones
            del self._wasInEstate

        def setSC(self, msgId):
            DistributedToonAI.notify.debug('setSC: %s' % msgId)
            from toontown.pets import PetObserve
            PetObserve.send(self.zoneId, PetObserve.getSCObserve(msgId, self.doId))
            if msgId in [21006]:
                self.setHatePets(1)
            elif msgId in [21000,
             21001,
             21003,
             21004,
             21200,
             21201,
             21202,
             21203,
             21204,
             21205,
             21206]:
                self.setHatePets(0)

        def setSCCustom(self, msgId):
            DistributedToonAI.notify.debug('setSCCustom: %s' % msgId)
            from toontown.pets import PetObserve
            PetObserve.send(self.zoneId, PetObserve.getSCObserve(msgId, self.doId))

    def setHatePets(self, hate):
        self.hatePets = hate

    def takeOutKart(self, zoneId = None):
        if not self.kart:
            from toontown.racing import DistributedVehicleAI
            self.kart = DistributedVehicleAI.DistributedVehicleAI(self.air, self.doId)
            if zoneId:
                self.kart.generateWithRequired(zoneId)
            else:
                self.kart.generateWithRequired(self.zoneId)
            self.kart.start()

    def reqCogSummons(self, type, suitIndex):
        if type not in ('single', 'building', 'invasion'):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='invalid cog summons type: %s' % type)
            self.sendUpdate('cogSummonsResponse', ['fail', suitIndex, 0])
            return
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='invalid suitIndex: %s' % suitIndex)
            self.sendUpdate('cogSummonsResponse', ['fail', suitIndex, 0])
            return
        if not self.hasCogSummons(suitIndex, type):
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='bogus cog summons')
            self.sendUpdate('cogSummonsResponse', ['fail', suitIndex, 0])
            return
        if ZoneUtil.isWelcomeValley(self.zoneId):
            self.sendUpdate('cogSummonsResponse', ['fail', suitIndex, 0])
            return
        returnCode = None
        if type == 'single':
            returnCode = self.doSummonSingleCog(suitIndex)
        elif type == 'building':
            returnCode = self.doBuildingTakeover(suitIndex)
        elif type == 'invasion':
            returnCode = self.doCogInvasion(suitIndex)
        if returnCode:
            if returnCode[0] == 'success':
                self.air.writeServerEvent('cogSummoned', avId=self.doId, cogType=type, suitIndex=suitIndex, zoneId=self.zoneId)
                self.removeCogSummonsEarned(suitIndex, type)
            self.sendUpdate('cogSummonsResponse', returnCode)
        return

    def doSummonSingleCog(self, suitIndex):
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.notify.warning('Bad suit index: %s' % suitIndex)
            return ['badIndex', suitIndex, 0]
        suitName = SuitDNA.suitHeadTypes[suitIndex]
        streetId = ZoneUtil.getBranchZone(self.zoneId)
        if not self.air.suitPlanners.has_key(streetId):
            return ['badlocation', suitIndex, 0]
        sp = self.air.suitPlanners[streetId]
        map = sp.getZoneIdToPointMap()
        zones = [self.zoneId, self.zoneId - 1, self.zoneId + 1]
        for zoneId in zones:
            if map.has_key(zoneId):
                points = map[zoneId][:]
                suit = sp.createNewSuit([], points, suitName=suitName)
                if suit:
                    return ['success', suitIndex, 0]
        return ['badlocation', suitIndex, 0]

    def doBuildingTakeover(self, suitIndex):
        streetId = ZoneUtil.getBranchZone(self.zoneId)
        if not self.air.suitPlanners.has_key(streetId):
            self.notify.warning('Street %d is not known.' % streetId)
            return ['badlocation', suitIndex, 0]
        sp = self.air.suitPlanners[streetId]
        bm = sp.buildingMgr
        building = self.findClosestDoor()
        if building == None:
            return ['badlocation', suitIndex, 0]
        level = None
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.notify.warning('Bad suit index: %s' % suitIndex)
            return ['badIndex', suitIndex, 0]
        suitName = SuitDNA.suitHeadTypes[suitIndex]
        track = SuitDNA.getSuitDept(suitName)
        type = SuitDNA.getSuitType(suitName)
        level, type, track = sp.pickLevelTypeAndTrack(None, type, track)
        building.suitTakeOver(track, level, None)
        self.notify.warning('cogTakeOver %s %s %d %d' % (track,
         level,
         building.block,
         self.zoneId))
        return ['success', suitIndex, building.doId]

    def doCogInvasion(self, suitIndex):
        invMgr = self.air.suitInvasionManager
        if invMgr.getInvading():
            returnCode = 'busy'
        else:
            if suitIndex >= len(SuitDNA.suitHeadTypes):
                self.notify.warning('Bad suit index: %s' % suitIndex)
                return ['badIndex', suitIndex, 0]
            cogType = SuitDNA.suitHeadTypes[suitIndex]
            numCogs = 1000
            if invMgr.startInvasion(cogType, numCogs, False):
                returnCode = 'success'
            else:
                returnCode = 'fail'
        return [returnCode, suitIndex, 0]

    def b_setCogSummonsEarned(self, cogSummonsEarned):
        self.d_setCogSummonsEarned(cogSummonsEarned)
        self.setCogSummonsEarned(cogSummonsEarned)

    def d_setCogSummonsEarned(self, cogSummonsEarned):
        self.sendUpdate('setCogSummonsEarned', [cogSummonsEarned])

    def setCogSummonsEarned(self, cogSummonsEarned):
        self.cogSummonsEarned = cogSummonsEarned

    def getCogSummonsEarned(self):
        return self.cogSummonsEarned

    def restockAllCogSummons(self):
        numSuits = len(SuitDNA.suitHeadTypes)
        fullSetForSuit = 1 | 2 | 4
        allSummons = numSuits * [fullSetForSuit]
        self.b_setCogSummonsEarned(allSummons)

    def addCogSummonsEarned(self, suitIndex, type):
        summons = self.getCogSummonsEarned()
        curSetting = summons[suitIndex]
        if type == 'single':
            curSetting |= 1
        elif type == 'building':
            curSetting |= 2
        elif type == 'invasion':
            curSetting |= 4
        summons[suitIndex] = curSetting
        self.b_setCogSummonsEarned(summons)

    def removeCogSummonsEarned(self, suitIndex, type):
        summons = self.getCogSummonsEarned()
        curSetting = summons[suitIndex]
        if self.hasCogSummons(suitIndex, type):
            if type == 'single':
                curSetting &= -2
            elif type == 'building':
                curSetting &= -3
            elif type == 'invasion':
                curSetting &= -5
            summons[suitIndex] = curSetting
            self.b_setCogSummonsEarned(summons)
            if hasattr(self, 'autoRestockSummons') and self.autoRestockSummons:
                self.restockAllCogSummons()
            return True
        self.notify.warning("Toon %s doesn't have a %s summons for %s" % (self.doId, type, suitIndex))
        return False

    def hasCogSummons(self, suitIndex, type = None):
        summons = self.getCogSummonsEarned()
        curSetting = summons[suitIndex]
        if type == 'single':
            return curSetting & 1
        elif type == 'building':
            return curSetting & 2
        elif type == 'invasion':
            return curSetting & 4
        return curSetting

    def hasParticularCogSummons(self, deptIndex, level, type):
        if deptIndex not in range(len(SuitDNA.suitDepts)):
            self.notify.warning('invalid parameter deptIndex %s' % deptIndex)
            return False
        if level not in range(SuitDNA.suitsPerDept):
            self.notify.warning('invalid parameter level %s' % level)
            return False
        suitIndex = deptIndex * SuitDNA.suitsPerDept + level
        retval = self.hasCogSummons(suitIndex, type)
        return retval

    def assignNewCogSummons(self, level = None, summonType = None, deptIndex = None):
        if level != None:
            if deptIndex in range(len(SuitDNA.suitDepts)):
                dept = deptIndex
            else:
                numDepts = len(SuitDNA.suitDepts)
                dept = random.randrange(0, numDepts)
            suitIndex = dept * SuitDNA.suitsPerDept + level
        elif deptIndex in range(len(SuitDNA.suitDepts)):
            randomLevel = random.randrange(0, SuitDNA.suitsPerDept)
            suitIndex = deptIndex * SuitDNA.suitsPerLevel + randomLevel
        else:
            numSuits = len(SuitDNA.suitHeadTypes)
            suitIndex = random.randrange(0, numSuits)
        if summonType in ['single', 'building', 'invasion']:
            type = summonType
        else:
            typeWeights = ['single'] * 70 + ['building'] * 25 + ['invasion'] * 5
            type = random.choice(typeWeights)
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.notify.warning('Bad suit index: %s' % suitIndex)
        self.addCogSummonsEarned(suitIndex, type)
        return (suitIndex, type)

    def findClosestDoor(self):
        zoneId = self.zoneId
        streetId = ZoneUtil.getBranchZone(zoneId)
        sp = self.air.suitPlanners[streetId]
        if not sp:
            return None
        bm = sp.buildingMgr
        if not bm:
            return None
        zones = [zoneId,
         zoneId - 1,
         zoneId + 1,
         zoneId - 2,
         zoneId + 2]
        for zone in zones:
            for i in bm.getToonBlocks():
                building = bm.getBuilding(i)
                extZoneId, intZoneId = building.getExteriorAndInteriorZoneId()
                if not NPCToons.isZoneProtected(intZoneId):
                    if hasattr(building, 'door'):
                        if building.door.zoneId == zone:
                            return building

        return None

    def b_setGardenTrophies(self, trophyList):
        self.setGardenTrophies(trophyList)
        self.d_setGardenTrophies(trophyList)

    def setGardenTrophies(self, trophyList):
        self.notify.debug('setting gardenTrophies to %s' % trophyList)
        self.gardenTrophies = trophyList

    def d_setGardenTrophies(self, trophyList):
        self.sendUpdate('setGardenTrophies', [trophyList])

    def getGardenTrophies(self):
        return self.gardenTrophies

    def setGardenSpecials(self, specials):
        for special in specials:
            if special[1] > 255:
                special[1] = 255

        self.gardenSpecials = specials

    def getGardenSpecials(self):
        return self.gardenSpecials

    def d_setGardenSpecials(self, specials):
        self.sendUpdate('setGardenSpecials', [specials])

    def b_setGardenSpecials(self, specials):
        for special in specials:
            if special[1] > 255:
                newCount = 255
                index = special[0]
                self.gardenSpecials.remove(special)
                self.gardenSpecials.append((index, newCount))
                self.gardenSpecials.sort()

        self.setGardenSpecials(specials)
        self.d_setGardenSpecials(specials)

    def addGardenItem(self, index, count):
        for item in self.gardenSpecials:
            if item[0] == index:
                newCount = item[1] + count
                self.gardenSpecials.remove(item)
                self.gardenSpecials.append((index, newCount))
                self.gardenSpecials.sort()
                self.b_setGardenSpecials(self.gardenSpecials)
                return

        self.gardenSpecials.append((index, count))
        self.gardenSpecials.sort()
        self.b_setGardenSpecials(self.gardenSpecials)

    def removeGardenItem(self, index, count):
        for item in self.gardenSpecials:
            if item[0] == index:
                newCount = item[1] - count
                self.gardenSpecials.remove(item)
                if newCount > 0:
                    self.gardenSpecials.append((index, newCount))
                self.gardenSpecials.sort()
                self.b_setGardenSpecials(self.gardenSpecials)
                return

        self.notify.warning("removing garden item %d that toon doesn't have" % index)

    def b_setFlowerCollection(self, speciesList, varietyList):
        self.setFlowerCollection(speciesList, varietyList)
        self.d_setFlowerCollection(speciesList, varietyList)

    def d_setFlowerCollection(self, speciesList, varietyList):
        self.sendUpdate('setFlowerCollection', [speciesList, varietyList])

    def setFlowerCollection(self, speciesList, varietyList):
        self.flowerCollection = FlowerCollection.FlowerCollection()
        self.flowerCollection.makeFromNetLists(speciesList, varietyList)

    def getFlowerCollection(self):
        return self.flowerCollection.getNetLists()

    def b_setMaxFlowerBasket(self, maxFlowerBasket):
        self.d_setMaxFlowerBasket(maxFlowerBasket)
        self.setMaxFlowerBasket(maxFlowerBasket)

    def d_setMaxFlowerBasket(self, maxFlowerBasket):
        self.sendUpdate('setMaxFlowerBasket', [maxFlowerBasket])

    def setMaxFlowerBasket(self, maxFlowerBasket):
        self.maxFlowerBasket = maxFlowerBasket

    def getMaxFlowerBasket(self):
        return self.maxFlowerBasket

    def b_setFlowerBasket(self, speciesList, varietyList):
        self.setFlowerBasket(speciesList, varietyList)
        self.d_setFlowerBasket(speciesList, varietyList)

    def d_setFlowerBasket(self, speciesList, varietyList):
        self.sendUpdate('setFlowerBasket', [speciesList, varietyList])

    def setFlowerBasket(self, speciesList, varietyList):
        self.flowerBasket = FlowerBasket.FlowerBasket()
        self.flowerBasket.makeFromNetLists(speciesList, varietyList)

    def getFlowerBasket(self):
        return self.flowerBasket.getNetLists()

    def makeRandomFlowerBasket(self):
        self.flowerBasket.generateRandomBasket()
        self.d_setFlowerBasket(*self.flowerBasket.getNetLists())

    def addFlowerToBasket(self, species, variety):
        numFlower = len(self.flowerBasket)
        if numFlower >= self.maxFlowerBasket:
            self.notify.warning('addFlowerToBasket: cannot add flower, basket is full')
            return 0
        elif self.flowerBasket.addFlower(species, variety):
            self.d_setFlowerBasket(*self.flowerBasket.getNetLists())
            return 1
        else:
            self.notify.warning('addFlowerToBasket: addFlower failed')
            return 0

    def removeFlowerFromBasketAtIndex(self, index):
        if self.flowerBasket.removeFlowerAtIndex(index):
            self.d_setFlowerBasket(*self.flowerBasket.getNetLists())
            return 1
        else:
            self.notify.warning('removeFishFromTank: cannot find fish')
            return 0

    def b_setShovel(self, shovelId):
        self.d_setShovel(shovelId)
        self.setShovel(shovelId)

    def d_setShovel(self, shovelId):
        self.sendUpdate('setShovel', [shovelId])

    def setShovel(self, shovelId):
        self.shovel = shovelId

    def getShovel(self):
        return self.shovel

    def b_setShovelSkill(self, skillLevel):
        self.sendGardenEvent()
        if skillLevel >= GardenGlobals.ShovelAttributes[self.shovel]['skillPts']:
            if self.shovel < GardenGlobals.MAX_SHOVELS - 1:
                self.b_setShovel(self.shovel + 1)
                self.setShovelSkill(0)
                self.d_setShovelSkill(0)
                self.sendUpdate('promoteShovel', [self.shovel])
                self.air.writeServerEvent('garden_new_shovel', avId=self.doId, shovel='%d' % self.shovel)
        else:
            self.setShovelSkill(skillLevel)
            self.d_setShovelSkill(skillLevel)

    def d_setShovelSkill(self, skillLevel):
        self.sendUpdate('setShovelSkill', [skillLevel])

    def setShovelSkill(self, skillLevel):
        self.shovelSkill = skillLevel

    def getShovelSkill(self):
        return self.shovelSkill

    def b_setWateringCan(self, wateringCanId):
        self.d_setWateringCan(wateringCanId)
        self.setWateringCan(wateringCanId)

    def d_setWateringCan(self, wateringCanId):
        self.sendUpdate('setWateringCan', [wateringCanId])

    def setWateringCan(self, wateringCanId):
        self.wateringCan = wateringCanId

    def getWateringCan(self):
        return self.wateringCan

    def b_setWateringCanSkill(self, skillLevel):
        self.sendGardenEvent()
        if skillLevel >= GardenGlobals.WateringCanAttributes[self.wateringCan]['skillPts']:
            if self.wateringCan < GardenGlobals.MAX_WATERING_CANS - 1:
                self.b_setWateringCan(self.wateringCan + 1)
                self.setWateringCanSkill(0)
                self.d_setWateringCanSkill(0)
                self.sendUpdate('promoteWateringCan', [self.wateringCan])
                self.air.writeServerEvent('garden_new_wateringCan', avId=self.doId, can='%d' % self.wateringCan)
            else:
                skillLevel = GardenGlobals.WateringCanAttributes[self.wateringCan]['skillPts'] - 1
                self.setWateringCanSkill(skillLevel)
                self.d_setWateringCanSkill(skillLevel)
        else:
            self.setWateringCanSkill(skillLevel)
            self.d_setWateringCanSkill(skillLevel)

    def d_setWateringCanSkill(self, skillLevel):
        self.sendUpdate('setWateringCanSkill', [skillLevel])

    def setWateringCanSkill(self, skillLevel):
        self.wateringCanSkill = skillLevel

    def getWateringCanSkill(self):
        return self.wateringCanSkill

    def b_setTrackBonusLevel(self, trackBonusLevelArray):
        self.setTrackBonusLevel(trackBonusLevelArray)
        self.d_setTrackBonusLevel(trackBonusLevelArray)

    def d_setTrackBonusLevel(self, trackBonusLevelArray):
        self.sendUpdate('setTrackBonusLevel', [trackBonusLevelArray])

    def setTrackBonusLevel(self, trackBonusLevelArray):
        self.trackBonusLevel = trackBonusLevelArray

    def getTrackBonusLevel(self, track = None):
        if track == None:
            return self.trackBonusLevel
        else:
            return self.trackBonusLevel[track]
        return

    def checkGagBonus(self, track, level):
        trackBonus = self.getTrackBonusLevel(track)
        return trackBonus >= level

    def giveMeSpecials(self, id = None):
        print 'Specials Go!!'
        self.b_setGardenSpecials([(0, 3),
         (1, 2),
         (2, 3),
         (3, 2),
         (4, 3),
         (5, 2),
         (6, 3),
         (7, 2),
         (100, 1),
         (101, 3),
         (102, 1)])

    def reqUseSpecial(self, special):
        response = self.tryToUseSpecial(special)
        self.sendUpdate('useSpecialResponse', [response])

    def tryToUseSpecial(self, special):
        estateOwnerDoId = simbase.air.estateMgr.zone2owner.get(self.zoneId)
        response = 'badlocation'
        doIHaveThisSpecial = False
        for curSpecial in self.gardenSpecials:
            if curSpecial[0] == special and curSpecial[1] > 0:
                doIHaveThisSpecial = True
                break

        if not doIHaveThisSpecial:
            return response
        if not self.doId == estateOwnerDoId:
            self.notify.warning("how did this happen, planting an item you don't own")
            return response
        if estateOwnerDoId:
            estate = simbase.air.estateMgr.estate.get(estateOwnerDoId)
            if estate and hasattr(estate, 'avIdList'):
                ownerIndex = estate.avIdList.index(estateOwnerDoId)
                if ownerIndex >= 0:
                    estate.doEpochNow(onlyForThisToonIndex=ownerIndex)
                    self.removeGardenItem(special, 1)
                    response = 'success'
                    self.air.writeServerEvent('garden_fertilizer', avId=self.doId)
        return response

    def sendGardenEvent(self):
        if hasattr(self, 'estateZones') and hasattr(self, 'doId'):
            if simbase.wantPets and self.hatePets:
                PetObserve.send(self.estateZones, PetObserve.PetActionObserve(PetObserve.Actions.GARDEN, self.doId))

    def setGardenStarted(self, bStarted):
        self.gardenStarted = bStarted

    def d_setGardenStarted(self, bStarted):
        self.sendUpdate('setGardenStarted', [bStarted])

    def b_setGardenStarted(self, bStarted):
        self.setGardenStarted(bStarted)
        self.d_setGardenStarted(bStarted)

    def getGardenStarted(self):
        return self.gardenStarted

    def logSuspiciousEvent(self, eventName):
        senderId = self.air.getAvatarIdFromSender()
        eventStr = 'senderId=%s ' % senderId
        eventStr += eventName
        strSearch = re.compile('AvatarHackWarning! nodename')
        if strSearch.search(eventName, 0, 100):
            self.air.district.recordSuspiciousEventData(len(eventStr))
        self.air.writeServerEvent('suspicious', avId=self.doId, issue=eventStr)
        if simbase.config.GetBool('want-ban-setSCSinging', True):
            if 'invalid msgIndex in setSCSinging:' in eventName:
                if senderId == self.doId:
                    commentStr = 'Toon %s trying to call setSCSinging' % self.doId
                    #simbase.air.banManager.ban(self.doId, self.DISLid, commentStr)
                else:
                    self.notify.warning('logSuspiciousEvent event=%s senderId=%s != self.doId=%s' % (eventName, senderId, self.doId))
        if simbase.config.GetBool('want-ban-setAnimState', True):
            if eventName.startswith('setAnimState: '):
                if senderId == self.doId:
                    commentStr = 'Toon %s trying to call setAnimState' % self.doId
                    #simbase.air.banManager.ban(self.doId, self.DISLid, commentStr)
                else:
                    self.notify.warning('logSuspiciousEvent event=%s senderId=%s != self.doId=%s' % (eventName, senderId, self.doId))

    def getGolfTrophies(self):
        return self.golfTrophies

    def getGolfCups(self):
        return self.golfCups

    def b_setGolfHistory(self, history):
        self.setGolfHistory(history)
        self.d_setGolfHistory(history)

    def d_setGolfHistory(self, history):
        self.sendUpdate('setGolfHistory', [history])

    def setGolfHistory(self, history):
        self.notify.debug('setting golfHistory to %s' % history)
        self.golfHistory = history
        self.golfTrophies = GolfGlobals.calcTrophyListFromHistory(self.golfHistory)
        self.golfCups = GolfGlobals.calcCupListFromHistory(self.golfHistory)

    def getGolfHistory(self):
        return self.golfHistory

    def b_setGolfHoleBest(self, holeBest):
        self.setGolfHoleBest(holeBest)
        self.d_setGolfHoleBest(holeBest)

    def d_setGolfHoleBest(self, holeBest):
        packed = GolfGlobals.packGolfHoleBest(holeBest)
        self.sendUpdate('setPackedGolfHoleBest', [packed])

    def setGolfHoleBest(self, holeBest):
        self.golfHoleBest = holeBest

    def getGolfHoleBest(self):
        return self.golfHoleBest

    def getPackedGolfHoleBest(self):
        packed = GolfGlobals.packGolfHoleBest(self.golfHoleBest)
        return packed

    def setPackedGolfHoleBest(self, packedHoleBest):
        unpacked = GolfGlobals.unpackGolfHoleBest(packedHoleBest)
        self.setGolfHoleBest(unpacked)

    def b_setGolfCourseBest(self, courseBest):
        self.setGolfCourseBest(courseBest)
        self.d_setGolfCourseBest(courseBest)

    def d_setGolfCourseBest(self, courseBest):
        self.sendUpdate('setGolfCourseBest', [courseBest])

    def setGolfCourseBest(self, courseBest):
        self.golfCourseBest = courseBest

    def getGolfCourseBest(self):
        return self.golfCourseBest

    def setUnlimitedSwing(self, unlimitedSwing):
        self.unlimitedSwing = unlimitedSwing

    def getUnlimitedSwing(self):
        return self.unlimitedSwing

    def b_setUnlimitedSwing(self, unlimitedSwing):
        self.setUnlimitedSwing(unlimitedSwing)
        self.d_setUnlimitedSwing(unlimitedSwing)

    def d_setUnlimitedSwing(self, unlimitedSwing):
        self.sendUpdate('setUnlimitedSwing', [unlimitedSwing])

    def b_setPinkSlips(self, pinkSlips):
        self.d_setPinkSlips(pinkSlips)
        self.setPinkSlips(pinkSlips)

    def d_setPinkSlips(self, pinkSlips):
        self.sendUpdate('setPinkSlips', [pinkSlips])

    def setPinkSlips(self, pinkSlips):
        self.pinkSlips = pinkSlips

    def getPinkSlips(self):
        return self.pinkSlips

    def addPinkSlips(self, amountToAdd):
        pinkSlips = min(self.pinkSlips + amountToAdd, 255)
        self.b_setPinkSlips(pinkSlips)

    def removePinkSlips(self, amount):
        if hasattr(self, 'autoRestockPinkSlips') and self.autoRestockPinkSlips:
            amount = 0
        pinkSlips = max(self.pinkSlips - amount, 0)
        self.b_setPinkSlips(pinkSlips)

    def setPreviousAccess(self, access):
        self.previousAccess = access

    def b_setAccess(self, access):
        self.setAccess(access)
        self.d_setAccess(access)

    def d_setAccess(self, access):
        self.sendUpdate('setAccess', [access])

    def setAccess(self, access):
        paidStatus = simbase.config.GetString('force-paid-status', 'none')
        if paidStatus == 'unpaid':
            access = 1
        print 'Setting Access %s' % access
        if access == OTPGlobals.AccessInvalid:
            if not __dev__:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='setAccess not being sent by the OTP Server, changing access to unpaid')
                access = OTPGlobals.AccessVelvetRope
            elif __dev__:
                access = OTPGlobals.AccessFull
        self.setGameAccess(access)

    def setGameAccess(self, access):
        self.gameAccess = access

    def getGameAccess(self):
        return self.gameAccess

    def b_setNametagStyle(self, nametagStyle):
        self.d_setNametagStyle(nametagStyle)
        self.setNametagStyle(nametagStyle)

    def d_setNametagStyle(self, nametagStyle):
        self.sendUpdate('setNametagStyle', [nametagStyle])

    def setNametagStyle(self, nametagStyle):
        self.nametagStyle = nametagStyle

    def getNametagStyle(self):
        return self.nametagStyle

    def logMessage(self, message):
        avId = self.air.getAvatarIdFromSender()
        if __dev__:
            print 'CLIENT LOG MESSAGE %s %s' % (avId, message)
        try:
            self.air.writeServerEvent('client-log', avId=avId, message=message)
        except:
            self.air.writeServerEvent('suspicious', avId=avId, issue='client sent us a clientLog that caused an exception')

    def b_setMail(self, mail):
        self.d_setMail(mail)
        self.setMail(mail)

    def d_setMail(self, mail):
        self.sendUpdate('setMail', [mail])

    def setMail(self, mail):
        self.mail = mail

    def setNumMailItems(self, numMailItems):
        self.numMailItems = numMailItems

    def setSimpleMailNotify(self, simpleMailNotify):
        self.simpleMailNotify = simpleMailNotify

    def setInviteMailNotify(self, inviteMailNotify):
        self.inviteMailNotify = inviteMailNotify

    def setInvites(self, invites):
        self.invites = []
        for i in xrange(len(invites)):
            oneInvite = invites[i]
            newInvite = InviteInfoBase(*oneInvite)
            self.invites.append(newInvite)

    def updateInviteMailNotify(self):
        invitesInMailbox = self.getInvitesToShowInMailbox()
        newInvites = 0
        readButNotRepliedInvites = 0
        for invite in invitesInMailbox:
            if invite.status == PartyGlobals.InviteStatus.NotRead:
                newInvites += 1
            elif invite.status == PartyGlobals.InviteStatus.ReadButNotReplied:
                readButNotRepliedInvites += 1
            if __dev__:
                partyInfo = self.getOnePartyInvitedTo(invite.partyId)
                if not partyInfo:
                    self.notify.error('party info not found in partiesInvtedTo, partyId = %s' % str(invite.partyId))

        if newInvites:
            self.setInviteMailNotify(ToontownGlobals.NewItems)
        elif readButNotRepliedInvites:
            self.setInviteMailNotify(ToontownGlobals.OldItems)
        else:
            self.setInviteMailNotify(ToontownGlobals.NoItems)

    def getNumNonResponseInvites(self):
        count = 0
        for i in xrange(len(self.invites)):
            if self.invites[i].status == InviteStatus.NotRead or self.invites[i].status == InviteStatus.ReadButNotReplied:
                count += 1

        return count

    def getInvitesToShowInMailbox(self):
        result = []
        for invite in self.invites:
            appendInvite = True
            if invite.status == InviteStatus.Accepted or invite.status == InviteStatus.Rejected:
                appendInvite = False
            if appendInvite:
                partyInfo = self.getOnePartyInvitedTo(invite.partyId)
                if not partyInfo:
                    appendInvite = False
                if appendInvite:
                    if partyInfo.status == PartyGlobals.PartyStatus.Cancelled:
                        appendInvite = False
                if appendInvite:
                    endDate = partyInfo.endTime.date()
                    curDate = simbase.air.toontownTimeManager.getCurServerDateTime().date()
                    if endDate < curDate:
                        appendInvite = False
            if appendInvite:
                result.append(invite)

        return result

    def getNumInvitesToShowInMailbox(self):
        result = len(self.getInvitesToShowInMailbox())
        return result

    def setHostedParties(self, hostedParties):
        self.hostedParties = []
        for i in xrange(len(hostedParties)):
            hostedInfo = hostedParties[i]
            newParty = PartyInfoAI(*hostedInfo)
            self.hostedParties.append(newParty)

    def setPartiesInvitedTo(self, partiesInvitedTo):
        self.partiesInvitedTo = []
        for i in xrange(len(partiesInvitedTo)):
            partyInfo = partiesInvitedTo[i]
            newParty = PartyInfoAI(*partyInfo)
            self.partiesInvitedTo.append(newParty)

        self.updateInviteMailNotify()
        self.checkMailboxFullIndicator()

    def getOnePartyInvitedTo(self, partyId):
        result = None
        for i in xrange(len(self.partiesInvitedTo)):
            partyInfo = self.partiesInvitedTo[i]
            if partyInfo.partyId == partyId:
                result = partyInfo
                break

        return result

    def setPartyReplyInfoBases(self, replies):
        self.partyReplyInfoBases = []
        for i in xrange(len(replies)):
            partyReply = replies[i]
            repliesForOneParty = PartyReplyInfoBase(*partyReply)
            self.partyReplyInfoBases.append(repliesForOneParty)

    def updateInvite(self, inviteKey, newStatus):
        for invite in self.invites:
            if invite.inviteKey == inviteKey:
                invite.status = newStatus
                self.updateInviteMailNotify()
                self.checkMailboxFullIndicator()
                break

    def updateReply(self, partyId, inviteeId, newStatus):
        for partyReply in self.partyReplyInfoBases:
            if partyReply.partyId == partyId:
                for reply in partyReply.replies:
                    if reply.inviteeId == inviteeId:
                        reply.inviteeId = newStatus
                        break

    def canPlanParty(self):
        nonCancelledPartiesInTheFuture = 0
        for partyInfo in self.hostedParties:
            if partyInfo.status not in (PartyGlobals.PartyStatus.Cancelled, PartyGlobals.PartyStatus.Finished, PartyGlobals.PartyStatus.NeverStarted):
                nonCancelledPartiesInTheFuture += 1
                if nonCancelledPartiesInTheFuture >= PartyGlobals.MaxHostedPartiesPerToon:
                    break

        result = nonCancelledPartiesInTheFuture < PartyGlobals.MaxHostedPartiesPerToon
        return result

    def setPartyCanStart(self, partyId):
        self.notify.debug('setPartyCanStart called passing in partyId=%s' % partyId)
        found = False
        for partyInfo in self.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = PartyGlobals.PartyStatus.CanStart
                found = True
                break

        if not found:
            self.notify.warning("setPartyCanStart can't find partyId %s" % partyId)

    def setPartyStatus(self, partyId, newStatus):
        self.notify.debug('setPartyStatus  called passing in partyId=%s newStauts=%d' % (partyId, newStatus))
        found = False
        for partyInfo in self.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = newStatus
                found = True
                break

        info = self.getOnePartyInvitedTo(partyId)
        if info:
            found = True
            info.status = newStatus
        if not found:
            self.notify.warning("setPartyCanStart can't find hosted or invitedTO partyId %s" % partyId)

    def b_setAwardMailboxContents(self, awardMailboxContents):
        self.setAwardMailboxContents(awardMailboxContents)
        self.d_setAwardMailboxContents(awardMailboxContents)

    def d_setAwardMailboxContents(self, awardMailboxContents):
        self.sendUpdate('setAwardMailboxContents', [awardMailboxContents.getBlob(store=CatalogItem.Customization)])

    def setAwardMailboxContents(self, awardMailboxContents):
        self.notify.debug('Setting awardMailboxContents to %s.' % awardMailboxContents)
        self.awardMailboxContents = CatalogItemList.CatalogItemList(awardMailboxContents, store=CatalogItem.Customization)
        self.notify.debug('awardMailboxContents is %s.' % self.awardMailboxContents)
        if len(awardMailboxContents) == 0:
            self.b_setAwardNotify(ToontownGlobals.NoItems)
        self.checkMailboxFullIndicator()

    def getAwardMailboxContents(self):
        return self.awardMailboxContents.getBlob(store=CatalogItem.Customization)

    def b_setAwardSchedule(self, onOrder, doUpdateLater = True):
        self.setAwardSchedule(onOrder, doUpdateLater)
        self.d_setAwardSchedule(onOrder)

    def d_setAwardSchedule(self, onOrder):
        self.sendUpdate('setAwardSchedule', [onOrder.getBlob(store=CatalogItem.Customization | CatalogItem.DeliveryDate)])

    def setAwardSchedule(self, onAwardOrder, doUpdateLater = True):
        self.onAwardOrder = CatalogItemList.CatalogItemList(onAwardOrder, store=CatalogItem.Customization | CatalogItem.DeliveryDate)
        if hasattr(self, 'name'):
            if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air'):
                taskName = self.uniqueName('next-award-delivery')
                taskMgr.remove(taskName)
                now = int(time.time() / 60 + 0.5)
                nextItem = None
                nextTime = self.onAwardOrder.getNextDeliveryDate()
                nextItem = self.onAwardOrder.getNextDeliveryItem()
                if nextItem != None:
                    pass
                if nextTime != None:
                    duration = max(10.0, nextTime * 60 - time.time())
                    taskMgr.doMethodLater(duration, self.__deliverAwardPurchase, taskName)
        return

    def __deliverAwardPurchase(self, task):
        now = int(time.time() / 60 + 0.5)
        delivered, remaining = self.onAwardOrder.extractDeliveryItems(now)
        self.notify.info('Award Delivery for %s: %s.' % (self.doId, delivered))
        self.b_setAwardMailboxContents(self.awardMailboxContents + delivered)
        self.b_setAwardSchedule(remaining)
        if delivered:
            self.b_setAwardNotify(ToontownGlobals.NewItems)
        return Task.done

    def b_setAwardNotify(self, awardMailboxNotify):
        self.setAwardNotify(awardMailboxNotify)
        self.d_setAwardNotify(awardMailboxNotify)

    def d_setAwardNotify(self, awardMailboxNotify):
        self.sendUpdate('setAwardNotify', [awardMailboxNotify])

    def setAwardNotify(self, awardNotify):
        self.awardNotify = awardNotify

    def b_setGM(self, type):
        self.sendUpdate('setGM', [type])
        self.setGM(type)

    def setGM(self, type):
        wasGM = self._isGM
        formerType = self._gmType
        self._isGM = type != 0
        self._gmType = None
        if self._isGM:
            self._gmType = type - 1
            MaxGMType = len(TTLocalizer.GM_NAMES) - 1
            if self._gmType > MaxGMType:
                self.notify.warning('toon %s has invalid GM type: %s' % (self.doId, self._gmType))
                self._gmType = MaxGMType
        #self._updateGMName(formerType)
        return

    def isGM(self):
        return self._isGM

    def _nameIsPrefixed(self, prefix):
        if len(self.name) > len(prefix):
            if self.name[:len(prefix)] == prefix:
                return True
        return False

    def _updateGMName(self, formerType = None):
        if formerType is None:
            formerType = self._gmType
        name = self.name
        if formerType is not None:
            gmPrefix = TTLocalizer.GM_NAMES[formerType] + ' '
            if self._nameIsPrefixed(gmPrefix):
                name = self.name[len(gmPrefix):]
        if self._isGM:
            gmPrefix = TTLocalizer.GM_NAMES[self._gmType] + ' '
            newName = gmPrefix + name
        else:
            newName = name
        if self.name != newName:
            self.b_setName(newName)
        return

    def setName(self, name):
        DistributedPlayerAI.DistributedPlayerAI.setName(self, name)
        if self.WantOldGMNameBan:
            if self.isGenerated():
                self._checkOldGMName()
        #self._updateGMName()

    def _checkOldGMName(self):
        if '$' in set(self.name):
            if config.GetBool('want-ban-old-gm-name', 0):
                self.ban('invalid name: %s' % self.name)
            else:
                self.air.writeServerEvent('suspicious', avId=self.doId, issue='$ found in toon name')

    def setModuleInfo(self, info):
        avId = self.air.getAvatarIdFromSender()
        key = 'outrageous'
        self.moduleWhitelist = self.modulelist.loadWhitelistFile()
        self.moduleBlacklist = self.modulelist.loadBlacklistFile()
        for obfuscatedModule in info:
            module = ''
            p = 0
            for ch in obfuscatedModule:
                ic = ord(ch) ^ ord(key[p])
                p += 1
                if p >= len(key):
                    p = 0
                module += chr(ic)

            if module not in self.moduleWhitelist:
                if module in self.moduleBlacklist:
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Black List module %s loaded into process.' % module)
                    if simbase.config.GetBool('want-ban-blacklist-module', False):
                        commentStr = 'User has blacklist module: %s attached to their game process' % module
                        dislId = self.DISLid
                        #simbase.air.banManager.ban(self.doId, dislId, commentStr)
                else:
                    self.air.writeServerEvent('suspicious', avId=avId, issue='Unknown module %s loaded into process.' % module)

    def teleportResponseToAI(self, toAvId, available, shardId, hoodId, zoneId, fromAvId):
        if not self.WantTpTrack:
            return
        senderId = self.air.getAvatarIdFromSender()
        if toAvId != self.doId:
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='toAvId=%d is not equal to self.doId' % toAvId)
            return
        if available != 1:
            self.air.writeServerEvent('suspicious', avId=self.doId, issue='invalid availableValue=%d' % available)
            return
        if fromAvId == 0:
            return
        self.air.teleportRegistrar.registerValidTeleport(toAvId, available, shardId, hoodId, zoneId, fromAvId)
        dg = self.dclass.aiFormatUpdate('teleportResponse', fromAvId, fromAvId, self.doId, [toAvId,
         available,
         shardId,
         hoodId,
         zoneId])
        self.air.send(dg)

    @staticmethod
    def staticGetLogicalZoneChangeAllEvent():
        return 'DOLogicalChangeZone-all'

    def _garbageInfo(self):
        if hasattr(self, 'inventory'):
            if not hasattr(self.inventory, '_createStack'):
                return 'inventory has no create stack'
            else:
                return self.inventory._createStack
        return 'no inventory'

    def flagAv(self, avId, reason, params):
        self.notify.debug('reason: %s timepassed: %s' % (reason, globalClock.getFrameTime() - DistributedToonAI.lastFlagAvTime))
        if reason == AV_FLAG_REASON_TOUCH and globalClock.getFrameTime() - DistributedToonAI.lastFlagAvTime > AV_TOUCH_CHECK_DELAY_AI:
            DistributedToonAI.lastFlagAvTime = globalClock.getFrameTime()
            av = self.air.doId2do.get(avId)
            otherAv = self.air.doId2do.get(int(params[0]))
            self.notify.debug('checking suspicious avatar positioning %s for %s with %s' % (avId, reason, params))
            if av and otherAv and isinstance(av, DistributedToonAI) and isinstance(otherAv, DistributedToonAI) and av.zoneId == otherAv.zoneId and av.zoneId not in MinigameCreatorAI.MinigameZoneRefs:
                self.notify.debug('...in zone %s' % av.zoneId)
                componentNode = av.getParent().attachNewNode('blah')
                componentNode.setPos(av.getComponentX(), av.getComponentY(), av.getComponentZ())
                avPos = componentNode.getPos(av.getRender())
                componentNode.reparentTo(otherAv.getParent())
                componentNode.setPos(otherAv.getComponentX(), otherAv.getComponentY(), otherAv.getComponentZ())
                otherAvPos = componentNode.getPos(otherAv.getRender())
                componentNode.removeNode()
                zDist = avPos.getZ() - otherAvPos.getZ()
                avPos2D = copy.copy(avPos)
                avPos2D.setZ(0)
                otherAvPos2D = copy.copy(otherAvPos)
                otherAvPos2D.setZ(0)
                moveVec = avPos2D - otherAvPos2D
                dist = moveVec.length()
                self.notify.debug('2d dist between avs is %s %s %s' % (dist, avPos, otherAvPos))
                if dist < AV_TOUCH_CHECK_DIST and zDist < AV_TOUCH_CHECK_DIST_Z:
                    self.notify.debug('...moving!')
                    if dist == 0.0:
                        moveVec = Vec3(1.0, 0, 0)
                    else:
                        moveVec.normalize()
                    moveVec = moveVec * AV_TOUCH_CHECK_DIST
                    avHpr = av.getHpr(av.getRender())
                    newX = avPos.getX() + moveVec.getX()
                    newY = avPos.getY() + moveVec.getY()
                    newZ = avPos.getZ() + moveVec.getZ()
                    newH = avHpr.getX()
                    newP = avHpr.getY()
                    newR = avHpr.getZ()
                    av.setPosHpr(av.getRender(), newX, newY, newZ, newH, newP, newR)
                    newAvPos = av.getPos()
                    if newAvPos.getX() > 3000 or newAvPos.getX() < -3000 or newAvPos.getY() > 3000 or newAvPos.getY() < -3000:
                        return
                    av.d_setXY(newAvPos.getX(), newAvPos.getY())
                    self.notify.debug('setting ai pos: %s %s %s and sending pos: %s' % (newX,
                     newY,
                     newZ,
                     newAvPos))
                    if len(DistributedToonAI.flagCounts) > AV_FLAG_HISTORY_LEN:
                        DistributedToonAI.flagCounts = {}
                    avPairKey = str(min(av.doId, otherAv.doId)) + '+' + str(max(av.doId, otherAv.doId))
                    prevCount = DistributedToonAI.flagCounts.setdefault(avPairKey, [{}, globalClock.getFrameTime(), {}])
                    if not prevCount[2].has_key(av.doId):
                        prevCount[2][av.doId] = [None, None]
                    if not prevCount[0].has_key(av.doId):
                        prevCount[0][av.doId] = 0
                    self.notify.debug('moving av %s, newPos: %s oldPos: %s' % (av.doId, prevCount[2][av.doId], avPos))
                    if prevCount[2][av.doId][0] == None or prevCount[2][av.doId][1] == None:
                        pass
                    elif prevCount[2][av.doId][0] != avPos.getX() or prevCount[2][av.doId][1] != avPos.getY():
                        prevCount[0][av.doId] += 1
                    prevCount[2][av.doId] = [newX, newY]
                    if prevCount[0][av.doId] > AV_TOUCH_COUNT_LIMIT:
                        if globalClock.getFrameTime() - prevCount[1] < AV_TOUCH_COUNT_TIME:
                            zoneId = not hasattr(av, 'zoneId') and 'undef' or av.zoneId
                            battleId = not hasattr(av, 'battleId') and 'undef' or av.battleId
                            animName = not hasattr(av, 'animName') and 'undef' or av.animName
                            inEstate = not hasattr(av, 'isInEstate') and 'undef' or av.isInEstate()
                            ghostMode = not hasattr(av, 'ghostMode') and 'undef' or av.ghostMode
                            immortalMode = not hasattr(av, 'immortalMode') and 'undef' or av.immortalMode
                            isGm = not hasattr(av, '_isGM') and 'undef' or av._isGM
                            valStr = '%s %s %s %s %s %s %s %s' % (otherAv.doId,
                             zoneId,
                             battleId,
                             animName,
                             inEstate,
                             ghostMode,
                             immortalMode,
                             isGm)
                            self.notify.info('av %s is consistently in an inappropriate position with %s...' % (av.doId, valStr))
                            self.air.writeServerEvent('suspicious', avId=avId, issue=' consistently in an inappropriate position with toon %s' % valStr)
                            response = simbase.config.GetString('toon-pos-hack-response', 'nothing')
                            av.handleHacking(response, 'collision and position hacking', [otherAv])
                        del DistributedToonAI.flagCounts[avPairKey]
        return

    def handleHacking(self, response, comment, coconspirators = []):
        if response == 'quietzone':
            self.b_setLocation(self.parentId, ToontownGlobals.QuietZone)
        elif response == 'disconnect':
            self.disconnect()
        elif response == 'disconnectall':
            self.disconnect()
            for coconspirator in coconspirators:
                coconspirator.disconnect()

        elif response == 'ban':
            self.ban('collision and position hacking')
            self.disconnect()
        elif response == 'banall':
            self.ban('collision and position hacking')
            self.disconnect()
            for coconspirator in coconspirators:
                coconspirator.ban('collision and position hacking')
                coconspirator.disconnect()

    def setWantBetaKeyQuest(self, wantQuest):
        self.wantBetaKeyQuest = wantQuest

    def d_setWantBetaKeyQuest(self, wantQuest):
        self.sendUpdate('setWantBetaKeyQuest', [wantQuest])

    def b_setWantBetaKeyQuest(self, wantQuest):
        self.setWantBetaKeyQuest(wantQuest)
        self.d_setWantBetaKeyQuest(wantQuest)

    def getWantBetaKeyQuest(self):
        return self.wantBetaKeyQuest

    def magicFanfare(self):
        self.sendUpdate('magicFanfare', [])

    def magicTeleportResponse(self, requesterId, hoodId):
        toon = self.air.doId2do.get(requesterId)
        if toon:
            toon.magicTeleportInitiate(self.getDoId(), hoodId, self.getLocation()[1])

    def magicTeleportInitiate(self, targetId, hoodId, zoneId):
        if targetId not in self.magicWordTeleportRequests:
            return
        self.magicWordTeleportRequests.remove(targetId)
        self.sendUpdate('magicTeleportInitiate', [hoodId, zoneId])

    def setWebAccountId(self, webId):
        self.webAccountId = webId

    def getWebAccountId(self):
        return self.webAccountId

    def ping(self):
        self.notify.debug("Pinging %s (%d)." % (self.getName(), self.getDoId()))
        self.sendUpdate('ping', ["mooBseoGkcauQcM"])
        taskMgr.doMethodLater(config.GetInt('toon-ping-timeout-delay', 30), self.__noPong, self.uniqueName('PingTimeout'), extraArgs=[])

    def __noPong(self):
        # No response from the client. Assume this avatar is a ghost.
        self.notify.debug("Ping timeout %s (%d)." % (self.getName(), self.getDoId()))
        self.__failedPing = True
        self.requestDelete()

    def pong(self, data):
        if hasattr(self, "__failedPing") and self.__failedPing:
            # Too late to respond, we already failed to respond on time.
            self.notify.debug("Pong after timeout %s (%d)." % (self.getName(), self.getDoId()))
            return
        if data != "McQuackGoesBoom":
            self.air.writeServerEvent("suspicious", avId=self.getDoId(), issue="Avatar failed to respond to ping with correct data.")
            self.requestDelete()
            return
        self.notify.debug("Pong received from %s (%d) successfully." % (self.getName(), self.getDoId()))
        taskMgr.remove(self.uniqueName('PingTimeout'))
        taskMgr.doMethodLater(config.GetInt('toon-ping-cooldown', 120), self.ping, self.uniqueName('PingCooldown'), extraArgs=[])

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int, int])
def setCE(CEValue, CEHood=0, CEExpire=0):
    """Set Cheesy Effect of the target."""
    CEHood = CEHood * 1000 #So the invoker only has to use '1' for DonaldsDock, '2' for TTC etc.
    if not 0 <= CEValue <= 18:
        return 'Invalid value %s specified for Cheesy Effect.' % CEValue
    if CEHood != 0 and not 100 < CEHood < ToontownGlobals.DynamicZonesBegin:
        return 'Invalid zoneId specified.'
    spellbook.getTarget().b_setCheesyEffect(CEValue, CEHood, time.time()+CEExpire)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int], targetClasses=[DistributedToonAI], aliases=['hp', 'toonHp', 'currHp'])
def setHp(hpVal):
    """Set target's current laff"""
    if not -1 <= hpVal <= 137:
        return 'Laff must be between -1 and 137!'
    spellbook.getTarget().b_setHp(hpVal)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def setMaxHp(hpVal):
    """Set target's laff"""
    if not 15 <= hpVal <= 137:
        return 'Laff must be between 15 and 137!'
    spellbook.getTarget().b_setMaxHp(hpVal)
    spellbook.getTarget().toonUp(hpVal)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int, int, int, int, int, int])
def setTrackAccess(toonup, trap, lure, sound, throw, squirt, drop):
    """Set target's gag track access."""
    spellbook.getTarget().b_setTrackAccess([toonup, trap, lure, sound, throw, squirt, drop])

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str])
def maxToon(hasConfirmed='UNCONFIRMED'):
    """Max out the toons stats, for end-level gameplay. Should only be (and is restricted to) casting on Administrators only."""
    toon = spellbook.getInvoker()

    if hasConfirmed != 'CONFIRM':
        return 'Are you sure you want to max out %s? This process is irreversible. Use "~maxToon CONFIRM" to confirm.' % toon.getName()

    # Max out gag tracks (all 7 tracks)
    toon.b_setTrackAccess([1] * 7)
    toon.b_setMaxCarry(MaxCarryLimit + 15) # Compensate for the extra gag track.
    toon.experience.maxOutExp() # Completely max out the toons experience.
    toon.b_setExperience(toon.experience.makeNetString())

    # Restock all gags.
    toon.inventory.zeroInv()
    toon.inventory.maxOutInv(filterUberGags=0, filterPaidGags=0)
    toon.b_setInventory(toon.inventory.makeNetString())

    # Max out laff
    toon.b_setMaxHp(ToontownGlobals.MaxHpLimit)
    toon.toonUp(toon.getMaxHp() - toon.getHp())

    # Max out cog suits (ORDER: Bossbot, Lawbot, Cashbot, Sellbot)
    toon.b_setCogParts([
        CogDisguiseGlobals.PartsPerSuitBitmasks[0], # Bossbot
        CogDisguiseGlobals.PartsPerSuitBitmasks[1], # Lawbot
        CogDisguiseGlobals.PartsPerSuitBitmasks[2], # Cashbot
        CogDisguiseGlobals.PartsPerSuitBitmasks[3]  # Sellbot
    ])
    toon.b_setCogLevels([ToontownGlobals.MaxCogSuitLevel] * 4)
    toon.b_setCogTypes([SuitDNA.suitsPerDept-1] * 4)

    # High racing tickets
    toon.b_setTickets(99999)

    # Teleport access everywhere (Including CogHQ, excluding Funny Farm.)
    toon.b_setHoodsVisited(ToontownGlobals.Hoods)
    toon.b_setTeleportAccess(ToontownGlobals.HoodsForTeleportAll)

    # General end game settings
    toon.b_setQuestCarryLimit(ToontownGlobals.MaxQuestCarryLimit)
    toon.b_setRewardHistory(Quests.ELDER_TIER, [])
    toon.b_setMaxMoney(250)
    toon.b_setMoney(toon.getMaxMoney())
    toon.b_setBankMoney(ToontownGlobals.DefaultMaxBankMoney)

    return 'By the power invested in me, I, McQuack, max your toon.'

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def setMaxMoney(moneyVal):
    """Set target's money and maxMoney values."""
    if not 40 <= moneyVal <= 250:
        return 'Money value must be between 40 and 250.'
    spellbook.getTarget().b_setMaxMoney(moneyVal)
    spellbook.getTarget().b_setMoney(moneyVal)
    return 'maxMoney set to %s' % moneyVal

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def setFishingRod(rodVal):
    """Set target's fishing rod value."""
    if not 0 <= rodVal <= 4:
        return 'Rod value must be between 0 and 4.'
    spellbook.getTarget().b_setFishingRod(rodVal)
    return 'Rod changed to ' + str(rodVal)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def setMaxFishTank(tankVal):
    """Set target's max fish tank value."""
    if not 20 <= tankVal <= 99:
        return 'Max fish tank value must be between 20 and 99'
    spellbook.getTarget().b_setMaxFishTank(tankVal)
    return 'Max size of fish tank changed to ' + str(tankVal)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str])
def setName(nameStr):
    """Set target's name."""
    spellbook.getTarget().b_setName(nameStr)
    return "Changed avId %s's name to %s" % (spellbook.getTarget().doId, nameStr)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int])
def setHat(hatId, hatTex=0):
    """Set hat of target toon."""
    if not 0 <= hatId <= 56:
        return 'Invalid hat specified.'
    if not 0 <= hatTex <= 20:
        return 'Invalid hat texture specified.'
    spellbook.getTarget().b_setHat(hatId, hatTex, 0)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int])
def setGlasses(glassesId, glassesTex=0):
    """Set glasses of target toon."""
    if not 0 <= glassesId <= 21:
        return 'Invalid glasses specified.'
    if not 0 <= glassesTex <= 4:
        return 'Invalid glasses texture specified.'
    spellbook.getTarget().b_setGlasses(glassesId, glassesTex, 0)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int])
def setBackpack(bpId, bpTex=0):
    """Set backpack of target toon."""
    if not 0 <= bpId <= 24:
        return 'Invalid backpack specified.'
    if not 0 <= bpTex <= 6:
        return 'Invalid backpack texture specified.'
    spellbook.getTarget().b_setBackpack(bpId, bpTex, 0)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int])
def setShoes(shoesId, shoesTex=0):
    """Set shoes of target toon."""
    if not 0 <= shoesId <= 3:
        return 'Invalid shoe type specified.'
    if not 0 <= shoesTex <= 48:
        return 'Invalid shoe specified.'
    spellbook.getTarget().b_setShoes(shoesId, shoesTex, 0)

@magicWord(category=CATEGORY_MODERATION, types=[str])
def kick(reason):
    """Kick the player from the game server."""
    if spellbook.getTarget() == spellbook.getInvoker():
        # Dumbass tried to kick themselves. Tut tut tut.
        return "You cannot kick yourself, %s!" % spellbook.getInvoker().getName()
    dg = PyDatagram()
    dg.addServerHeader(spellbook.getTarget().GetPuppetConnectionChannel(spellbook.getTarget().doId), simbase.air.ourChannel, CLIENTAGENT_EJECT)
    dg.addUint16(155)
    dg.addString(reason)
    simbase.air.send(dg)
    return "You kicked %s with reason '%s'." % (spellbook.getTarget().getName(), reason)

@magicWord(category=CATEGORY_MODERATION, types=[str, bool, bool], access=400) # Set to 400 for now...
def ban(reason="Unknown reason.", confirmed=False, overrideSelfBan=False):
    """Ban the player from the game server."""
    return 'banManager is not currently implemented!' # Disabled until we have a working banManager.
    if not confirmed:
        return "Are you sure you want to ban this player? Use '~~ban REASON True' if you are."
    if not overrideSelfBan and spellbook.getTarget() == spellbook.getInvoker():
        return "Are you sure you want to ban yourself? Use '~ban REASON True True' if you are."
    spellbook.getTarget().ban(reason)

#This command has been disabled due to many breakingnessings. GG developers, you suck at sanity >:C
'''
@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str, str])
def ut(doField, doData=None):
    """Update a toons field in the db."""

    methodExists = hasattr(spellbook.getTarget(), doField)
    b_methodExists = hasattr(spellbook.getTarget(), 'b_'+doField)
    access = spellbook.getInvokerAccess()
    if doData:
        #There are arguments to be passed, lets find out how many.
        theData = shlex.split(doData)
        for count in range(0, len(theData)):
            theData[count] = theData[count].split(',')
            for cur in range(0, len(theData[count])):
                try:
                    theData[count][cur] = int(theData[count][cur])
                except:
                    #Could not convert to integer, pass.
                    pass
            if len(theData[count])==1:
               theData[count] = theData[count][0]
        if len(theData)==1:
            singleData = theData[0] #Only has 1 parameter
            if b_methodExists:
                getattr(spellbook.getTarget(), 'b_'+doField)(singleData)
            elif methodExists:
                getattr(spellbook.getTarget(), doField)(singleData)
            #elif access==500: #To prevent unexperienced admins from breaking toons.
            else:
                spellbook.getTarget().sendUpdate(doField, [singleData])
            #else:
                #return "Unable to send to Astron. Access 500 required."
        else:
            if b_methodExists:
                getattr(spellbook.getTarget(), 'b_'+doField)(*theData)
            elif methodExists:
                getattr(spellbook.getTarget(), doField)(*theData)
            #elif access==500:
            else:
                spellbook.getTarget().sendUpdate(doField, theData)
            #else:
                #return "Unable to send to Astron. Access 500 required."
    else:
        #There are no arguments, we will simply call the function.
        if b_methodExists:
            getattr(spellbook.getTarget(), 'b_'+doField)()
        elif methodExists:
            getattr(spellbook.getTarget(), doField)()
        #elif access==500:
        else:
            spellbook.getTarget().sendUpdate(doField)
        #else:
            #return "Unable to send to Astron. Access 500 required."

    return "Method " + doField + " was called on " + spellbook.getTarget().name + " successfully."
'''

@magicWord(category=CATEGORY_MODERATION)
def togGM():
    """Toggle GM Icon for toon."""
    access = spellbook.getInvokerAccess()
    if spellbook.getInvoker().isGM():
        spellbook.getInvoker().b_setGM(0)
        return 'You have disabled your GM icon.'
    else:
        if access>=400:
            spellbook.getInvoker().b_setGM(2)
        elif access>=200:
            spellbook.getInvoker().b_setGM(3)
        return 'You have enabled your GM icon.'

@magicWord(category=CATEGORY_MODERATION)
def ghost():
    """Set toon to invisible."""
    if spellbook.getInvoker().ghostMode == 0:
        spellbook.getInvoker().b_setGhostMode(2)
        return 'Time to ninja!'
    else:
        spellbook.getInvoker().b_setGhostMode(0)

@magicWord(category=CATEGORY_MODERATION)
def badName():
    """Set target's name to the 'REJECTED' state and rename them to their <COLOR SPECIES> name."""
    oldname = spellbook.getTarget().name
    dna = spellbook.getTarget().dna
    colorstring = TTLocalizer.NumToColor[dna.headColor]
    animaltype = TTLocalizer.AnimalToSpecies[dna.getAnimal()]
    spellbook.getTarget().b_setName(colorstring + ' ' + animaltype)
    spellbook.getTarget().sendUpdate('WishNameState', 4) # 4 = WISHNAME_REJECTED
    return "Revoked %s's name successfully. They have been renamed to %s." % (oldname, spellbook.getTarget().getName())

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def setGM(gmId):
    """Set the target's GM level (used for icon)."""
    if gmId == 1:
        return 'You cannot set a toon to TOON COUNCIL.'
    if not 0 <= gmId <= 4:
        return 'Invalid GM type specified.'
    if spellbook.getTarget().isGM() and gmId != 0: # This is because if you change from 1 GM level to another (excluding 0), it won't update in-game.
        spellbook.getTarget().b_setGM(0)
    spellbook.getTarget().b_setGM(gmId)
    return 'You have set %s to GM type %s' % (spellbook.getTarget().getName(), gmId)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def setTickets(tixVal):
    """Set the target's racing ticket's value."""
    if not 0 <= tixVal <= 99999:
        return 'Ticket value out of range (0-99999)'
    spellbook.getTarget().b_setTickets(tixVal)
    return "%s's tickets were set to %s." % (spellbook.getTarget().getName(), tixVal)

@magicWord(category=CATEGORY_OVERRIDE, types=[int])
def setCogIndex(indexVal):
    """Transform into a cog/suit. THIS SHOULD ONLY BE USED WHERE NEEDED, E.G. ELECTIONS"""
    if not -1 <= indexVal <= 3:
        return 'CogIndex value %s is invalid.' % str(indexVal)
    spellbook.getTarget().b_setCogIndex(indexVal)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str, str])
def dna(part, value):
    # This is where the fun begins, woo!
    """Set a specific part of DNA for the target toon. Be careful, you don't want to break anyone!"""

    av = spellbook.getTarget()

    dna = ToonDNA.ToonDNA()
    dna.makeFromNetString(av.getDNAString())

    def isValidColor(colorIndex):
        if not 0 <= colorIndex <= 26: # This could actually be selected from ToonDNA, but I prefer this :D
            return False
        if colorIndex == 0 and dna.getAnimal() != 'bear':
            return False
        if colorIndex == 26 and dna.getAnimal() != 'cat':
            return False
        return True

    # Body Part Colors
    if part=='headColor':
        value = int(value)
        if not isValidColor(value):
            return "DNA: Invalid color specified for head."
        dna.headColor = value
    elif part=='armColor':
        value = int(value)
        if not isValidColor(value):
            return "DNA: Invalid color specified for arms."
        dna.armColor = value
    elif part=='legColor':
        value = int(value)
        if not isValidColor(value):
            return "DNA: Invalid color specified for legs."
        dna.legColor = value
    elif part=='color':
        value = int(value)
        if not isValidColor(value):
            return "DNA: Invalid color specified for toon."
        dna.headColor = value
        dna.armColor = value
        dna.legColor = value
    elif part=='gloves': # Incase anyone tries to change glove color for whatever reason...
        return "DNA: Change of glove colors are not allowed."
        # If you ever want to be able to edit gloves, feel free to comment out this return.
        # However, since DToonAI checks ToonDNA, this would be impossible unless changes
        # are made.
        value = int(value)
        if not 0 <= value <= 26:
            return "DNA: Color index out of range."
        dna.gloveColor = value

    # Body Sizes, Species & Gender (y u want to change gender pls)
    elif part=='gender':
        if value=='male':
            dna.gender = 'm'
        elif value=='female':
            dna.gender = 'f'
        else:
            return "DNA: Invalid gender. Stick to 'male' or 'female'."
    elif part=='species':
        species = ['dog', 'cat', 'horse', 'mouse', 'rabbit', 'duck', 'monkey', 'bear', 'pig']
        if value not in species:
            return "DNA: Invalid head type specified."
        if dna.headColor == 0x1a and value != 'cat':
            return "DNA: Cannot have a black toon (non-cat)!"
        if dna.headColor == 0 and value != 'bear':
            return "DNA: Cannot have a white toon (non-bear)!"
        species = dict(map(None, species, ToonDNA.toonSpeciesTypes))
        headSize = dna.head[1:3]
        dna.head = (species.get(value) + headSize)
    elif part=='headSize':
        sizes = ['ls', 'ss', 'sl', 'll']
        value = int(value)
        if not 0 <= value <= 3:
            return "DNA: Invalid head size index."
        species = dna.head[0]
        dna.head = (species + sizes[value])
    elif part=='torso':
        value = int(value)
        if dna.gender == 'm':
            if not 0 <= value <= 2:
                return "DNA: Male torso index out of range (0-2)."
        elif dna.gender == 'f':
            if not 3 <= value <= 8:
                return "DNA: Female torso index out of range (3-8)."
        else:
            return "DNA: Unable to determine gender. Aborting DNA change."
        dna.torso = ToonDNA.toonTorsoTypes[value]
    elif part=='legs':
        value = int(value)
        if not 0 <= value <= 2:
            return "DNA: Legs index out of range."
        dna.legs = ToonDNA.toonLegTypes[value]

    # Allow Admins to back up a toons current DNA before making changes.
    elif part=='save':
        av.mwDNABackup[spellbook.getInvoker().doId] = av.getDNAString()
        return "Saved DNA to toon's DToonAI. Note: If the toon logs out, the save will be lost!"

    # Restore from a previous back up of DNA.
    elif part=='restore':
        if spellbook.getInvoker().doId in av.mwDNABackup:
            dna.makeFromNetString(av.mwDNABackup.get(spellbook.getInvoker().doId))
            av.b_setDNAString(dna.makeNetString())
            return "Restored %s's DNA to last save." % av.getName()
        else:
            return "DNA: There are no backups available."

    # Don't allow them to submit any changes if they don't enter a valid DNA part.
    else:
        return "DNA: Invalid part specified."

    av.b_setDNAString(dna.makeNetString())
    return "Completed DNA change successfully."

@magicWord(category=CATEGORY_OVERRIDE, types=[int])
def setTrophyScore(value):
    """Set the trophy score of target"""
    if value < 0:
        return "Cannot have a trophy score below 0."
    spellbook.getTarget().d_setTrophyScore(value)

@magicWord(category=CATEGORY_OVERRIDE, types=[int, int])
def givePies(pieType, numPies=0):
    """Give target Y number of X pies."""
    av = spellbook.getTarget()
    if pieType == -1:
        av.b_setNumPies(0)
        return "Removed %s's pies." % spellbook.getTarget().getName()
    if pieType == 6:
        return "Wedding cake 'pie' cause client crashes!"
    if not 0 <= pieType <= 7:
        return "pieType value out of range (0-7)"
    if not 0 <= numPies <= 99:
        return "numPies value out of range (0-99)"
    av.b_setPieType(pieType)
    av.b_setNumPies(numPies)

# TODO: Set minimum access for this MW back to 400, after fishing supports quests.
@magicWord(category=CATEGORY_OVERRIDE, types=[int, int])
def setQP(questId=0, progress=0):
    """
    Get current questId in progress via ~setQP.
    Set questId progress via ~setQP questId value.
    """

    av = spellbook.getTarget()
    questIds = ""
    for index in range(len(av.quests)):
        questIds += "{0} ".format(av.quests[index][0])
        if av.quests[index][0] == questId:
            av.quests[index][4] = progress
    av.b_setQuests(av.quests)
    return questIds

@magicWord(category=CATEGORY_MODERATION, types=[int, str])
def locate(avIdShort=0, returnType=''):
    """Locate an avatar anywhere on the [CURRENT] AI."""
    # TODO: Use Astron msgs to get location of avId from anywhere in the Astron cyber-space.
    # NOTE: The avIdShort concept needs changing, especially when we start entering 200000000's for avIds
    if avIdShort <= 0:
        return "Please enter a valid avId to find! Note: You only need to enter the last few digits of the full avId!"
    avIdFull = 400000000 - (300000000 - avIdShort)
    av = simbase.air.doId2do.get(avIdFull, None)
    if not av:
        return "Could not find the avatar on the current AI."

    # Get the avatar's location.
    zoneId = av.getLocation()[1] # This returns: (parentId, zoneId)
    trueZoneId = zoneId
    interior = False

    if returnType == 'zone':
        # The avatar that called the MagicWord wants a zoneId... Provide them with the untouched zoneId.
        return "%s is in zoneId %d." % (av.getName(), trueZoneId)

    if returnType == 'playground':
        # The avatar that called the MagicWord wants the playground name that the avatar is currently in.
        zoneId = ZoneUtil.getCanonicalHoodId(zoneId)

    if ZoneUtil.isInterior(zoneId):
        # If we're in an interior, we want to fetch the street/playground zone, since there isn't
        # any mapping for interiorId -> shop name (afaik).
        zoneId -= 500
        interior = True

    if ZoneUtil.isPlayground(zoneId):
        # If it's a playground, TTG contains a map of all hoodIds -> playground names.
        where = ToontownGlobals.hoodNameMap.get(zoneId, None)
    else:
        # If it's not a playground, the TTL contains a list of all streetId -> street names.
        zoneId = zoneId - zoneId % 100 # This essentially truncates the last 2 digits.
        where = TTLocalizer.GlobalStreetNames.get(zoneId, None)

    if not where:
        return "Failed to map the zoneId %d [trueZoneId: %d] to a location..." % (zoneId, trueZoneId)

    if interior:
        return "%s has been located %s %s, inside a building." % (av.getName(), where[1], where[2])
    return "%s has been located %s %s." % (av.getName(), where[1], where[2])

@magicWord(category=CATEGORY_OVERRIDE, types=[int])
def online(doId):
    """ Check if a toon is online. """
    av = spellbook.getTarget()
    doId = 100000000 + doId
    simbase.air.getActivated(doId, lambda x,y: av.d_setSystemMessage(0, '%d is %s!' % (x, 'online' if y else 'offline')))

@magicWord(category=CATEGORY_OVERRIDE)
def unlimitedGags():
    """ Restock avatar's gags at the start of each round. """
    av = spellbook.getTarget() if spellbook.getInvokerAccess() >= 500 else spellbook.getInvoker()
    av.setUnlimitedGags(not av.unlimitedGags)
    return 'Toggled unlimited gags %s for %s' % ('ON' if av.unlimitedGags else 'OFF', av.getName())

@magicWord(category=CATEGORY_OVERRIDE)
def immortal():
    """ Make target (if 500+) or self (if 499-) immortal. """
    av = spellbook.getTarget() if spellbook.getInvokerAccess() >= 500 else spellbook.getInvoker()
    av.setImmortalMode(not av.immortalMode)
    return 'Toggled immortal mode %s for %s' % ('ON' if av.immortalMode else 'OFF', av.getName())

@magicWord(category=CATEGORY_CHARACTERSTATS)
def sostoons():
    """Restock all *good* VP SOS toons."""
    spellbook.getTarget().restockAllNPCFriends(99)
    return 'Restocked all NPC SOS toons successfully!'

@magicWord(category=CATEGORY_CHARACTERSTATS)
def unites():
    """Restock all CFO phrases."""
    spellbook.getTarget().restockAllResistanceMessages(99)
    return 'Restocked all unites successfully!'

@magicWord(category=CATEGORY_OVERRIDE)
def summons():
    """ Restock all CJ summons. """
    av = spellbook.getInvoker()
    # Make sure we have every cog in our Cog Page.
    cogCount = []
    from toontown.shtiker import CogPageGlobals
    for deptIndex in xrange(4):
        for cogIndex in xrange(8):
            cogCount.append(CogPageGlobals.COG_QUOTAS[1][cogIndex])
    av.b_setCogCount(cogCount)
    av.b_setCogStatus([CogPageGlobals.COG_COMPLETE2] * 32)
    av.restockAllCogSummons()
    return 'Restocked all cog summons successfully!'

@magicWord(category=CATEGORY_OVERRIDE)
def pinkslips():
    """ Restock (to 99) CEO pink slips. """
    spellbook.getTarget().b_setPinkSlips(99)
    return 'Restocked 99 pink slips successfully!'

@magicWord(category=CATEGORY_OVERRIDE, types=[int])
def questTier(tier):
    """
    Set toon's tier to specified value. Note that this does not give the
    toon the rewards they would normally require to be in this tier, so
    use this magic word with caution. This will also reset all of the
    target's quests, so they will lose any progress on any tasks that
    they are currently working on.
    """
    av = spellbook.getTarget()
    av.b_setQuests([])
    av.b_setRewardHistory(tier, [])
    return "Set %s's quest tier to %d." % (av.getName(), tier)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int, int, int, int, int, int, int])
def tracks(toonup, trap, lure, sound, throw, squirt, drop):
    """ Set access for each of the 7 gag tracks. """
    spellbook.getTarget().b_setTrackAccess([toonup, trap, lure, sound, throw, squirt, drop])
    return "Set track access accordingly."

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str, int])
def exp(track, amt):
    """ Set your experience to the amount specified for a single track. """
    trackIndex = TTLocalizer.BattleGlobalTracks.index(track)
    av = spellbook.getTarget()
    av.experience.setExp(trackIndex, amt)
    av.b_setExperience(av.experience.makeNetString())
    return "Set %s exp to %d successfully." % (track, amt)

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str, str, int])
def disguise(corp, type, level=0):
    """ Set disguise type and level. """
    # Idk if this is defined anywhere, but laziness got the best of me.
    corps = ['bossbot', 'lawbot', 'cashbot', 'sellbot']
    if corp not in corps:
        return "Invalid cog corp. specified."
    corpIndex = corps.index(corp)
    toon = spellbook.getTarget()

    if type == "nosuit":
        # They want to reset their suit entirely.
        parts = toon.getCogParts()
        parts[corpIndex] = 0
        toon.b_setCogParts(parts)
        types = toon.getCogTypes()
        types[corpIndex] = 0
        toon.b_setCogTypes(types)
        levels = toon.getCogLevels()
        levels[corpIndex] = 0
        toon.b_setCogLevels(levels)
        merits = toon.getCogMerits()
        merits[corpIndex] = 0
        toon.b_setCogMerits(merits)
        return "Reset %s disguise and removed all earned parts." % corp.capitalize()

    if level == 0:
        return "You must specify a level!"

    # Get the cog type from the specified short-hand value.
    types = SuitDNA.suitHeadTypes[8*corpIndex:(8*corpIndex)+8]
    if type not in types:
        return "Invalid cog type specified. Note that this uses the short-hand, such as 'rb' or 'tbc'."
    typeIndex = types.index(type)

    # Make sure they gave a level that is in range.
    if typeIndex == 7:
        # The final suit can go up to Level 50.
        levelRange = range(8, 51) # Last digit is exclusive.
    else:
        levelRange = range((typeIndex+1), (typeIndex+6))
    if level not in levelRange:
        return "Invalid level specified for %s disguise %s." % (corp.capitalize(), SuitBattleGlobals.SuitAttributes[type]['name'])

    # Reset their merits to 0.
    merits = toon.getCogMerits()
    merits[corpIndex] = 0
    toon.b_setCogMerits(merits)

    # Ensure they have all the parts.
    # TODO: Allow them to set the parts they have. This will probably be another MW: ~parts leftleg 1
    parts = toon.getCogParts()
    parts[corpIndex] = CogDisguiseGlobals.PartsPerSuitBitmasks[corpIndex]
    toon.b_setCogParts(parts)

    # Find out if they need laff boosts or laff points removed.
    for levelBoost in [14, 19, 29, 39, 49]:
        if level <= levelBoost and not levelBoost > toon.getCogLevels()[corpIndex]:
            if toon.getMaxHp() <= 15:
                continue
            toon.b_setMaxHp(toon.getMaxHp()-1)
        elif level > levelBoost and not levelBoost <= toon.getCogLevels()[corpIndex]:
            if toon.getMaxHp() >= 137:
                continue
            toon.b_setMaxHp(toon.getMaxHp()+1)
    # Lets be nice and give them a toonup or make them suffer.
    if toon.getHp() > toon.getMaxHp():
        toon.takeDamage(toon.getHp() - toon.getMaxHp())
    else:
        toon.toonUp(toon.getMaxHp() - toon.getHp())

    # Set their type and level that they specified.
    types = toon.getCogTypes()
    types[corpIndex] = typeIndex
    toon.b_setCogTypes(types)
    levels = toon.getCogLevels()
    levels[corpIndex] = level-1 # -1 because it starts at 0
    toon.b_setCogLevels(levels)

    return "Set %s disguise to %s Level %d." % (corp.capitalize(), SuitBattleGlobals.SuitAttributes[type]['name'], level)

@magicWord(category=CATEGORY_OVERRIDE, types=[str, int])
def merits(corp, amount):
    """ Set the target's merits to the value specified. """
    corps = ['bossbot', 'lawbot', 'cashbot', 'sellbot']
    if corp not in corps:
        return "Invalid cog corp. specified."
    corpIndex = corps.index(corp)
    toon = spellbook.getTarget()

    # Correct me if I'm wrong, but I don't think we need a sanity check for the amount.
    merits = toon.getCogMerits()
    merits[corpIndex] = amount
    toon.b_setCogMerits(merits)

@magicWord(category=CATEGORY_OVERRIDE)
def fanfare():
    """ Give target toon a fanfare for the lolz. """
    spellbook.getTarget().magicFanfare()
    return "Jason: Because the trumpets they go...~"

@magicWord(category=CATEGORY_CHARACTERSTATS, types=[int])
def pouch(amt):
    """ Set the target's max gag limit. """
    spellbook.getTarget().b_setMaxCarry(amt)
    return "Set %s's pouch size to %d" % (spellbook.getTarget().getName(), amt)

@magicWord(category=CATEGORY_MODERATION, types=[int])
def goto(avIdShort):
    """ Teleport to the avId specified. """
    avId = 100000000+avIdShort # To get target doId.
    toon = simbase.air.doId2do.get(avId)
    if not toon:
        return "Unable to teleport to target, they are not currently on this district."
    spellbook.getInvoker().magicWordTeleportRequests.append(avId)
    toon.sendUpdate('magicTeleportRequest', [spellbook.getInvoker().getDoId()])

@magicWord(category=CATEGORY_SYSADMIN)
def dump_doId2do():
    """
    Please note that this MW should NOT be used more than it needs to be on a live
    cluster. This is very hacked together and is purely so we can get a dump of doId2do
    to get an idea of where the huge memory usage is coming from.

    This should be removed once we are complete.
    """
    import sys, operator, tempfile
    objSizes = {}
    for object in simbase.air.doId2do.itervalues():
        # Iterate through each object in doId2do.
        name = object.__class__.__name__
        objCurrSizes = objSizes.get(name)
        if not objCurrSizes:
            # We haven't yet come across this class. Store first size value.
            objSizes[name] = sys.getsizeof(object)
        else:
            # Increment the stored value by the size of the object we just
            # iterated through.
            objSizes[name] += sys.getsizeof(object)
    # Sort the dict by the size of the objects.
    # N.B.: This spits out a list of tuples, e.g: [('obj1', 1000), ('obj2', 1001)]
    sorted_objSizes = sorted(objSizes.iteritems(), key=operator.itemgetter(1))
    # Create a temporary file that we can store to. This returns a tuple of a file
    # handler and an absolute file location. (handler, location)
    temp_file = tempfile.mkstemp(prefix='doId2do-dump_', suffix='.txt', text=True)
    # Screw the documents, the first value in temp_file is a useless pile of dog shit.
    # I hax and do like this. <3
    with open(temp_file[1], 'w+') as file:
        # Write each class to the file, containing the name and the total size of
        # all instances of that class.
        for name, size in sorted_objSizes:
            file.write('OBJ: %s | SIZE: %d\n' % (name, size))
    return "Dumped doId2do sizes (grouped by class) to '%s'." % temp_file[1]
