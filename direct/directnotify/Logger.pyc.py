# 2013.08.22 22:13:49 Pacific Daylight Time
# Embedded file name: direct.directnotify.Logger
import sys
import time
import math

class Logger():
    __module__ = __name__

    def __init__(self, fileName = 'log'):
        self.__timeStamp = 1
        self.__startTime = 0.0
        self.__logFile = None
        self.__logFileName = fileName
        return

    def setTimeStamp(self, bool):
        self.__timeStamp = bool

    def getTimeStamp(self):
        return self.__timeStamp

    def resetStartTime(self):
        self.__startTime = time.time()

    def log(self, entryString):
        if self.__logFile == None:
            self.__openLogFile()
        if self.__timeStamp:
            self.__logFile.write(self.__getTimeStamp())
        self.__logFile.write(entryString + '\n')
        return

    def __openLogFile(self):
        self.resetStartTime()
        t = time.localtime(self.__startTime)
        st = time.strftime('%m-%d-%Y-%H-%M-%S', t)
        logFileName = self.__logFileName + '.' + st
        self.__logFile = open(logFileName, 'w')

    def __closeLogFile(self):
        if self.__logFile != None:
            self.__logFile.close()
        return

    def __getTimeStamp(self):
        t = time.time()
        dt = t - self.__startTime
        if dt >= 86400:
            days = int(math.floor(dt / 86400))
            dt = dt % 86400
        else:
            days = 0
        if dt >= 3600:
            hours = int(math.floor(dt / 3600))
            dt = dt % 3600
        else:
            hours = 0
        if dt >= 60:
            minutes = int(math.floor(dt / 60))
            dt = dt % 60
        else:
            minutes = 0
        seconds = int(math.ceil(dt))
        return '%02d:%02d:%02d:%02d: ' % (days,
         hours,
         minutes,
         seconds)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directnotify\Logger.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:50 Pacific Daylight Time
