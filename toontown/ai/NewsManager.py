from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import SuitBattleGlobals
from toontown.toonbase import TTLocalizer
import HolidayDecorator
import HalloweenHolidayDecorator
import CrashedLeaderBoardDecorator
from direct.interval.IntervalGlobal import *
import calendar
from copy import deepcopy
from toontown.speedchat import TTSCJellybeanJamMenu
decorationHolidays = [ToontownGlobals.WINTER_DECORATIONS,
 ToontownGlobals.WACKY_WINTER_DECORATIONS,
 ToontownGlobals.HALLOWEEN_PROPS,
 ToontownGlobals.SPOOKY_PROPS,
 ToontownGlobals.HALLOWEEN_COSTUMES,
 ToontownGlobals.SPOOKY_COSTUMES,
 ToontownGlobals.CRASHED_LEADERBOARD]
promotionalSpeedChatHolidays = [ToontownGlobals.ELECTION_PROMOTION]

class NewsManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManager')
    neverDisable = 1
    YearlyHolidayType = 1
    OncelyHolidayType = 2
    RelativelyHolidayType = 3
    OncelyMultipleStartHolidayType = 4

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.population = 0
        self.invading = 0
        self.decorationHolidayIds = []
        self.holidayDecorator = None
        self.holidayIdList = []
        base.cr.newsManager = self
        base.localAvatar.inventory.setInvasionCreditMultiplier(1)
        self.weeklyCalendarHolidays = []
        return

    def delete(self):
        self.cr.newsManager = None
        if self.holidayDecorator:
            self.holidayDecorator.exit()
        DistributedObject.DistributedObject.delete(self)
        return

    def setPopulation(self, population):
        self.population = population
        messenger.send('newPopulation', [population])

    def getPopulation(self):
        return population

    def sendSystemMessage(self, message, style):
        base.localAvatar.setSystemMessage(style, message)

    def setInvasionStatus(self, msgType, cogType, numRemaining, skeleton):
        self.notify.info('setInvasionStatus: msgType: %s cogType: %s, numRemaining: %s, skeleton: %s' % (msgType,
         cogType,
         numRemaining,
         skeleton))
        cogName = SuitBattleGlobals.SuitAttributes[cogType]['name']
        cogNameP = SuitBattleGlobals.SuitAttributes[cogType]['pluralname']
        if skeleton:
            cogName = TTLocalizer.Skeleton
            cogNameP = TTLocalizer.SkeletonP
        if msgType == ToontownGlobals.SuitInvasionBegin:
            msg1 = TTLocalizer.SuitInvasionBegin1
            msg2 = TTLocalizer.SuitInvasionBegin2 % cogNameP
            self.invading = 1
        elif msgType == ToontownGlobals.SuitInvasionUpdate:
            msg1 = TTLocalizer.SuitInvasionUpdate1 % numRemaining
            msg2 = TTLocalizer.SuitInvasionUpdate2 % cogNameP
            self.invading = 1
        elif msgType == ToontownGlobals.SuitInvasionEnd:
            msg1 = TTLocalizer.SuitInvasionEnd1 % cogName
            msg2 = TTLocalizer.SuitInvasionEnd2
            self.invading = 0
        elif msgType == ToontownGlobals.SuitInvasionBulletin:
            msg1 = TTLocalizer.SuitInvasionBulletin1
            msg2 = TTLocalizer.SuitInvasionBulletin2 % cogNameP
            self.invading = 1
        else:
            self.notify.warning('setInvasionStatus: invalid msgType: %s' % msgType)
            return
        if self.invading:
            mult = ToontownBattleGlobals.getInvasionMultiplier()
        else:
            mult = 1
        base.localAvatar.inventory.setInvasionCreditMultiplier(mult)
        Sequence(Wait(1.0), Func(base.localAvatar.setSystemMessage, 0, msg1), Wait(5.0), Func(base.localAvatar.setSystemMessage, 0, msg2), name='newsManagerWait', autoPause=1).start()

    def getInvading(self):
        return self.invading

    def startHoliday(self, holidayId):
        if holidayId not in self.holidayIdList:
            self.notify.info('setHolidayId: Starting Holiday %s' % holidayId)
            self.holidayIdList.append(holidayId)
            if holidayId in decorationHolidays:
                self.decorationHolidayIds.append(holidayId)
                if holidayId == ToontownGlobals.HALLOWEEN_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addHalloweenMenu()
                        self.setHalloweenPropsHolidayStart()
                elif holidayId == ToontownGlobals.SPOOKY_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addHalloweenMenu()
                        self.setSpookyPropsHolidayStart()
                elif holidayId == ToontownGlobals.WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addWinterMenu()
                        self.setWinterDecorationsStart()
                elif holidayId == ToontownGlobals.WACKY_WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.addWinterMenu()
                        self.setWackyWinterDecorationsStart()
                if hasattr(base.cr.playGame, 'dnaStore') and hasattr(base.cr.playGame, 'hood') and hasattr(base.cr.playGame.hood, 'loader'):
                    if holidayId == ToontownGlobals.HALLOWEEN_COSTUMES or holidayId == ToontownGlobals.SPOOKY_COSTUMES:
                        self.holidayDecorator = HalloweenHolidayDecorator.HalloweenHolidayDecorator()
                    elif holidayId == ToontownGlobals.CRASHED_LEADERBOARD:
                        self.holidayDecorator = CrashedLeaderBoardDecorator.CrashedLeaderBoardDecorator()
                    else:
                        self.holidayDecorator = HolidayDecorator.HolidayDecorator()
                    self.holidayDecorator.decorate()
                    messenger.send('decorator-holiday-%d-starting' % holidayId)
            elif holidayId in promotionalSpeedChatHolidays:
                if hasattr(base, 'TTSCPromotionalMenu'):
                    base.TTSCPromotionalMenu.startHoliday(holidayId)
            elif holidayId == ToontownGlobals.MORE_XP_HOLIDAY:
                self.setMoreXpHolidayStart()
            elif holidayId == ToontownGlobals.JELLYBEAN_DAY:
                pass
            elif holidayId == ToontownGlobals.CIRCUIT_RACING_EVENT:
                self.setGrandPrixWeekendStart()
            elif holidayId == ToontownGlobals.HYDRANT_ZERO_HOLIDAY:
                self.setHydrantZeroHolidayStart()
            elif holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addAprilToonsMenu()
            elif holidayId == ToontownGlobals.WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addCarolMenu()
                    self.setWinterCarolingStart()
            elif holidayId == ToontownGlobals.WACKY_WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addCarolMenu()
            elif holidayId == ToontownGlobals.VALENTINES_DAY:
                messenger.send('ValentinesDayStart')
                base.localAvatar.setSystemMessage(0, TTLocalizer.ValentinesDayStart)
            elif holidayId == ToontownGlobals.SILLY_CHATTER_ONE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseOneMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_TWO:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseTwoMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_THREE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseThreeMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FOUR:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseFourMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FIVE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseFiveMenu()
            elif holidayId == ToontownGlobals.VICTORY_PARTY_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addVictoryPartiesMenu()
            elif holidayId == ToontownGlobals.SELLBOT_NERF_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSellbotNerfHolidayStart()
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSellbotNerfMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addJellybeanJamMenu(TTSCJellybeanJamMenu.JellybeanJamPhases.TROLLEY)
            elif holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addJellybeanJamMenu(TTSCJellybeanJamMenu.JellybeanJamPhases.FISHING)
            elif holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setJellybeanPartiesHolidayStart()
            elif holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setJellybeanMonthHolidayStart()
            elif holidayId == ToontownGlobals.BANK_UPGRADE_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setBankUpgradeHolidayStart()
            elif holidayId == ToontownGlobals.BLACK_CAT_DAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setBlackCatHolidayStart()
            elif holidayId == ToontownGlobals.SPOOKY_BLACK_CAT:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSpookyBlackCatHolidayStart()
            elif holidayId == ToontownGlobals.TOP_TOONS_MARATHON:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setTopToonsMarathonStart()
            elif holidayId == ToontownGlobals.SELLBOT_INVASION:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSellbotInvasionMenu()
            elif holidayId == ToontownGlobals.SELLBOT_FIELD_OFFICE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSellbotFieldOfficeMenu()
            elif holidayId == ToontownGlobals.IDES_OF_MARCH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setIdesOfMarchStart()
                    base.localAvatar.chatMgr.chatInputSpeedChat.addIdesOfMarchMenu()
            elif holidayId == ToontownGlobals.EXPANDED_CLOSETS:
                self.setExpandedClosetsStart()
            elif holidayId == ToontownGlobals.KARTING_TICKETS_HOLIDAY:
                self.setKartingTicketsHolidayStart()

    def endHoliday(self, holidayId):
        if holidayId in self.holidayIdList:
            self.notify.info('setHolidayId: Ending Holiday %s' % holidayId)
            self.holidayIdList.remove(holidayId)
            if holidayId in self.decorationHolidayIds:
                self.decorationHolidayIds.remove(holidayId)
                if holidayId == ToontownGlobals.HALLOWEEN_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeHalloweenMenu()
                        self.setHalloweenPropsHolidayEnd()
                elif holidayId == ToontownGlobals.SPOOKY_PROPS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeHalloweenMenu()
                        self.setSpookyPropsHolidayEnd()
                elif holidayId == ToontownGlobals.WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeWinterMenu()
                        self.setWinterDecorationsEnd()
                elif holidayId == ToontownGlobals.WACKY_WINTER_DECORATIONS:
                    if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                        base.localAvatar.chatMgr.chatInputSpeedChat.removeWinterMenu()
                if hasattr(base.cr.playGame, 'dnaStore') and hasattr(base.cr.playGame, 'hood') and hasattr(base.cr.playGame.hood, 'loader'):
                    if holidayId == ToontownGlobals.HALLOWEEN_COSTUMES or holidayId == ToontownGlobals.SPOOKY_COSTUMES:
                        self.holidayDecorator = HalloweenHolidayDecorator.HalloweenHolidayDecorator()
                    elif holidayId == ToontownGlobals.CRASHED_LEADERBOARD:
                        self.holidayDecorator = CrashedLeaderBoardDecorator.CrashedLeaderBoardDecorator()
                    else:
                        self.holidayDecorator = HolidayDecorator.HolidayDecorator()
                    self.holidayDecorator.undecorate()
                    messenger.send('decorator-holiday-%d-ending' % holidayId)
            elif holidayId in promotionalSpeedChatHolidays:
                if hasattr(base, 'TTSCPromotionalMenu'):
                    base.TTSCPromotionalMenu.endHoliday(holidayId)
            elif holidayId == ToontownGlobals.MORE_XP_HOLIDAY:
                self.setMoreXpHolidayEnd()
            elif holidayId == ToontownGlobals.JELLYBEAN_DAY:
                pass
            elif holidayId == ToontownGlobals.CIRCUIT_RACING_EVENT:
                self.setGrandPrixWeekendEnd()
            elif holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeAprilToonsMenu()
            elif holidayId == ToontownGlobals.VALENTINES_DAY:
                messenger.send('ValentinesDayStop')
                base.localAvatar.setSystemMessage(0, TTLocalizer.ValentinesDayEnd)
            elif holidayId == ToontownGlobals.SILLY_CHATTER_ONE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseOneMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_TWO:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseTwoMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_THREE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseThreeMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FOUR:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseFourMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FIVE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseFiveMenu()
            elif holidayId == ToontownGlobals.VICTORY_PARTY_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeVictoryPartiesMenu()
            elif holidayId == ToontownGlobals.WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeCarolMenu()
            elif holidayId == ToontownGlobals.WACKY_WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeCarolMenu()
            elif holidayId == ToontownGlobals.SELLBOT_NERF_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSellbotNerfHolidayEnd()
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSellbotNerfMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_TROLLEY_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeJellybeanJamMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeJellybeanJamMenu()
            elif holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY or holidayId == ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY_MONTH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setJellybeanPartiesHolidayEnd()
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeJellybeanJamMenu()
            elif holidayId == ToontownGlobals.BLACK_CAT_DAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setBlackCatHolidayEnd()
            elif holidayId == ToontownGlobals.SPOOKY_BLACK_CAT:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setSpookyBlackCatHolidayEnd()
            elif holidayId == ToontownGlobals.TOP_TOONS_MARATHON:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    self.setTopToonsMarathonEnd()
            elif holidayId == ToontownGlobals.SELLBOT_INVASION:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSellbotInvasionMenu()
            elif holidayId == ToontownGlobals.SELLBOT_FIELD_OFFICE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSellbotFieldOfficeMenu()
            elif holidayId == ToontownGlobals.IDES_OF_MARCH:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeIdesOfMarchMenu()

    def setHolidayIdList(self, holidayIdList):

        def isEnding(id):
            return id not in holidayIdList

        def isStarting(id):
            return id not in self.holidayIdList

        toEnd = filter(isEnding, self.holidayIdList)
        for endingHolidayId in toEnd:
            self.endHoliday(endingHolidayId)

        toStart = filter(isStarting, holidayIdList)
        for startingHolidayId in toStart:
            self.startHoliday(startingHolidayId)

        messenger.send('setHolidayIdList', [holidayIdList])

    def getDecorationHolidayId(self):
        return self.decorationHolidayIds

    def getHolidayIdList(self):
        return self.holidayIdList

    def setBingoWin(self, zoneId):
        base.localAvatar.setSystemMessage(0, 'Bingo congrats!')

    def setBingoStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoStart)

    def setBingoOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoOngoing)

    def setBingoEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoEnd)

    def setCircuitRaceStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceStart)

    def setCircuitRaceOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceOngoing)

    def setCircuitRaceEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceEnd)

    def setTrolleyHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayStart)

    def setTrolleyHolidayOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayOngoing)

    def setTrolleyHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayEnd)

    def setTrolleyWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyWeekendStart)

    def setTrolleyWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyWeekendEnd)

    def setRoamingTrialerWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendStart)
        base.roamingTrialers = True

    def setRoamingTrialerWeekendOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendOngoing)
        base.roamingTrialers = True

    def setRoamingTrialerWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendEnd)
        base.roamingTrialers = False

    def setMoreXpHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayStart)

    def setMoreXpHolidayOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayOngoing)

    def setMoreXpHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayEnd)

    def setJellybeanDayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanDayHolidayStart)

    def setJellybeanDayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanDayHolidayEnd)

    def setGrandPrixWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GrandPrixWeekendHolidayStart)

    def setGrandPrixWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GrandPrixWeekendHolidayEnd)

    def setHydrantZeroHolidayStart(self):
        messenger.send('HydrantZeroIsRunning', [True])

    def setSellbotNerfHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SellbotNerfHolidayStart)

    def setSellbotNerfHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SellbotNerfHolidayEnd)

    def setJellybeanTrolleyHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanTrolleyHolidayStart)

    def setJellybeanTrolleyHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanTrolleyHolidayEnd)

    def setJellybeanFishingHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanFishingHolidayStart)

    def setJellybeanFishingHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanFishingHolidayEnd)

    def setJellybeanPartiesHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanPartiesHolidayStart)

    def setJellybeanMonthHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanMonthHolidayStart)

    def setJellybeanPartiesHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanPartiesHolidayEnd)

    def setBankUpgradeHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.BankUpgradeHolidayStart)

    def setHalloweenPropsHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.HalloweenPropsHolidayStart)

    def setHalloweenPropsHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.HalloweenPropsHolidayEnd)

    def setSpookyPropsHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SpookyPropsHolidayStart)

    def setSpookyPropsHolidayEnd(self):
        pass

    def setBlackCatHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.BlackCatHolidayStart)

    def setBlackCatHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.BlackCatHolidayEnd)

    def setSpookyBlackCatHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.SpookyBlackCatHolidayStart)
        for currToon in base.cr.toons.values():
            currToon.setDNA(currToon.style.clone())

    def setSpookyBlackCatHolidayEnd(self):
        for currToon in base.cr.toons.values():
            currToon.setDNA(currToon.style.clone())

    def setTopToonsMarathonStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TopToonsMarathonStart)

    def setTopToonsMarathonEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TopToonsMarathonEnd)

    def setWinterDecorationsStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WinterDecorationsStart)

    def setWinterDecorationsEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WinterDecorationsEnd)

    def setWackyWinterDecorationsStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WackyWinterDecorationsStart)

    def setWinterCarolingStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.WinterCarolingStart)

    def setExpandedClosetsStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.ExpandedClosetsStart)

    def setKartingTicketsHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.KartingTicketsHolidayStart)

    def setIdesOfMarchStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.IdesOfMarchStart)

    def holidayNotify(self):
        for id in self.holidayIdList:
            if id == 19:
                self.setBingoOngoing()
            elif id == 20:
                self.setCircuitRaceOngoing()
            elif id == 21:
                self.setTrolleyHolidayOngoing()
            elif id == 22:
                self.setRoamingTrialerWeekendOngoing()

    def setWeeklyCalendarHolidays(self, weeklyCalendarHolidays):
        self.weeklyCalendarHolidays = weeklyCalendarHolidays

    def getHolidaysForWeekday(self, day):
        result = []
        for item in self.weeklyCalendarHolidays:
            if item[1] == day:
                result.append(item[0])

        return result

    def setYearlyCalendarHolidays(self, yearlyCalendarHolidays):
        self.yearlyCalendarHolidays = yearlyCalendarHolidays

    def getYearlyHolidaysForDate(self, theDate):
        result = []
        for item in self.yearlyCalendarHolidays:
            if item[1][0] == theDate.month and item[1][1] == theDate.day:
                newItem = [self.YearlyHolidayType] + list(item)
                result.append(tuple(newItem))
                continue
            if item[2][0] == theDate.month and item[2][1] == theDate.day:
                newItem = [self.YearlyHolidayType] + list(item)
                result.append(tuple(newItem))

        return result

    def setMultipleStartHolidays(self, multipleStartHolidays):
        self.multipleStartHolidays = multipleStartHolidays

    def getMultipleStartHolidaysForDate(self, theDate):
        result = []
        for theHoliday in self.multipleStartHolidays:
            times = theHoliday[1:]
            tempTimes = times[0]
            for startAndStopTimes in tempTimes:
                startTime = startAndStopTimes[0]
                endTime = startAndStopTimes[1]
                if startTime[0] == theDate.year and startTime[1] == theDate.month and startTime[2] == theDate.day:
                    fakeOncelyHoliday = [theHoliday[0], startTime, endTime]
                    newItem = [self.OncelyMultipleStartHolidayType] + fakeOncelyHoliday
                    result.append(tuple(newItem))
                    continue
                if endTime[0] == theDate.year and endTime[1] == theDate.month and endTime[2] == theDate.day:
                    fakeOncelyHoliday = [theHoliday[0], startTime, endTime]
                    newItem = [self.OncelyMultipleStartHolidayType] + fakeOncelyHoliday
                    result.append(tuple(newItem))

        return result

    def setOncelyCalendarHolidays(self, oncelyCalendarHolidays):
        self.oncelyCalendarHolidays = oncelyCalendarHolidays

    def getOncelyHolidaysForDate(self, theDate):
        result = []
        for item in self.oncelyCalendarHolidays:
            if item[1][0] == theDate.year and item[1][1] == theDate.month and item[1][2] == theDate.day:
                newItem = [self.OncelyHolidayType] + list(item)
                result.append(tuple(newItem))
                continue
            if item[2][0] == theDate.year and item[2][1] == theDate.month and item[2][2] == theDate.day:
                newItem = [self.OncelyHolidayType] + list(item)
                result.append(tuple(newItem))

        return result

    def setRelativelyCalendarHolidays(self, relativelyCalendarHolidays):
        self.relativelyCalendarHolidays = relativelyCalendarHolidays

    def getRelativelyHolidaysForDate--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'result'

