import time
from datetime import datetime, timedelta, tzinfo
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

# This is a cheap implementation of US/Pacific time that only calculates
# correct DST for dates post-2006, because Toontown is far too silly a place
# to care about perfect DST.
class ToontownTimeZone(tzinfo):
    OFFSET = -8
    DST_BEGIN = datetime(1, 3, 8, 2) # DST begins on the second Sunday of March
    DST_END = datetime(1, 11, 1, 1) # ...and ends on the first Sunday of November
    NAMES = ('PST', 'PDT')

    @staticmethod
    def forward_to_sunday(dt):
        days_to_go = 6 - dt.weekday()
        if days_to_go:
            dt += timedelta(days_to_go)
        return dt

    def dst(self, dt):
        # Find out if DST is active for the dt.
        beginning = self.forward_to_sunday(self.DST_BEGIN.replace(year=dt.year))
        ending = self.forward_to_sunday(self.DST_END.replace(year=dt.year))

        if beginning <= dt.replace(tzinfo=None) < ending:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def utcoffset(self, dt):
        offset = timedelta(hours=self.OFFSET)
        offset += self.dst(dt)
        return offset
    
    def tzname(self, dt):
        standard_name, dst_name = self.NAMES
        if self.dst(dt):
            return dst_name
        else:
            return standard_name


# UTC is very simple, though:
class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

class ToontownTimeManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownTimeManager')
    ClockFormat = '%I:%M:%S %p'
    formatStr = '%Y-%m-%d %H:%M:%S'

    def __init__(self, serverTimeUponLogin = 0, clientTimeUponLogin = 0, globalClockRealTimeUponLogin = 0):
        self.serverTimeZone = ToontownTimeZone()
        self.updateLoginTimes(serverTimeUponLogin, clientTimeUponLogin, globalClockRealTimeUponLogin)
        self.debugSecondsAdded = 0

    def updateLoginTimes(self, serverTimeUponLogin, clientTimeUponLogin, globalClockRealTimeUponLogin):
        self.serverTimeUponLogin = serverTimeUponLogin
        self.clientTimeUponLogin = clientTimeUponLogin
        self.globalClockRealTimeUponLogin = globalClockRealTimeUponLogin
        naiveTime = datetime.utcfromtimestamp(self.serverTimeUponLogin)
        self.serverDateTime = datetime.fromtimestamp(self.serverTimeUponLogin, self.serverTimeZone)

    def getCurServerDateTime(self):
        secondsPassed = globalClock.getRealTime() - self.globalClockRealTimeUponLogin + self.debugSecondsAdded
        curDateTime = (self.serverDateTime + timedelta(seconds=secondsPassed)).astimezone(self.serverTimeZone)
        return curDateTime

    def getRelativeServerDateTime(self, timeOffset):
        secondsPassed = globalClock.getRealTime() - self.globalClockRealTimeUponLogin + self.debugSecondsAdded
        secondsPassed += timeOffset
        curDateTime = (self.serverDateTime + timedelta(seconds=secondsPassed)).astimezone(self.serverTimeZone)
        return curDateTime

    def getCurServerDateTimeForComparison(self):
        secondsPassed = globalClock.getRealTime() - self.globalClockRealTimeUponLogin + self.debugSecondsAdded
        curDateTime = self.serverDateTime + timedelta(seconds=secondsPassed)
        curDateTime = curDateTime.replace(tzinfo=self.serverTimeZone)
        return curDateTime

    def getCurServerTimeStr(self):
        curDateTime = self.getCurServerDateTime()
        result = curDateTime.strftime(self.ClockFormat)
        if result[0] == '0':
            result = result[1:]
        return result

    def setDebugSecondsAdded(self, moreSeconds):
        self.debugSecondsAdded = moreSeconds

    def debugTest(self):
        startTime = datetime.today()
        serverTzInfo = self.serverTimeZone
        startTime = startTime.replace(tzinfo=serverTzInfo)
        self.notify.info('startTime = %s' % startTime)
        serverTime = self.getCurServerDateTime()
        self.notify.info('serverTime = %s' % serverTime)
        result = startTime <= serverTime
        self.notify.info('start < serverTime %s' % result)
        startTime1MinAgo = startTime + timedelta(minutes=-1)
        self.notify.info('startTime1MinAgo = %s' % startTime1MinAgo)
        result2 = startTime1MinAgo <= serverTime
        self.notify.info('startTime1MinAgo < serverTime %s' % result2)
        serverTimeForComparison = self.getCurServerDateTimeForComparison()
        self.notify.info('serverTimeForComparison = %s' % serverTimeForComparison)
        result3 = startTime1MinAgo <= serverTimeForComparison
        self.notify.info('startTime1MinAgo < serverTimeForComparison %s' % result3)

    def convertStrToToontownTime(self, dateStr):
        curDateTime = self.getCurServerDateTime()
        try:
            curDateTime = datetime.fromtimestamp(time.mktime(time.strptime(dateStr, self.formatStr)), self.serverTimeZone)
        except:
            self.notify.warning('error parsing date string=%s' % dateStr)

        result = curDateTime
        return result

    def convertUtcStrToToontownTime(self, dateStr):
        curDateTime = self.getCurServerDateTime()
        try:
            timeTuple = time.strptime(dateStr, self.formatStr)
            utcDateTime = datetime(timeTuple[0], timeTuple[1], timeTuple[2], timeTuple[3], timeTuple[4], timeTuple[5], timeTuple[6], UTC())
            curDateTime = utcDateTime.astimezone(self.serverTimeZone)
        except:
            self.notify.warning('error parsing date string=%s' % dateStr)

        result = curDateTime
        return result
