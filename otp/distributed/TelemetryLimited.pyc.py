# 2013.08.22 22:15:20 Pacific Daylight Time
# Embedded file name: otp.distributed.TelemetryLimited


class TelemetryLimited():
    __module__ = __name__
    Sng = SerialNumGen()

    def __init__(self):
        self._telemetryLimiterId = self.Sng.next()
        self._limits = set()

    def getTelemetryLimiterId(self):
        return self._telemetryLimiterId

    def addTelemetryLimit(self, limit):
        self._limits.add(limit)

    def removeTelemetryLimit(self, limit):
        if limit in self._limits:
            self._limits.remove(limit)

    def enforceTelemetryLimits(self):
        for limit in self._limits:
            limit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\distributed\TelemetryLimited.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:20 Pacific Daylight Time
