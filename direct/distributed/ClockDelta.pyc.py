# 2013.08.22 22:14:00 Pacific Daylight Time
# Embedded file name: direct.distributed.ClockDelta
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
import math
NetworkTimeBits = 16
NetworkTimePrecision = 100.0
NetworkTimeMask = (1 << NetworkTimeBits) - 1
NetworkTimeSignedMask = NetworkTimeMask >> 1
NetworkTimeTopBits = 32 - NetworkTimeBits
MaxTimeDelta = NetworkTimeSignedMask / NetworkTimePrecision
ClockDriftPerHour = 1.0
ClockDriftPerSecond = ClockDriftPerHour / 3600.0
P2PResyncDelay = 10.0

class ClockDelta(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ClockDelta')

    def __init__(self):
        self.globalClock = ClockObject.getGlobalClock()
        self.delta = 0
        self.uncertainty = None
        self.lastResync = 0.0
        self.accept('resetClock', self.__resetClock)
        return

    def getDelta(self):
        return self.delta

    def getUncertainty(self):
        if self.uncertainty == None:
            return
        now = self.globalClock.getRealTime()
        elapsed = now - self.lastResync
        return self.uncertainty + elapsed * ClockDriftPerSecond

    def getLastResync(self):
        return self.lastResync

    def __resetClock(self, timeDelta):
        self.delta += timeDelta

    def clear(self):
        self.delta = 0
        self.uncertainty = None
        self.lastResync = 0.0
        return

    def resynchronize(self, localTime, networkTime, newUncertainty, trustNew = 1):
        newDelta = float(localTime) - float(networkTime) / NetworkTimePrecision
        self.newDelta(localTime, newDelta, newUncertainty, trustNew=trustNew)

    def peerToPeerResync(self, avId, timestamp, serverTime, uncertainty):
        now = self.globalClock.getRealTime()
        if now - self.lastResync < P2PResyncDelay:
            return -1
        local = self.networkToLocalTime(timestamp, now)
        elapsed = now - local
        delta = (local + now) / 2.0 - serverTime
        gotSync = 0
        if elapsed <= 0 or elapsed > P2PResyncDelay:
            self.notify.info('Ignoring old request for resync from %s.' % avId)
        else:
            self.notify.info('Got sync +/- %.3f s, elapsed %.3f s, from %s.' % (uncertainty, elapsed, avId))
            delta -= elapsed / 2.0
            uncertainty += elapsed / 2.0
            gotSync = self.newDelta(local, delta, uncertainty, trustNew=0)
        return gotSync

    def newDelta(self, localTime, newDelta, newUncertainty, trustNew = 1):
        oldUncertainty = self.getUncertainty()
        if oldUncertainty != None:
            self.notify.info('previous delta at %.3f s, +/- %.3f s.' % (self.delta, oldUncertainty))
            self.notify.info('new delta at %.3f s, +/- %.3f s.' % (newDelta, newUncertainty))
            oldLow = self.delta - oldUncertainty
            oldHigh = self.delta + oldUncertainty
            newLow = newDelta - newUncertainty
            newHigh = newDelta + newUncertainty
            low = max(oldLow, newLow)
            high = min(oldHigh, newHigh)
            if low > high:
                if not trustNew:
                    self.notify.info('discarding new delta.')
                    return 0
                self.notify.info('discarding previous delta.')
            else:
                newDelta = (low + high) / 2.0
                newUncertainty = (high - low) / 2.0
                self.notify.info('intersection at %.3f s, +/- %.3f s.' % (newDelta, newUncertainty))
        self.delta = newDelta
        self.uncertainty = newUncertainty
        self.lastResync = localTime
        return 1

    def networkToLocalTime(self, networkTime, now = None, bits = 16, ticksPerSec = NetworkTimePrecision):
        if now == None:
            now = self.globalClock.getRealTime()
        if self.globalClock.getMode() == ClockObject.MNonRealTime and base.config.GetBool('movie-network-time', False):
            return now
        ntime = int(math.floor((now - self.delta) * ticksPerSec + 0.5))
        if bits == 16:
            diff = self.__signExtend(networkTime - ntime)
        else:
            diff = networkTime - ntime
        return now + float(diff) / ticksPerSec

    def localToNetworkTime(self, localTime, bits = 16, ticksPerSec = NetworkTimePrecision):
        ntime = int(math.floor((localTime - self.delta) * ticksPerSec + 0.5))
        if bits == 16:
            return self.__signExtend(ntime)
        else:
            return ntime

    def getRealNetworkTime(self, bits = 16, ticksPerSec = NetworkTimePrecision):
        return self.localToNetworkTime(self.globalClock.getRealTime(), bits=bits, ticksPerSec=ticksPerSec)

    def getFrameNetworkTime(self, bits = 16, ticksPerSec = NetworkTimePrecision):
        return self.localToNetworkTime(self.globalClock.getFrameTime(), bits=bits, ticksPerSec=ticksPerSec)

    def localElapsedTime(self, networkTime, bits = 16, ticksPerSec = NetworkTimePrecision):
        now = self.globalClock.getFrameTime()
        dt = now - self.networkToLocalTime(networkTime, now, bits=bits, ticksPerSec=ticksPerSec)
        return max(dt, 0.0)

    def __signExtend(self, networkTime):
        r = (networkTime + 32768 & NetworkTimeMask) - 32768
        return r


globalClockDelta = ClockDelta()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\ClockDelta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:00 Pacific Daylight Time