6	BUILD_LIST_0      None
9	LOAD_FAST         'self'
12	STORE_ATTR        'weekDaysInMonth'

15	LOAD_CONST        (28, 0)
18	LOAD_CONST        (29, 1)
21	LOAD_CONST        (30, 2)
24	LOAD_CONST        (31, 3)
27	BUILD_LIST_4      None
30	LOAD_FAST         'self'
33	STORE_ATTR        'numDaysCorMatrix'

36	SETUP_LOOP        '81'
39	LOAD_GLOBAL       'range'
42	LOAD_CONST        7
45	CALL_FUNCTION_1   None
48	GET_ITER          None
49	FOR_ITER          '80'
52	STORE_FAST        'i'

55	LOAD_FAST         'self'
58	LOAD_ATTR         'weekDaysInMonth'
61	LOAD_ATTR         'append'
64	LOAD_FAST         'i'
67	LOAD_CONST        4
70	BUILD_TUPLE_2     None
73	CALL_FUNCTION_1   None
76	POP_TOP           None
77	JUMP_BACK         '49'
80	POP_BLOCK         None
81_0	COME_FROM         '36'

81	SETUP_LOOP        '995'
84	LOAD_FAST         'self'
87	LOAD_ATTR         'relativelyCalendarHolidays'
90	GET_ITER          None
91	FOR_ITER          '994'
94	STORE_FAST        'holidayItem'

