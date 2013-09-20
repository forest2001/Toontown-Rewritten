# 2013.08.22 22:21:04 Pacific Daylight Time
# Embedded file name: toontown.login.TTDateObject
import DateObject

class TTDateObject(DateObject.DateObject):
    __module__ = __name__

    def __init__(self, accountServerDate):
        self.accountServerDate = accountServerDate

    def getYear(self):
        return self.accountServerDate.getYear()

    def getMonth(self):
        return self.accountServerDate.getMonth()

    def getDay(self):
        return self.accountServerDate.getDay()

    def getDetailedAge(self, dobMonth, dobYear, dobDay = None, curMonth = None, curYear = None, curDay = None):
        return DateObject.DateObject.getDetailedAge(self, dobMonth, dobYear, dobDay, curMonth=self.getMonth(), curYear=self.getYear(), curDay=self.getDay())

    def getAge(self, dobMonth, dobYear, dobDay = None, curMonth = None, curYear = None, curDay = None):
        return TTDateObject.getDetailedAge(self, dobMonth, dobYear, dobDay=dobDay, curMonth=curMonth, curYear=curYear, curDay=curDay)[0]
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\login\TTDateObject.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:21:04 Pacific Daylight Time
