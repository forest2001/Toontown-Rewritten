from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.speedchat.SpeedChatTypes import *
from toontown.speedchat.TTSpeedChatTypes import *
from otp.speedchat.SpeedChat import SpeedChat
from otp.speedchat import SpeedChatGlobals
from toontown.speedchat import TTSpeedChatGlobals
from toontown.speedchat import TTSCSingingTerminal
from toontown.speedchat import TTSCIndexedTerminal
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from toontown.shtiker.OptionsPage import speedChatStyles
from toontown.toonbase import TTLocalizer
from toontown.parties.PartyGlobals import ActivityIds, DecorationIds
from toontown.toonbase import ToontownGlobals
scStructure = [
 [OTPLocalizer.SCMenuTesting,
  [OTPLocalizer.SCMenuBugs,
   5406,
   5407,
   5408,
   5409,
   5410,
   5411,
   5412],
  5400,
  5401,
  5402,
  5403,
  5404,
  5405],
 [OTPLocalizer.SCMenuHello,
  {100: 0},
  {101: 0},
  {102: 0},
  {103: 0},
  {104: 0},
  {105: 0},
  106,
  107,
  108],
 [OTPLocalizer.SCMenuBye,
  {200: 0},
  {201: 0},
  {202: 0},
  203,
  204,
  205,
  206,
  207,
  208,
  209],
 [OTPLocalizer.SCMenuConvo,
  [OTPLocalizer.SCMenuEmoticons,
   5500,
   {5501: 2},
   5502,
   5503,
   5504,
   5505,
   5506,
   5507],
  [OTPLocalizer.SCMenuFriendlyILike,
   700,
   701,
   702,
   703,
   704,
   705,
   706,
   707],
  5600,
  5601,
  5602,
  5603,
  5604],
 [OTPLocalizer.SCMenuResponse,
  [OTPLocalizer.SCMenuGood,
   {5700: 1},
   5701,
   5702,
   5703],
  [OTPLocalizer.SCMenuBad,
   5800,
   5801,
   {5802: 2},
   {5803: 2}],
  [OTPLocalizer.SCMenuHappy,
   {300: 1},
   {301: 1},
   {302: 1},
   {303: 1},
   304,
   305,
   306,
   307,
   308,
   309,
   310,
   311],
  [OTPLocalizer.SCMenuSad,
   {400: 2},
   {401: 2},
   402,
   403,
   404,
   405,
   406,
   {407: 2}],
  5900,
  5901,
  5902,
  5903,
  5904,
  5905],
 [OTPLocalizer.SCMenuFriendly,
  [OTPLocalizer.SCMenuFriendlyYou,
   600,
   601,
   602,
   603],
  500,
  501,
  502,
  503,
  504,
  505,
  506,
  507,
  508,
  509,
  510,
  511],
 [OTPLocalizer.SCMenuSorry,
  [OTPLocalizer.SCMenuBusy,
   808,
   809,
   810,
   811,
   812,
   813,
   814,
   815,
   816,
   817],
  800,
  801,
  802,
  803,
  804,
  805,
  806,
  807],
 [OTPLocalizer.SCMenuStinky,
  {900: 3},
  {901: 3},
  {902: 3},
  {903: 3},
  904,
  905],
 [OTPLocalizer.SCMenuPlaces,
  [OTPLocalizer.SCMenuPlacesPlayground,
   1100,
   1101,
   1102,
   1103,
   1104,
   1105,
   1106,
   1107,
   1108,
   1109,
   1110,
   1111],
  [OTPLocalizer.SCMenuPlacesCogs,
   1112,
   1113,
   1114,
   1115,
   1116,
   1117,
   1118,
   1119,
   1120,
   1121,
   1122,
   1123],
  [OTPLocalizer.SCMenuPlacesEstate,
   1124,
   1125,
   1126,
   1127,
   1128],
  [OTPLocalizer.SCMenuParties,
   5300,
   5301,
   5302,
   5303],
  [OTPLocalizer.SCMenuPlacesWait,
   1130,
   1131,
   1132,
   1133,
   1134,
   1135,
   1136],
  1000,
  1001,
  1002,
  1003,
  1004,
  1005,
  1006,
  1007,
  1008],
 [OTPLocalizer.SCMenuToontasks,
  [TTSCToontaskMenu, OTPLocalizer.SCMenuToontasksMyTasks],
  [OTPLocalizer.SCMenuToontasksYouShouldChoose,
   1300,
   1301,
   1302,
   1303,
   1304],
  [OTPLocalizer.SCMenuToontasksINeedMore,
   1206,
   1210,
   1211,
   1212,
   1207,
   1213,
   1214,
   1215],
  1200,
  1201,
  1202,
  1208,
  1203,
  1209,
  1204,
  1205],
 [OTPLocalizer.SCMenuBattle,
  [OTPLocalizer.SCMenuBattleStrategy,
   [OTPLocalizer.SCMenuBattleUse,
    [OTPLocalizer.SCMenuBattleToonUp,
     6000,
     6001,
     6002,
     6003,
     6004,
     6005],
    [OTPLocalizer.SCMenuBattleTrap,
     6010,
     6011,
     6012,
     6013,
     6014,
     6015],
    [OTPLocalizer.SCMenuBattleLure,
     6020,
     6021,
     6022,
     6023,
     6024,
     6025,
     6026],
    [OTPLocalizer.SCMenuBattleSound,
     6030,
     6031,
     6032,
     6033],
    [OTPLocalizer.SCMenuBattleThrow,
     6040,
     6041,
     6042,
     6043,
     6044,
     6045],
    [OTPLocalizer.SCMenuBattleSquirt,
     6050,
     6051,
     6052,
     6053,
     6054,
     6055],
    [OTPLocalizer.SCMenuBattleDrop,
     6060,
     6061,
     6062,
     6063,
     6064,
     6065]],  
   [OTPLocalizer.SCMenuBattleGags,    
    1500,   
    1501,
    1502,
    1503,
    1504,
    1505,
    1506,
    1507,
    1508,
    1509,
    1510],
   1416,
   1550,
   1551,
   1552,
   1415,
   1553,
   1554,
   1555,
   1556,
   1557,
   1558,
   1559],
  [OTPLocalizer.SCMenuBattleTaunts,
   1520,
   1521,
   1522,
   1523,
   1524,
   1525,
   1526,
   1527,
   1528,
   1529],
  1400,
  1401,
  1402,
  1403,
  1404,
  1405,
  1406],
 [OTPLocalizer.SCMenuGagShop,
  1600,
  1601,
  1602,
  1603,
  1604,
  1605],
 {1: 17},
 {2: 18},
 3]