97	LOAD_GLOBAL       'deepcopy'
100	LOAD_FAST         'holidayItem'
103	CALL_FUNCTION_1   None
106	STORE_FAST        'item'

109	BUILD_LIST_0      None
112	STORE_FAST        'newItem'

115	LOAD_FAST         'newItem'
118	LOAD_ATTR         'append'
121	LOAD_FAST         'item'
124	LOAD_CONST        0
127	BINARY_SUBSCR     None
128	CALL_FUNCTION_1   None
131	POP_TOP           None

132	LOAD_CONST        1
135	STORE_FAST        'i'

138	SETUP_LOOP        '808'
141	LOAD_FAST         'i'
144	LOAD_GLOBAL       'len'
147	LOAD_FAST         'item'
150	CALL_FUNCTION_1   None
153	COMPARE_OP        '<'
156	JUMP_IF_FALSE     '807'

159	LOAD_FAST         'item'
162	LOAD_FAST         'i'
165	BINARY_SUBSCR     None
166	LOAD_CONST        1
169	BINARY_SUBSCR     None
170	STORE_FAST        'sRepNum'

173	LOAD_FAST         'item'
176	LOAD_FAST         'i'
179	BINARY_SUBSCR     None
180	LOAD_CONST        2
183	BINARY_SUBSCR     None
184	STORE_FAST        'sWeekday'

