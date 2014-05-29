from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("NewsManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.accept('avatarEntered', self.__announceIfInvasion)

    def __announceIfInvasion(self, avatar):
        if self.air.suitInvasionManager.getInvading():
            self.sendUpdateToAvatarId(avatar.getDoId(), 'setInvasionStatus', [
                ToontownGlobals.SuitInvasionBulletin, self.air.suitInvasionManager.suitName,
                self.air.suitInvasionManager.numSuits, self.air.suitInvasionManager.specialSuit
            ])

    def setPopulation(self, todo0):
        pass

    def setBingoWin(self, todo0):
        pass

    def setBingoStart(self):
        pass

    def setBingoEnd(self):
        pass

    def setCircuitRaceStart(self):
        pass

    def setCircuitRaceEnd(self):
        pass

    def setTrolleyHolidayStart(self):
        pass

    def setTrolleyHolidayEnd(self):
        pass

    def setTrolleyWeekendStart(self):
        pass

    def setTrolleyWeekendEnd(self):
        pass

    def setRoamingTrialerWeekendStart(self):
        pass

    def setRoamingTrialerWeekendEnd(self):
        pass

    def setInvasionStatus(self, todo0, todo1, todo2, todo3):
        pass

    def setHolidayIdList(self, todo0):
        pass

    def holidayNotify(self):
        pass

    def setWeeklyCalendarHolidays(self, todo0):
        pass

    def getWeeklyCalendarHolidays(self):
        return []

    def setYearlyCalendarHolidays(self, todo0):
        pass

    def getYearlyCalendarHolidays(self):
        return []

    def setOncelyCalendarHolidays(self, todo0):
        pass

    def getOncelyCalendarHolidays(self):
        return []

    def setRelativelyCalendarHolidays(self, todo0):
        pass

    def getRelativelyCalendarHolidays(self):
        return []

    def setMultipleStartHolidays(self, todo0):
        pass

    def getMultipleStartHolidays(self):
        return []

    def sendSystemMessage(self, todo0, todo1):
        pass