if hasattr(base, 'wantPets') and base.wantPets:
    scPetMenuStructure = [[OTPLocalizer.SCMenuPets,
      [TTSCPetTrickMenu, OTPLocalizer.SCMenuPetTricks],
      21000,
      21001,
      21002,
      21003,
      21004,
      21005,
      21006]]
cfoMenuStructure = [[OTPLocalizer.SCMenuCFOBattleCranes,
  2100,
  2101,
  2102,
  2103,
  2104,
  2105,
  2106,
  2107,
  2108,
  2109,
  2110],
 [OTPLocalizer.SCMenuCFOBattleGoons,
  2120,
  2121,
  2122,
  2123,
  2124,
  2125,
  2126],
 2130,
 2131,
 2132,
 2133,
 1410]
cjMenuStructure = [2200,
 2201,
 2202,
 2203,
 2204,
 2205,
 2206,
 2207,
 2208,
 2209,
 2210]
ceoMenuStructure = [2300,
 2301,
 2302,
 2303,
 2304,
 2305,
 2306,
 2307,
 2312,
 2313,
 2314,
 2315,
 2308,
 2309,
 2310,
 2311,
 2316,
 2317]

class TTChatInputSpeedChat(DirectObject.DirectObject):
    DefaultSCColorScheme = SCColorScheme()

    def __init__(self, chatMgr):
        self.chatMgr = chatMgr
        self.whisperAvatarId = None
        self.toPlayer = 0
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.emoteNoAccessPanel = DirectFrame(parent=hidden, relief=None, state='normal', text=OTPLocalizer.SCEmoteNoAccessMsg, frameSize=(-1, 1, -1, 1), geom=DGG.getDefaultDialogGeom(), geom_color=OTPGlobals.GlobalDialogColor, geom_scale=(0.92, 1, 0.6), geom_pos=(0, 0, -.08), text_scale=0.08)
        self.okButton = DirectButton(parent=self.emoteNoAccessPanel, image=okButtonImage, relief=None, text=OTPLocalizer.SCEmoteNoAccessOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.2), command=self.handleEmoteNoAccessDone)
        self.insidePartiesMenu = None
        self.createSpeedChat()
        self.whiteList = None
        self.allowWhiteListSpeedChat = base.config.GetBool('white-list-speed-chat', 0)
        if self.allowWhiteListSpeedChat:
            self.addWhiteList()
        self.factoryMenu = None
        self.kartRacingMenu = None
        self.cogMenu = None
        self.cfoMenu = None
        self.cjMenu = None
        self.ceoMenu = None
        self.golfMenu = None
        self.boardingGroupMenu = None
        self.singingGroupMenu = None
        self.aprilToonsMenu = None
        self.victoryPartiesMenu = None
        self.sillyPhaseOneMenu = None
        self.sillyPhaseTwoMenu = None
        self.sillyPhaseThreeMenu = None
        self.sillyPhaseFourMenu = None
        self.sillyPhaseFiveMenu = None
        self.sellbotNerfMenu = None
        self.jellybeanJamMenu = None
        self.halloweenMenu = None
        self.winterMenu = None
        self.sellbotInvasionMenu = None
        self.sellbotFieldOfficeMenu = None
        self.idesOfMarchMenu = None

        def listenForSCEvent(eventBaseName, handler, self = self):
            eventName = self.speedChat.getEventName(eventBaseName)
            self.accept(eventName, handler)

        listenForSCEvent(SpeedChatGlobals.SCTerminalLinkedEmoteEvent, self.handleLinkedEmote)
        listenForSCEvent(SpeedChatGlobals.SCStaticTextMsgEvent, self.handleStaticTextMsg)
        listenForSCEvent(SpeedChatGlobals.SCCustomMsgEvent, self.handleCustomMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteMsgEvent, self.handleEmoteMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteNoAccessEvent, self.handleEmoteNoAccess)
        listenForSCEvent(TTSpeedChatGlobals.TTSCToontaskMsgEvent, self.handleToontaskMsg)
        listenForSCEvent(TTSpeedChatGlobals.TTSCResistanceMsgEvent, self.handleResistanceMsg)
        listenForSCEvent(TTSCSingingTerminal.TTSCSingingMsgEvent, self.handleSingingMsg)
        listenForSCEvent('SpeedChatStyleChange', self.handleSpeedChatStyleChange)
        listenForSCEvent(TTSCIndexedTerminal.TTSCIndexedMsgEvent, self.handleStaticTextMsg)
        self.fsm = ClassicFSM.ClassicFSM('SpeedChat', [State.State('off', self.enterOff, self.exitOff, ['active']), State.State('active', self.enterActive, self.exitActive, ['off'])], 'off', 'off')
        self.fsm.enterInitialState()
        return

    def delete(self):
        self.ignoreAll()
        self.removeWhiteList()
        self.okButton.destroy()
        self.emoteNoAccessPanel.destroy()
        del self.emoteNoAccessPanel
        self.speedChat.destroy()
        del self.speedChat
        del self.fsm
        del self.chatMgr

    def show(self, whisperAvatarId = None, toPlayer = 0):
        self.whisperAvatarId = whisperAvatarId
        self.toPlayer = toPlayer
        self.fsm.request('active')

    def hide(self):
        self.fsm.request('off')

    def createSpeedChat(self):
        structure = []
        if launcher and not launcher.isTestServer() or __dev__:
            structure.append([TTSCPromotionalMenu, OTPLocalizer.SCMenuPromotion])
        structure.append([SCEmoteMenu, OTPLocalizer.SCMenuEmotions])
        structure.append([SCCustomMenu, OTPLocalizer.SCMenuCustom])
        structure.append([TTSCResistanceMenu, OTPLocalizer.SCMenuResistance])
        if base.config.GetBool('want-doomsday', False):
          structure.append([OTPLocalizer.SCMenuElection, 10100, 10101, 10102, 10103, 10104, 10105])
        if hasattr(base, 'wantPets') and base.wantPets:
            structure += scPetMenuStructure
        structure += scStructure
        self.createSpeedChatObject(structure)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterActive(self):

        def handleCancel(self = self):
            self.chatMgr.fsm.request('mainMenu')

        self.accept('mouse1', handleCancel)

        def selectionMade(self = self):
            self.chatMgr.fsm.request('mainMenu')

        self.terminalSelectedEvent = self.speedChat.getEventName(SpeedChatGlobals.SCTerminalSelectedEvent)
        if base.config.GetBool('want-sc-auto-hide', 1):
            self.accept(self.terminalSelectedEvent, selectionMade)
        self.speedChat.reparentTo(base.a2dpTopLeft, DGG.FOREGROUND_SORT_INDEX)
        scZ = -0.04
        self.speedChat.setPos(0.283, 0, scZ)
        self.speedChat.setWhisperMode(self.whisperAvatarId != None)
        self.speedChat.enter()
        return

    def exitActive(self):
        self.ignore('mouse1')
        self.ignore(self.terminalSelectedEvent)
        self.speedChat.exit()
        self.speedChat.reparentTo(hidden)
        self.emoteNoAccessPanel.reparentTo(hidden)

    def handleLinkedEmote(self, emoteId):
        if self.whisperAvatarId is None:
            lt = base.localAvatar
            lt.b_setEmoteState(emoteId, animMultiplier=lt.animMultiplier)
        return

    def handleStaticTextMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCChatMessage(textId)
        else:
            self.chatMgr.sendSCWhisperMessage(textId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleSingingMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCSingingChatMessage(textId)
        else:
            self.chatMgr.sendSCSingingWhisperMessage(textId)
        self.toPlayer = 0
        return

    def handleCustomMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCCustomChatMessage(textId)
        else:
            self.chatMgr.sendSCCustomWhisperMessage(textId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleEmoteMsg(self, emoteId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCEmoteChatMessage(emoteId)
        else:
            self.chatMgr.sendSCEmoteWhisperMessage(emoteId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleEmoteNoAccess(self):
        if self.whisperAvatarId is None:
            self.emoteNoAccessPanel.setPos(0, 0, 0)
        else:
            self.emoteNoAccessPanel.setPos(0.37, 0, 0)
        self.emoteNoAccessPanel.reparentTo(aspect2d)
        return

    def handleEmoteNoAccessDone(self):
        self.emoteNoAccessPanel.reparentTo(hidden)

    def handleToontaskMsg(self, taskId, toNpcId, toonProgress, msgIndex):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCToontaskChatMessage(taskId, toNpcId, toonProgress, msgIndex)
        else:
            self.chatMgr.sendSCToontaskWhisperMessage(taskId, toNpcId, toonProgress, msgIndex, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleResistanceMsg(self, textId):
        self.chatMgr.sendSCResistanceChatMessage(textId)

    def handleSpeedChatStyleChange(self):
        nameKey, arrowColor, rolloverColor, frameColor = speedChatStyles[base.localAvatar.getSpeedChatStyleIndex()]
        newSCColorScheme = SCColorScheme(arrowColor=arrowColor, rolloverColor=rolloverColor, frameColor=frameColor)
        self.speedChat.setColorScheme(newSCColorScheme)

    def createSpeedChatObject(self, structure):
        if hasattr(self, 'speedChat'):
            self.speedChat.exit()
            self.speedChat.destroy()
            del self.speedChat
        self.speedChat = SpeedChat(structure=structure, backgroundModelName='phase_3/models/gui/ChatPanel', guiModelName='phase_3.5/models/gui/speedChatGui')
        self.speedChat.setScale(TTLocalizer.TTCISCspeedChat)
        self.speedChat.setBin('gui-popup', 0)
        self.speedChat.setTopLevelOverlap(TTLocalizer.TTCISCtopLevelOverlap)
        self.speedChat.setColorScheme(self.DefaultSCColorScheme)
        self.speedChat.finalizeAll()

    def addFactoryMenu(self):
        if self.factoryMenu == None:
            menu = TTSCFactoryMenu()
            self.factoryMenu = SCMenuHolder(OTPLocalizer.SCMenuFactory, menu=menu)
            self.speedChat[2:2] = [self.factoryMenu]
        return

    def removeFactoryMenu(self):
        if self.factoryMenu:
            i = self.speedChat.index(self.factoryMenu)
            del self.speedChat[i]
            self.factoryMenu.destroy()
            self.factoryMenu = None
        return

    def addKartRacingMenu(self):
        if self.kartRacingMenu == None:
            menu = TTSCKartRacingMenu()
            self.kartRacingMenu = SCMenuHolder(OTPLocalizer.SCMenuKartRacing, menu=menu)
            self.speedChat[2:2] = [self.kartRacingMenu]
        return

    def removeKartRacingMenu(self):
        if self.kartRacingMenu:
            i = self.speedChat.index(self.kartRacingMenu)
            del self.speedChat[i]
            self.kartRacingMenu.destroy()
            self.kartRacingMenu = None
        return

    def addCogMenu(self, indices):
        if self.cogMenu == None:
            menu = TTSCCogMenu(indices)
            self.cogMenu = SCMenuHolder(OTPLocalizer.SCMenuCog, menu=menu)
            self.speedChat[2:2] = [self.cogMenu]
        return

    def removeCogMenu(self):
        if self.cogMenu:
            i = self.speedChat.index(self.cogMenu)
            del self.speedChat[i]
            self.cogMenu.destroy()
            self.cogMenu = None
        return

    def addCFOMenu(self):
        if self.cfoMenu == None:
            menu = SCMenu()
            menu.rebuildFromStructure(cfoMenuStructure)
            self.cfoMenu = SCMenuHolder(OTPLocalizer.SCMenuCFOBattle, menu=menu)
            self.speedChat[2:2] = [self.cfoMenu]
        return

    def removeCFOMenu(self):
        if self.cfoMenu:
            i = self.speedChat.index(self.cfoMenu)
            del self.speedChat[i]
            self.cfoMenu.destroy()
            self.cfoMenu = None
        return

    def addCJMenu(self, bonusWeight = -1):
        if self.cjMenu == None:
            menu = SCMenu()
            myMenuCopy = cjMenuStructure[:]
            if bonusWeight >= 0:
                myMenuCopy.append(2211 + bonusWeight)
            menu.rebuildFromStructure(myMenuCopy)
            self.cjMenu = SCMenuHolder(OTPLocalizer.SCMenuCJBattle, menu=menu)
            self.speedChat[2:2] = [self.cjMenu]
        return

    def removeCJMenu(self):
        if self.cjMenu:
            i = self.speedChat.index(self.cjMenu)
            del self.speedChat[i]
            self.cjMenu.destroy()
            self.cjMenu = None
        return

    def addCEOMenu(self):
        if self.ceoMenu == None:
            menu = SCMenu()
            menu.rebuildFromStructure(ceoMenuStructure)
            self.ceoMenu = SCMenuHolder(OTPLocalizer.SCMenuCEOBattle, menu=menu)
            self.speedChat[2:2] = [self.ceoMenu]
        return

    def removeCEOMenu(self):
        if self.ceoMenu:
            i = self.speedChat.index(self.ceoMenu)
            del self.speedChat[i]
            self.ceoMenu.destroy()
            self.ceoMenu = None
        return

    def addInsidePartiesMenu(self):

        def isActivityInParty(activityId):
            activityList = base.distributedParty.partyInfo.activityList
            for activity in activityList:
                if activity.activityId == activityId:
                    return True

            return False

        def isDecorInParty(decorId):
            decorList = base.distributedParty.partyInfo.decors
            for decor in decorList:
                if decor.decorId == decorId:
                    return True

            return False

        insidePartiesMenuStructure = [5305,
         5306,
         5307,
         5308,
         5309]
        if self.insidePartiesMenu == None:
            menu = SCMenu()
            if hasattr(base, 'distributedParty') and base.distributedParty:
                if base.distributedParty.partyInfo.hostId == localAvatar.doId:
                    insidePartiesMenuStructure.insert(0, 5304)
                if isActivityInParty(0):
                    insidePartiesMenuStructure.extend([5310, 5311])
                if isActivityInParty(1):
                    insidePartiesMenuStructure.append(5312)
                if isActivityInParty(2):
                    insidePartiesMenuStructure.extend([5313, 5314])
                if isActivityInParty(3):
                    insidePartiesMenuStructure.append(5315)
                if isActivityInParty(4):
                    insidePartiesMenuStructure.extend([5316, 5317])
                if isActivityInParty(5):
                    insidePartiesMenuStructure.append(5318)
                if isActivityInParty(6):
                    insidePartiesMenuStructure.extend([5319, 5320])
                if len(base.distributedParty.partyInfo.decors):
                    insidePartiesMenuStructure.append(5321)
                    if isDecorInParty(3):
                        insidePartiesMenuStructure.append(5322)
            menu.rebuildFromStructure(insidePartiesMenuStructure)
            self.insidePartiesMenu = SCMenuHolder(OTPLocalizer.SCMenuParties, menu=menu)
            self.speedChat[2:2] = [self.insidePartiesMenu]
        return

    def removeInsidePartiesMenu(self):
        if self.insidePartiesMenu:
            i = self.speedChat.index(self.insidePartiesMenu)
            del self.speedChat[i]
            self.insidePartiesMenu.destroy()
            self.insidePartiesMenu = None
        return

    def addGolfMenu(self):
        if self.golfMenu == None:
            menu = TTSCGolfMenu()
            self.golfMenu = SCMenuHolder(OTPLocalizer.SCMenuGolf, menu=menu)
            self.speedChat[2:2] = [self.golfMenu]
        return

    def removeGolfMenu(self):
        if self.golfMenu:
            i = self.speedChat.index(self.golfMenu)
            del self.speedChat[i]
            self.golfMenu.destroy()
            self.golfMenu = None
        return

    def addBoardingGroupMenu(self, zoneId):
        if self.boardingGroupMenu == None:
            menu = TTSCBoardingMenu(zoneId)
            self.boardingGroupMenu = SCMenuHolder(OTPLocalizer.SCMenuBoardingGroup, menu=menu)
            self.speedChat[2:2] = [self.boardingGroupMenu]
        return

    def removeBoardingGroupMenu(self):
        if self.boardingGroupMenu:
            i = self.speedChat.index(self.boardingGroupMenu)
            del self.speedChat[i]
            self.boardingGroupMenu.destroy()
            self.boardingGroupMenu = None
        return

    def addSingingGroupMenu(self):
        if self.singingGroupMenu == None:
            menu = TTSCSingingMenu()
            self.singingGroupMenu = SCMenuHolder(OTPLocalizer.SCMenuSingingGroup, menu=menu)
            self.speedChat[2:2] = [self.singingGroupMenu]
        return

    def removeSingingMenu(self):
        if self.singingGroupMenu:
            i = self.speedChat.index(self.singingGroupMenu)
            del self.speedChat[i]
            self.singingGroupMenu.destroy()
            self.singingGroupMenu = None
        return

    def addAprilToonsMenu(self):
        if self.aprilToonsMenu == None:
            menu = TTSCAprilToonsMenu()
            self.aprilToonsMenu = SCMenuHolder(OTPLocalizer.SCMenuAprilToons, menu=menu)
            self.speedChat[3:3] = [self.aprilToonsMenu]
        return

    def removeAprilToonsMenu(self):
        if self.aprilToonsMenu:
            i = self.speedChat.index(self.aprilToonsMenu)
            del self.speedChat[i]
            self.aprilToonsMenu.destroy()
            self.aprilToonsMenu = None
        return

    def addSillyPhaseOneMenu(self):
        if self.sillyPhaseOneMenu == None:
            menu = TTSCSillyPhaseOneMenu()
            self.sillyPhaseOneMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu=menu)
            self.speedChat[3:3] = [self.sillyPhaseOneMenu]
        return

    def removeSillyPhaseOneMenu(self):
        if self.sillyPhaseOneMenu:
            i = self.speedChat.index(self.sillyPhaseOneMenu)
            del self.speedChat[i]
            self.sillyPhaseOneMenu.destroy()
            self.sillyPhaseOneMenu = None
        return

    def addSillyPhaseTwoMenu(self):
        if self.sillyPhaseTwoMenu == None:
            menu = TTSCSillyPhaseTwoMenu()
            self.sillyPhaseTwoMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu=menu)
            self.speedChat[3:3] = [self.sillyPhaseTwoMenu]
        return

    def removeSillyPhaseTwoMenu(self):
        if self.sillyPhaseTwoMenu:
            i = self.speedChat.index(self.sillyPhaseTwoMenu)
            del self.speedChat[i]
            self.sillyPhaseTwoMenu.destroy()
            self.sillyPhaseTwoMenu = None
        return

    def addSillyPhaseThreeMenu(self):
        if self.sillyPhaseThreeMenu == None:
            menu = TTSCSillyPhaseThreeMenu()
            self.sillyPhaseThreeMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu=menu)
            self.speedChat[3:3] = [self.sillyPhaseThreeMenu]
        return

    def removeSillyPhaseThreeMenu(self):
        if self.sillyPhaseThreeMenu:
            i = self.speedChat.index(self.sillyPhaseThreeMenu)
            del self.speedChat[i]
            self.sillyPhaseThreeMenu.destroy()
            self.sillyPhaseThreeMenu = None
        return

    def addSillyPhaseFourMenu(self):
        if self.sillyPhaseFourMenu == None:
            menu = TTSCSillyPhaseFourMenu()
            self.sillyPhaseFourMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu=menu)
            self.speedChat[3:3] = [self.sillyPhaseFourMenu]
        return

    def removeSillyPhaseFourMenu(self):
        if self.sillyPhaseFourMenu:
            i = self.speedChat.index(self.sillyPhaseFourMenu)
            del self.speedChat[i]
            self.sillyPhaseFourMenu.destroy()
            self.sillyPhaseFourMenu = None
        return

    def addSillyPhaseFiveMenu(self):
        if self.sillyPhaseFiveMenu == None:
            menu = TTSCSillyPhaseFiveMenu()
            self.sillyPhaseFiveMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu=menu)
            self.speedChat[3:3] = [self.sillyPhaseFiveMenu]
        return

    def removeSillyPhaseFiveMenu(self):
        if self.sillyPhaseFiveMenu:
            i = self.speedChat.index(self.sillyPhaseFiveMenu)
            del self.speedChat[i]
            self.sillyPhaseFiveMenu.destroy()
            self.sillyPhaseFiveMenu = None
        return

    def addVictoryPartiesMenu(self):
        if self.victoryPartiesMenu == None:
            menu = TTSCVictoryPartiesMenu()
            self.victoryPartiesMenu = SCMenuHolder(OTPLocalizer.SCMenuVictoryParties, menu=menu)
            self.speedChat[3:3] = [self.victoryPartiesMenu]
        return

    def removeVictoryPartiesMenu(self):
        if self.victoryPartiesMenu:
            i = self.speedChat.index(self.victoryPartiesMenu)
            del self.speedChat[i]
            self.victoryPartiesMenu.destroy()
            self.victoryPartiesMenu = None
        return

    def addSellbotNerfMenu(self):
        if self.sellbotNerfMenu == None:
            menu = TTSCSellbotNerfMenu()
            self.sellbotNerfMenu = SCMenuHolder(OTPLocalizer.SCMenuSellbotNerf, menu=menu)
            self.speedChat[2:2] = [self.sellbotNerfMenu]
        return

    def removeSellbotNerfMenu(self):
        if self.sellbotNerfMenu:
            i = self.speedChat.index(self.sellbotNerfMenu)
            del self.speedChat[i]
            self.sellbotNerfMenu.destroy()
            self.sellbotNerfMenu = None
        return

    def addJellybeanJamMenu(self, phase):
        if self.jellybeanJamMenu == None:
            menu = TTSCJellybeanJamMenu(phase)
            self.jellybeanJamMenu = SCMenuHolder(OTPLocalizer.SCMenuJellybeanJam, menu=menu)
            self.speedChat[2:2] = [self.jellybeanJamMenu]
        return

    def removeJellybeanJamMenu(self):
        if self.jellybeanJamMenu:
            i = self.speedChat.index(self.jellybeanJamMenu)
            del self.speedChat[i]
            self.jellybeanJamMenu.destroy()
            self.jellybeanJamMenu = None
        return

    def addHalloweenMenu(self):
        if self.halloweenMenu == None:
            menu = TTSCHalloweenMenu()
            self.halloweenMenu = SCMenuHolder(OTPLocalizer.SCMenuHalloween, menu=menu)
            self.speedChat[2:2] = [self.halloweenMenu]
        return

    def removeHalloweenMenu(self):
        if self.halloweenMenu:
            i = self.speedChat.index(self.halloweenMenu)
            del self.speedChat[i]
            self.halloweenMenu.destroy()
            self.halloweenMenu = None
        return

    def addWinterMenu(self, carol = False):
        if self.winterMenu == None:
            menu = TTSCWinterMenu(carol)
            self.winterMenu = SCMenuHolder(OTPLocalizer.SCMenuWinter, menu=menu)
            self.speedChat[2:2] = [self.winterMenu]
        return

    def removeWinterMenu(self):
        if self.winterMenu:
            i = self.speedChat.index(self.winterMenu)
            del self.speedChat[i]
            self.winterMenu.destroy()
            self.winterMenu = None
        return

    def addCarolMenu(self):
        self.removeWinterMenu()
        self.addWinterMenu(carol=True)

    def removeCarolMenu(self):
        pass

    def addWhiteList(self):
        if self.whiteList == None:
            from toontown.chat.TTSCWhiteListTerminal import TTSCWhiteListTerminal
            self.whiteList = TTSCWhiteListTerminal(4, self)
            self.speedChat[1:1] = [self.whiteList]
        return

    def removeWhiteList(self):
        if self.whiteList:
            i = self.speedChat.index(self.whiteList)
            del self.speedChat[i]
            self.whiteList.destroy()
            self.whiteList = None
        return

    def addSellbotInvasionMenu(self):
        if self.sellbotInvasionMenu == None:
            menu = TTSCSellbotInvasionMenu()
            self.sellbotInvasionMenu = SCMenuHolder(OTPLocalizer.SCMenuSellbotInvasion, menu=menu)
            self.speedChat[2:2] = [self.sellbotInvasionMenu]
        return

    def removeSellbotInvasionMenu(self):
        if self.sellbotInvasionMenu:
            i = self.speedChat.index(self.sellbotInvasionMenu)
            del self.speedChat[i]
            self.sellbotInvasionMenu.destroy()
            self.sellbotInvasionMenu = None
        return

    def addSellbotFieldOfficeMenu(self):
        if self.sellbotFieldOfficeMenu == None:
            menu = TTSCSellbotFieldOfficeMenu()
            self.sellbotFieldOfficeMenu = SCMenuHolder(OTPLocalizer.SCMenuFieldOffice, menu=menu)
            self.speedChat[2:2] = [self.sellbotFieldOfficeMenu]
        return

    def removeSellbotFieldOfficeMenu(self):
        if self.sellbotFieldOfficeMenu:
            i = self.speedChat.index(self.sellbotFieldOfficeMenu)
            del self.speedChat[i]
            self.sellbotFieldOfficeMenu.destroy()
            self.sellbotFieldOfficeMenu = None
        return

    def addIdesOfMarchMenu(self):
        if self.idesOfMarchMenu == None:
            menu = TTSCIdesOfMarchMenu()
            self.idesOfMarchMenu = SCMenuHolder(OTPLocalizer.SCMenuIdesOfMarch, menu=menu)
            self.speedChat[2:2] = [self.idesOfMarchMenu]
        return

    def removeIdesOfMarchMenu(self):
        if self.idesOfMarchMenu:
            i = self.speedChat.index(self.idesOfMarchMenu)
            del self.speedChat[i]
            self.idesOfMarchMenu.destroy()
            self.idesOfMarchMenu = None
        return