187	LOAD_FAST         'item'
190	LOAD_FAST         'i'
193	LOAD_CONST        1
196	BINARY_ADD        None
197	BINARY_SUBSCR     None
198	LOAD_CONST        2
201	BINARY_SUBSCR     None
202	STORE_FAST        'eWeekday'

205	SETUP_LOOP        '658'

208	LOAD_FAST         'item'
211	LOAD_FAST         'i'
214	LOAD_CONST        1
217	BINARY_ADD        None
218	BINARY_SUBSCR     None
219	LOAD_CONST        1
222	BINARY_SUBSCR     None
223	STORE_FAST        'eRepNum'

226	LOAD_FAST         'self'
229	LOAD_ATTR         'initRepMatrix'
232	LOAD_FAST         'theDate'
235	LOAD_ATTR         'year'
238	LOAD_FAST         'item'
241	LOAD_FAST         'i'
244	BINARY_SUBSCR     None
245	LOAD_CONST        0
248	BINARY_SUBSCR     None
249	CALL_FUNCTION_2   None
252	POP_TOP           None

253	SETUP_LOOP        '293'
256	LOAD_FAST         'self'
259	LOAD_ATTR         'weekDaysInMonth'
262	LOAD_FAST         'sWeekday'
265	BINARY_SUBSCR     None
266	LOAD_CONST        1
269	BINARY_SUBSCR     None
270	LOAD_FAST         'sRepNum'
273	COMPARE_OP        '<'
276	JUMP_IF_FALSE     '292'

279	LOAD_FAST         'sRepNum'
282	LOAD_CONST        1
285	INPLACE_SUBTRACT  None
286	STORE_FAST        'sRepNum'
289	JUMP_BACK         '256'
292	POP_BLOCK         None
293_0	COME_FROM         '253'

293	LOAD_FAST         'self'
296	LOAD_ATTR         'dayForWeekday'
299	LOAD_FAST         'theDate'
302	LOAD_ATTR         'year'
305	LOAD_FAST         'item'
308	LOAD_FAST         'i'
311	BINARY_SUBSCR     None
312	LOAD_CONST        0
315	BINARY_SUBSCR     None
316	LOAD_FAST         'sWeekday'
319	LOAD_FAST         'sRepNum'
322	CALL_FUNCTION_4   None
325	STORE_FAST        'sDay'

328	LOAD_FAST         'self'
331	LOAD_ATTR         'initRepMatrix'
334	LOAD_FAST         'theDate'
337	LOAD_ATTR         'year'
340	LOAD_FAST         'item'
343	LOAD_FAST         'i'
346	LOAD_CONST        1
349	BINARY_ADD        None
350	BINARY_SUBSCR     None
351	LOAD_CONST        0
354	BINARY_SUBSCR     None
355	CALL_FUNCTION_2   None
358	POP_TOP           None

359	SETUP_LOOP        '399'
362	LOAD_FAST         'self'
365	LOAD_ATTR         'weekDaysInMonth'
368	LOAD_FAST         'eWeekday'
371	BINARY_SUBSCR     None
372	LOAD_CONST        1
375	BINARY_SUBSCR     None
376	LOAD_FAST         'eRepNum'
379	COMPARE_OP        '<'
382	JUMP_IF_FALSE     '398'

385	LOAD_FAST         'eRepNum'
388	LOAD_CONST        1
391	INPLACE_SUBTRACT  None
392	STORE_FAST        'eRepNum'
395	JUMP_BACK         '362'
398	POP_BLOCK         None
399_0	COME_FROM         '359'

399	LOAD_FAST         'self'
402	LOAD_ATTR         'dayForWeekday'
405	LOAD_FAST         'theDate'
408	LOAD_ATTR         'year'
411	LOAD_FAST         'item'
414	LOAD_FAST         'i'
417	LOAD_CONST        1
420	BINARY_ADD        None
421	BINARY_SUBSCR     None
422	LOAD_CONST        0
425	BINARY_SUBSCR     None
426	LOAD_FAST         'eWeekday'
429	LOAD_FAST         'eRepNum'
432	CALL_FUNCTION_4   None
435	STORE_FAST        'nDay'

438	LOAD_FAST         'nDay'
441	LOAD_FAST         'sDay'
444	COMPARE_OP        '>'
447	JUMP_IF_FALSE     '540'
450	LOAD_FAST         'item'
453	LOAD_FAST         'i'
456	LOAD_CONST        1
459	BINARY_ADD        None
460	BINARY_SUBSCR     None
461	LOAD_CONST        0
464	BINARY_SUBSCR     None
465	LOAD_FAST         'item'
468	LOAD_FAST         'i'
471	BINARY_SUBSCR     None
472	LOAD_CONST        0
475	BINARY_SUBSCR     None
476	COMPARE_OP        '=='
479	JUMP_IF_FALSE     '540'
482	LOAD_FAST         'item'
485	LOAD_FAST         'i'
488	LOAD_CONST        1
491	BINARY_ADD        None
492	BINARY_SUBSCR     None
493	LOAD_CONST        1
496	BINARY_SUBSCR     None
497	LOAD_FAST         'item'
500	LOAD_FAST         'i'
503	BINARY_SUBSCR     None
504	LOAD_CONST        1
507	BINARY_SUBSCR     None
508	BINARY_SUBTRACT   None
509	LOAD_FAST         'nDay'
512	LOAD_FAST         'sDay'
515	BINARY_SUBTRACT   None
516	LOAD_GLOBAL       'abs'
519	LOAD_FAST         'eWeekday'
522	LOAD_FAST         'sWeekday'
525	BINARY_SUBTRACT   None
526	CALL_FUNCTION_1   None
529	BINARY_ADD        None
530	LOAD_CONST        7
533	BINARY_DIVIDE     None
534	COMPARE_OP        '<='
537_0	COME_FROM         '447'
537_1	COME_FROM         '479'
537	JUMP_IF_TRUE      '572'
540	LOAD_FAST         'item'
543	LOAD_FAST         'i'
546	LOAD_CONST        1
549	BINARY_ADD        None
550	BINARY_SUBSCR     None
551	LOAD_CONST        0
554	BINARY_SUBSCR     None
555	LOAD_FAST         'item'
558	LOAD_FAST         'i'
561	BINARY_SUBSCR     None
562	LOAD_CONST        0
565	BINARY_SUBSCR     None
566	COMPARE_OP        '!='
569_0	COME_FROM         '537'
569	JUMP_IF_FALSE     '576'

572	BREAK_LOOP        None
573	JUMP_FORWARD      '576'
576_0	COME_FROM         '573'

576	LOAD_FAST         'self'
579	LOAD_ATTR         'weekDaysInMonth'
582	LOAD_FAST         'eWeekday'
585	BINARY_SUBSCR     None
586	LOAD_CONST        1
589	BINARY_SUBSCR     None
590	LOAD_FAST         'eRepNum'
593	COMPARE_OP        '>'
596	JUMP_IF_FALSE     '612'

599	LOAD_FAST         'eRepNum'
602	LOAD_CONST        1
605	INPLACE_ADD       None
606	STORE_FAST        'eRepNum'
609	JUMP_BACK         '208'

612	LOAD_FAST         'item'
615	LOAD_FAST         'i'
618	LOAD_CONST        1
621	BINARY_ADD        None
622	BINARY_SUBSCR     None
623	LOAD_CONST        0
626	DUP_TOPX_2        None
629	BINARY_SUBSCR     None
630	LOAD_CONST        1
633	INPLACE_ADD       None
634	ROT_THREE         None
635	STORE_SUBSCR      None

636	LOAD_CONST        1
639	LOAD_FAST         'item'
642	LOAD_FAST         'i'
645	LOAD_CONST        1
648	BINARY_ADD        None
649	BINARY_SUBSCR     None
650	LOAD_CONST        1
653	STORE_SUBSCR      None
654	JUMP_BACK         '208'
657	POP_BLOCK         None
658_0	COME_FROM         '205'

658	LOAD_FAST         'newItem'
661	LOAD_ATTR         'append'
664	LOAD_FAST         'item'
667	LOAD_FAST         'i'
670	BINARY_SUBSCR     None
671	LOAD_CONST        0
674	BINARY_SUBSCR     None
675	LOAD_FAST         'sDay'
678	LOAD_FAST         'item'
681	LOAD_FAST         'i'
684	BINARY_SUBSCR     None
685	LOAD_CONST        3
688	BINARY_SUBSCR     None
689	LOAD_FAST         'item'
692	LOAD_FAST         'i'
695	BINARY_SUBSCR     None
696	LOAD_CONST        4
699	BINARY_SUBSCR     None
700	LOAD_FAST         'item'
703	LOAD_FAST         'i'
706	BINARY_SUBSCR     None
707	LOAD_CONST        5
710	BINARY_SUBSCR     None
711	BUILD_LIST_5      None
714	CALL_FUNCTION_1   None
717	POP_TOP           None

718	LOAD_FAST         'newItem'
721	LOAD_ATTR         'append'
724	LOAD_FAST         'item'
727	LOAD_FAST         'i'
730	LOAD_CONST        1
733	BINARY_ADD        None
734	BINARY_SUBSCR     None
735	LOAD_CONST        0
738	BINARY_SUBSCR     None
739	LOAD_FAST         'nDay'
742	LOAD_FAST         'item'
745	LOAD_FAST         'i'
748	LOAD_CONST        1
751	BINARY_ADD        None
752	BINARY_SUBSCR     None
753	LOAD_CONST        3
756	BINARY_SUBSCR     None
757	LOAD_FAST         'item'
760	LOAD_FAST         'i'
763	LOAD_CONST        1
766	BINARY_ADD        None
767	BINARY_SUBSCR     None
768	LOAD_CONST        4
771	BINARY_SUBSCR     None
772	LOAD_FAST         'item'
775	LOAD_FAST         'i'
778	LOAD_CONST        1
781	BINARY_ADD        None
782	BINARY_SUBSCR     None
783	LOAD_CONST        5
786	BINARY_SUBSCR     None
787	BUILD_LIST_5      None
790	CALL_FUNCTION_1   None
793	POP_TOP           None

794	LOAD_FAST         'i'
797	LOAD_CONST        2
800	INPLACE_ADD       None
801	STORE_FAST        'i'
804	JUMP_BACK         '141'
807	POP_BLOCK         None
808_0	COME_FROM         '138'

808	LOAD_FAST         'item'
811	LOAD_CONST        1
814	BINARY_SUBSCR     None
815	LOAD_CONST        0
818	BINARY_SUBSCR     None
819	LOAD_FAST         'theDate'
822	LOAD_ATTR         'month'
825	COMPARE_OP        '=='
828	JUMP_IF_FALSE     '901'
831	LOAD_FAST         'newItem'
834	LOAD_CONST        1
837	BINARY_SUBSCR     None
838	LOAD_CONST        1
841	BINARY_SUBSCR     None
842	LOAD_FAST         'theDate'
845	LOAD_ATTR         'day'
848	COMPARE_OP        '=='
851_0	COME_FROM         '828'
851	JUMP_IF_FALSE     '901'

854	LOAD_FAST         'self'
857	LOAD_ATTR         'RelativelyHolidayType'
860	BUILD_LIST_1      None
863	LOAD_GLOBAL       'list'
866	LOAD_FAST         'newItem'
869	CALL_FUNCTION_1   None
872	BINARY_ADD        None
873	STORE_FAST        'nItem'

876	LOAD_FAST         'result'
879	LOAD_ATTR         'append'
882	LOAD_GLOBAL       'tuple'
885	LOAD_FAST         'nItem'
888	CALL_FUNCTION_1   None
891	CALL_FUNCTION_1   None
894	POP_TOP           None

895	CONTINUE          '91'
898	JUMP_FORWARD      '901'
901_0	COME_FROM         '898'

901	LOAD_FAST         'item'
904	LOAD_CONST        2
907	BINARY_SUBSCR     None
908	LOAD_CONST        0
911	BINARY_SUBSCR     None
912	LOAD_FAST         'theDate'
915	LOAD_ATTR         'month'
918	COMPARE_OP        '=='
921	JUMP_IF_FALSE     '991'
924	LOAD_FAST         'newItem'
927	LOAD_CONST        2
930	BINARY_SUBSCR     None
931	LOAD_CONST        1
934	BINARY_SUBSCR     None
935	LOAD_FAST         'theDate'
938	LOAD_ATTR         'day'
941	COMPARE_OP        '=='
944_0	COME_FROM         '921'
944	JUMP_IF_FALSE     '991'

947	LOAD_FAST         'self'
950	LOAD_ATTR         'RelativelyHolidayType'
953	BUILD_LIST_1      None
956	LOAD_GLOBAL       'list'
959	LOAD_FAST         'newItem'
962	CALL_FUNCTION_1   None
965	BINARY_ADD        None
966	STORE_FAST        'nItem'

969	LOAD_FAST         'result'
972	LOAD_ATTR         'append'
975	LOAD_GLOBAL       'tuple'
978	LOAD_FAST         'nItem'
981	CALL_FUNCTION_1   None
984	CALL_FUNCTION_1   None
987	POP_TOP           None
988	JUMP_BACK         '91'
991	JUMP_BACK         '91'
994	POP_BLOCK         None
995_0	COME_FROM         '81'

995	LOAD_FAST         'result'
998	RETURN_VALUE      
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\ai\NewsManager.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'result'

6	BUILD_LIST_0      None
9	LOAD_FAST         'self'
12	STORE_ATTR        'weekDaysInMonth'

15	LOAD_CONST        (28, 0)
18	LOAD_CONST        (29, 1)
21	LOAD_CONST        (30, 2)
24	LOAD_CONST        (31, 3)
27	BUILD_LIST_4      None
30	LOAD_FAST         'self'
33	STORE_ATTR        'numDaysCorMatrix'

36	SETUP_LOOP        '81'
39	LOAD_GLOBAL       'range'
42	LOAD_CONST        7
45	CALL_FUNCTION_1   None
48	GET_ITER          None
49	FOR_ITER          '80'
52	STORE_FAST        'i'

55	LOAD_FAST         'self'
58	LOAD_ATTR         'weekDaysInMonth'
61	LOAD_ATTR         'append'
64	LOAD_FAST         'i'
67	LOAD_CONST        4
70	BUILD_TUPLE_2     None
73	CALL_FUNCTION_1   None
76	POP_TOP           None
77	JUMP_BACK         '49'
80	POP_BLOCK         None
81_0	COME_FROM         '36'

81	SETUP_LOOP        '995'
84	LOAD_FAST         'self'
87	LOAD_ATTR         'relativelyCalendarHolidays'
90	GET_ITER          None
91	FOR_ITER          '994'
94	STORE_FAST        'holidayItem'

97	LOAD_GLOBAL       'deepcopy'
100	LOAD_FAST         'holidayItem'
103	CALL_FUNCTION_1   None
106	STORE_FAST        'item'

109	BUILD_LIST_0      None
112	STORE_FAST        'newItem'

115	LOAD_FAST         'newItem'
118	LOAD_ATTR         'append'
121	LOAD_FAST         'item'
124	LOAD_CONST        0
127	BINARY_SUBSCR     None
128	CALL_FUNCTION_1   None
131	POP_TOP           None

132	LOAD_CONST        1
135	STORE_FAST        'i'

138	SETUP_LOOP        '808'
141	LOAD_FAST         'i'
144	LOAD_GLOBAL       'len'
147	LOAD_FAST         'item'
150	CALL_FUNCTION_1   None
153	COMPARE_OP        '<'
156	JUMP_IF_FALSE     '807'

159	LOAD_FAST         'item'
162	LOAD_FAST         'i'
165	BINARY_SUBSCR     None
166	LOAD_CONST        1
169	BINARY_SUBSCR     None
170	STORE_FAST        'sRepNum'

173	LOAD_FAST         'item'
176	LOAD_FAST         'i'
179	BINARY_SUBSCR     None
180	LOAD_CONST        2
183	BINARY_SUBSCR     None
184	STORE_FAST        'sWeekday'

187	LOAD_FAST         'item'
190	LOAD_FAST         'i'
193	LOAD_CONST        1
196	BINARY_ADD        None
197	BINARY_SUBSCR     None
198	LOAD_CONST        2
201	BINARY_SUBSCR     None
202	STORE_FAST        'eWeekday'

205	SETUP_LOOP        '658'

208	LOAD_FAST         'item'
211	LOAD_FAST         'i'
214	LOAD_CONST        1
217	BINARY_ADD        None
218	BINARY_SUBSCR     None
219	LOAD_CONST        1
222	BINARY_SUBSCR     None
223	STORE_FAST        'eRepNum'

226	LOAD_FAST         'self'
229	LOAD_ATTR         'initRepMatrix'
232	LOAD_FAST         'theDate'
235	LOAD_ATTR         'year'
238	LOAD_FAST         'item'
241	LOAD_FAST         'i'
244	BINARY_SUBSCR     None
245	LOAD_CONST        0
248	BINARY_SUBSCR     None
249	CALL_FUNCTION_2   None
252	POP_TOP           None

253	SETUP_LOOP        '293'
256	LOAD_FAST         'self'
259	LOAD_ATTR         'weekDaysInMonth'
262	LOAD_FAST         'sWeekday'
265	BINARY_SUBSCR     None
266	LOAD_CONST        1
269	BINARY_SUBSCR     None
270	LOAD_FAST         'sRepNum'
273	COMPARE_OP        '<'
276	JUMP_IF_FALSE     '292'

279	LOAD_FAST         'sRepNum'
282	LOAD_CONST        1
285	INPLACE_SUBTRACT  None
286	STORE_FAST        'sRepNum'
289	JUMP_BACK         '256'
292	POP_BLOCK         None
293_0	COME_FROM         '253'

293	LOAD_FAST         'self'
296	LOAD_ATTR         'dayForWeekday'
299	LOAD_FAST         'theDate'
302	LOAD_ATTR         'year'
305	LOAD_FAST         'item'
308	LOAD_FAST         'i'
311	BINARY_SUBSCR     None
312	LOAD_CONST        0
315	BINARY_SUBSCR     None
316	LOAD_FAST         'sWeekday'
319	LOAD_FAST         'sRepNum'
322	CALL_FUNCTION_4   None
325	STORE_FAST        'sDay'

328	LOAD_FAST         'self'
331	LOAD_ATTR         'initRepMatrix'
334	LOAD_FAST         'theDate'
337	LOAD_ATTR         'year'
340	LOAD_FAST         'item'
343	LOAD_FAST         'i'
346	LOAD_CONST        1
349	BINARY_ADD        None
350	BINARY_SUBSCR     None
351	LOAD_CONST        0
354	BINARY_SUBSCR     None
355	CALL_FUNCTION_2   None
358	POP_TOP           None

359	SETUP_LOOP        '399'
362	LOAD_FAST         'self'
365	LOAD_ATTR         'weekDaysInMonth'
368	LOAD_FAST         'eWeekday'
371	BINARY_SUBSCR     None
372	LOAD_CONST        1
375	BINARY_SUBSCR     None
376	LOAD_FAST         'eRepNum'
379	COMPARE_OP        '<'
382	JUMP_IF_FALSE     '398'

385	LOAD_FAST         'eRepNum'
388	LOAD_CONST        1
391	INPLACE_SUBTRACT  None
392	STORE_FAST        'eRepNum'
395	JUMP_BACK         '362'
398	POP_BLOCK         None
399_0	COME_FROM         '359'

399	LOAD_FAST         'self'
402	LOAD_ATTR         'dayForWeekday'
405	LOAD_FAST         'theDate'
408	LOAD_ATTR         'year'
411	LOAD_FAST         'item'
414	LOAD_FAST         'i'
417	LOAD_CONST        1
420	BINARY_ADD        None
421	BINARY_SUBSCR     None
422	LOAD_CONST        0
425	BINARY_SUBSCR     None
426	LOAD_FAST         'eWeekday'
429	LOAD_FAST         'eRepNum'
432	CALL_FUNCTION_4   None
435	STORE_FAST        'nDay'

438	LOAD_FAST         'nDay'
441	LOAD_FAST         'sDay'
444	COMPARE_OP        '>'
447	JUMP_IF_FALSE     '540'
450	LOAD_FAST         'item'
453	LOAD_FAST         'i'
456	LOAD_CONST        1
459	BINARY_ADD        None
460	BINARY_SUBSCR     None
461	LOAD_CONST        0
464	BINARY_SUBSCR     None
465	LOAD_FAST         'item'
468	LOAD_FAST         'i'
471	BINARY_SUBSCR     None
472	LOAD_CONST        0
475	BINARY_SUBSCR     None
476	COMPARE_OP        '=='
479	JUMP_IF_FALSE     '540'
482	LOAD_FAST         'item'
485	LOAD_FAST         'i'
488	LOAD_CONST        1
491	BINARY_ADD        None
492	BINARY_SUBSCR     None
493	LOAD_CONST        1
496	BINARY_SUBSCR     None
497	LOAD_FAST         'item'
500	LOAD_FAST         'i'
503	BINARY_SUBSCR     None
504	LOAD_CONST        1
507	BINARY_SUBSCR     None
508	BINARY_SUBTRACT   None
509	LOAD_FAST         'nDay'
512	LOAD_FAST         'sDay'
515	BINARY_SUBTRACT   None
516	LOAD_GLOBAL       'abs'
519	LOAD_FAST         'eWeekday'
522	LOAD_FAST         'sWeekday'
525	BINARY_SUBTRACT   None
526	CALL_FUNCTION_1   None
529	BINARY_ADD        None
530	LOAD_CONST        7
533	BINARY_DIVIDE     None
534	COMPARE_OP        '<='
537_0	COME_FROM         '447'
537_1	COME_FROM         '479'
537	JUMP_IF_TRUE      '572'
540	LOAD_FAST         'item'
543	LOAD_FAST         'i'
546	LOAD_CONST        1
549	BINARY_ADD        None
550	BINARY_SUBSCR     None
551	LOAD_CONST        0
554	BINARY_SUBSCR     None
555	LOAD_FAST         'item'
558	LOAD_FAST         'i'
561	BINARY_SUBSCR     None
562	LOAD_CONST        0
565	BINARY_SUBSCR     None
566	COMPARE_OP        '!='
569_0	COME_FROM         '537'
569	JUMP_IF_FALSE     '576'

572	BREAK_LOOP        None
573	JUMP_FORWARD      '576'
576_0	COME_FROM         '573'

576	LOAD_FAST         'self'
579	LOAD_ATTR         'weekDaysInMonth'
582	LOAD_FAST         'eWeekday'
585	BINARY_SUBSCR     None
586	LOAD_CONST        1
589	BINARY_SUBSCR     None
590	LOAD_FAST         'eRepNum'
593	COMPARE_OP        '>'
596	JUMP_IF_FALSE     '612'

599	LOAD_FAST         'eRepNum'
602	LOAD_CONST        1
605	INPLACE_ADD       None
606	STORE_FAST        'eRepNum'
609	JUMP_BACK         '208'

612	LOAD_FAST         'item'
615	LOAD_FAST         'i'
618	LOAD_CONST        1
621	BINARY_ADD        None
622	BINARY_SUBSCR     None
623	LOAD_CONST        0
626	DUP_TOPX_2        None
629	BINARY_SUBSCR     None
630	LOAD_CONST        1
633	INPLACE_ADD       None
634	ROT_THREE         None
635	STORE_SUBSCR      None

636	LOAD_CONST        1
639	LOAD_FAST         'item'
642	LOAD_FAST         'i'
645	LOAD_CONST        1
648	BINARY_ADD        None
649	BINARY_SUBSCR     None
650	LOAD_CONST        1
653	STORE_SUBSCR      None
654	JUMP_BACK         '208'
657	POP_BLOCK         None
658_0	COME_FROM         '205'

658	LOAD_FAST         'newItem'
661	LOAD_ATTR         'append'
664	LOAD_FAST         'item'
667	LOAD_FAST         'i'
670	BINARY_SUBSCR     None
671	LOAD_CONST        0
674	BINARY_SUBSCR     None
675	LOAD_FAST         'sDay'
678	LOAD_FAST         'item'
681	LOAD_FAST         'i'
684	BINARY_SUBSCR     None
685	LOAD_CONST        3
688	BINARY_SUBSCR     None
689	LOAD_FAST         'item'
692	LOAD_FAST         'i'
695	BINARY_SUBSCR     None
696	LOAD_CONST        4
699	BINARY_SUBSCR     None
700	LOAD_FAST         'item'
703	LOAD_FAST         'i'
706	BINARY_SUBSCR     None
707	LOAD_CONST        5
710	BINARY_SUBSCR     None
711	BUILD_LIST_5      None
714	CALL_FUNCTION_1   None
717	POP_TOP           None

718	LOAD_FAST         'newItem'
721	LOAD_ATTR         'append'
724	LOAD_FAST         'item'
727	LOAD_FAST         'i'
730	LOAD_CONST        1
733	BINARY_ADD        None
734	BINARY_SUBSCR     None
735	LOAD_CONST        0
738	BINARY_SUBSCR     None
739	LOAD_FAST         'nDay'
742	LOAD_FAST         'item'
745	LOAD_FAST         'i'
748	LOAD_CONST        1
751	BINARY_ADD        None
752	BINARY_SUBSCR     None
753	LOAD_CONST        3
756	BINARY_SUBSCR     None
757	LOAD_FAST         'item'
760	LOAD_FAST         'i'
763	LOAD_CONST        1
766	BINARY_ADD        None
767	BINARY_SUBSCR     None
768	LOAD_CONST        4
771	BINARY_SUBSCR     None
772	LOAD_FAST         'item'
775	LOAD_FAST         'i'
778	LOAD_CONST        1
781	BINARY_ADD        None
782	BINARY_SUBSCR     None
783	LOAD_CONST        5
786	BINARY_SUBSCR     None
787	BUILD_LIST_5      None
790	CALL_FUNCTION_1   None
793	POP_TOP           None

794	LOAD_FAST         'i'
797	LOAD_CONST        2
800	INPLACE_ADD       None
801	STORE_FAST        'i'
804	JUMP_BACK         '141'
807	POP_BLOCK         None
808_0	COME_FROM         '138'

808	LOAD_FAST         'item'
811	LOAD_CONST        1
814	BINARY_SUBSCR     None
815	LOAD_CONST        0
818	BINARY_SUBSCR     None
819	LOAD_FAST         'theDate'
822	LOAD_ATTR         'month'
825	COMPARE_OP        '=='
828	JUMP_IF_FALSE     '901'
831	LOAD_FAST         'newItem'
834	LOAD_CONST        1
837	BINARY_SUBSCR     None
838	LOAD_CONST        1
841	BINARY_SUBSCR     None
842	LOAD_FAST         'theDate'
845	LOAD_ATTR         'day'
848	COMPARE_OP        '=='
851_0	COME_FROM         '828'
851	JUMP_IF_FALSE     '901'

854	LOAD_FAST         'self'
857	LOAD_ATTR         'RelativelyHolidayType'
860	BUILD_LIST_1      None
863	LOAD_GLOBAL       'list'
866	LOAD_FAST         'newItem'
869	CALL_FUNCTION_1   None
872	BINARY_ADD        None
873	STORE_FAST        'nItem'

876	LOAD_FAST         'result'
879	LOAD_ATTR         'append'
882	LOAD_GLOBAL       'tuple'
885	LOAD_FAST         'nItem'
888	CALL_FUNCTION_1   None
891	CALL_FUNCTION_1   None
894	POP_TOP           None

895	CONTINUE          '91'
898	JUMP_FORWARD      '901'
901_0	COME_FROM         '898'

901	LOAD_FAST         'item'
904	LOAD_CONST        2
907	BINARY_SUBSCR     None
908	LOAD_CONST        0
911	BINARY_SUBSCR     None
912	LOAD_FAST         'theDate'
915	LOAD_ATTR         'month'
918	COMPARE_OP        '=='
921	JUMP_IF_FALSE     '991'
924	LOAD_FAST         'newItem'
927	LOAD_CONST        2
930	BINARY_SUBSCR     None
931	LOAD_CONST        1
934	BINARY_SUBSCR     None
935	LOAD_FAST         'theDate'
938	LOAD_ATTR         'day'
941	COMPARE_OP        '=='
944_0	COME_FROM         '921'
944	JUMP_IF_FALSE     '991'

947	LOAD_FAST         'self'
950	LOAD_ATTR         'RelativelyHolidayType'
953	BUILD_LIST_1      None
956	LOAD_GLOBAL       'list'
959	LOAD_FAST         'newItem'
962	CALL_FUNCTION_1   None
965	BINARY_ADD        None
966	STORE_FAST        'nItem'

969	LOAD_FAST         'result'
972	LOAD_ATTR         'append'
975	LOAD_GLOBAL       'tuple'
978	LOAD_FAST         'nItem'
981	CALL_FUNCTION_1   None
984	CALL_FUNCTION_1   None
987	POP_TOP           None
988	JUMP_BACK         '91'
991	JUMP_BACK         '91'
994	POP_BLOCK         None
995_0	COME_FROM         '81'

995	LOAD_FAST         'result'
998	RETURN_VALUE      None
-None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 657

    def dayForWeekday(self, year, month, weekday, repNum):
        monthDays = calendar.monthcalendar(year, month)
        if monthDays[0][weekday] == 0:
            repNum += 1
        return monthDays[repNum - 1][weekday]

    def initRepMatrix(self, year, month):
        for i in range(7):
            self.weekDaysInMonth[i] = (i, 4)

        startingWeekDay, numDays = calendar.monthrange(year, month)
        if startingWeekDay > 6:
            import pdb
            pdb.set_trace()
        for i in range(4):
            if numDays == self.numDaysCorMatrix[i][0]:
                break

        for j in range(self.numDaysCorMatrix[i][1]):
            self.weekDaysInMonth[startingWeekDay] = (self.weekDaysInMonth[startingWeekDay][0], self.weekDaysInMonth[startingWeekDay][1] + 1)
            startingWeekDay = (startingWeekDay + 1) % 7

    def isHolidayRunning(self, holidayId):
        result = holidayId in self.holidayIdList
        return result
1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 657

