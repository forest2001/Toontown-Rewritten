# 2013.08.22 22:14:06 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedSmoothNode
from pandac.PandaModules import *
from ClockDelta import *
import DistributedNode
import DistributedSmoothNodeBase
from direct.task.Task import cont
MaxFuture = base.config.GetFloat('smooth-max-future', 0.2)
MinSuggestResync = base.config.GetFloat('smooth-min-suggest-resync', 15)
EnableSmoothing = base.config.GetBool('smooth-enable-smoothing', 1)
EnablePrediction = base.config.GetBool('smooth-enable-prediction', 1)
Lag = base.config.GetDouble('smooth-lag', 0.2)
PredictionLag = base.config.GetDouble('smooth-prediction-lag', 0.0)
GlobalSmoothing = 0
GlobalPrediction = 0

def globalActivateSmoothing(smoothing, prediction):
    global GlobalPrediction
    global GlobalSmoothing
    GlobalSmoothing = smoothing
    GlobalPrediction = prediction
    for obj in base.cr.getAllOfType(DistributedSmoothNode):
        obj.activateSmoothing(smoothing, prediction)


activateSmoothing = globalActivateSmoothing

class DistributedSmoothNode(DistributedNode.DistributedNode, DistributedSmoothNodeBase.DistributedSmoothNodeBase):
    __module__ = __name__

    def __init__(self, cr):
        try:
            self.DistributedSmoothNode_initialized
        except:
            self.DistributedSmoothNode_initialized = 1
            DistributedNode.DistributedNode.__init__(self, cr)
            DistributedSmoothNodeBase.DistributedSmoothNodeBase.__init__(self)
            self.smoothStarted = 0
            self.localControl = False
            self.stopped = False

    def generate(self):
        self.smoother = SmoothMover()
        self.smoothStarted = 0
        self.lastSuggestResync = 0
        self._smoothWrtReparents = False
        DistributedNode.DistributedNode.generate(self)
        DistributedSmoothNodeBase.DistributedSmoothNodeBase.generate(self)
        self.cnode.setRepository(self.cr, 0, 0)
        self.activateSmoothing(GlobalSmoothing, GlobalPrediction)
        self.stopped = False

    def disable(self):
        DistributedSmoothNodeBase.DistributedSmoothNodeBase.disable(self)
        DistributedNode.DistributedNode.disable(self)
        del self.smoother

    def delete(self):
        DistributedSmoothNodeBase.DistributedSmoothNodeBase.delete(self)
        DistributedNode.DistributedNode.delete(self)

    def smoothPosition(self):
        self.smoother.computeAndApplySmoothPosHpr(self, self)

    def doSmoothTask(self, task):
        self.smoothPosition()
        return cont

    def wantsSmoothing(self):
        return 1

    def startSmooth(self):
        if not self.wantsSmoothing() or self.isDisabled() or self.isLocal():
            return
        if not self.smoothStarted:
            taskName = self.taskName('smooth')
            taskMgr.remove(taskName)
            self.reloadPosition()
            taskMgr.add(self.doSmoothTask, taskName)
            self.smoothStarted = 1

    def stopSmooth(self):
        if self.smoothStarted:
            taskName = self.taskName('smooth')
            taskMgr.remove(taskName)
            self.forceToTruePosition()
            self.smoothStarted = 0

    def setSmoothWrtReparents(self, flag):
        self._smoothWrtReparents = flag

    def getSmoothWrtReparents(self):
        return self._smoothWrtReparents

    def forceToTruePosition(self):
        if not self.isLocal() and self.smoother.getLatestPosition():
            self.smoother.applySmoothPosHpr(self, self)
        self.smoother.clearPositions(1)

    def reloadPosition(self):
        self.smoother.clearPositions(0)
        self.smoother.setPosHpr(self.getPos(), self.getHpr())
        self.smoother.setPhonyTimestamp()
        self.smoother.markPosition()

    def _checkResume(self, timestamp):
        if self.stopped:
            currTime = globalClock.getFrameTime()
            now = currTime - self.smoother.getExpectedBroadcastPeriod()
            last = self.smoother.getMostRecentTimestamp()
            if now > last:
                if timestamp == None:
                    local = 0.0
                else:
                    local = globalClockDelta.networkToLocalTime(timestamp, currTime)
                self.smoother.setPhonyTimestamp(local, True)
                self.smoother.markPosition()
        self.stopped = False
        return

    def setSmStop(self, timestamp = None):
        self.setComponentTLive(timestamp)
        self.stopped = True

    def setSmH(self, h, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentH(h)
        self.setComponentTLive(timestamp)

    def setSmZ(self, z, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentZ(z)
        self.setComponentTLive(timestamp)

    def setSmXY(self, x, y, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentX(x)
        self.setComponentY(y)
        self.setComponentTLive(timestamp)

    def setSmXZ(self, x, z, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentX(x)
        self.setComponentZ(z)
        self.setComponentTLive(timestamp)

    def setSmPos(self, x, y, z, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentX(x)
        self.setComponentY(y)
        self.setComponentZ(z)
        self.setComponentTLive(timestamp)

    def setSmHpr(self, h, p, r, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentH(h)
        self.setComponentP(p)
        self.setComponentR(r)
        self.setComponentTLive(timestamp)

    def setSmXYH(self, x, y, h, timestamp):
        self._checkResume(timestamp)
        self.setComponentX(x)
        self.setComponentY(y)
        self.setComponentH(h)
        self.setComponentTLive(timestamp)

    def setSmXYZH(self, x, y, z, h, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentX(x)
        self.setComponentY(y)
        self.setComponentZ(z)
        self.setComponentH(h)
        self.setComponentTLive(timestamp)

    def setSmPosHpr(self, x, y, z, h, p, r, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentX(x)
        self.setComponentY(y)
        self.setComponentZ(z)
        self.setComponentH(h)
        self.setComponentP(p)
        self.setComponentR(r)
        self.setComponentTLive(timestamp)

    def setSmPosHprL(self, l, x, y, z, h, p, r, timestamp = None):
        self._checkResume(timestamp)
        self.setComponentL(l)
        self.setComponentX(x)
        self.setComponentY(y)
        self.setComponentZ(z)
        self.setComponentH(h)
        self.setComponentP(p)
        self.setComponentR(r)
        self.setComponentTLive(timestamp)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentX(self, x):
        self.smoother.setX(x)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentY(self, y):
        self.smoother.setY(y)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentZ(self, z):
        self.smoother.setZ(z)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentH(self, h):
        self.smoother.setH(h)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentP(self, p):
        self.smoother.setP(p)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentR(self, r):
        self.smoother.setR(r)

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentL(self, l):
        if l != self.zoneId:
            pass

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentT(self, timestamp):
        self.smoother.setPhonyTimestamp()
        self.smoother.clearPositions(1)
        self.smoother.markPosition()
        self.forceToTruePosition()

    @report(types=['args'], dConfigParam='smoothnode')
    def setComponentTLive(self, timestamp):
        if timestamp is None:
            if self.smoother.hasMostRecentTimestamp():
                self.smoother.setTimestamp(self.smoother.getMostRecentTimestamp())
            else:
                self.smoother.setPhonyTimestamp()
            self.smoother.markPosition()
        else:
            now = globalClock.getFrameTime()
            local = globalClockDelta.networkToLocalTime(timestamp, now)
            realTime = globalClock.getRealTime()
            chug = realTime - now
            howFarFuture = local - now
            if howFarFuture - chug >= MaxFuture:
                if globalClockDelta.getUncertainty() != None and realTime - self.lastSuggestResync >= MinSuggestResync and hasattr(self.cr, 'localAvatarDoId'):
                    self.lastSuggestResync = realTime
                    timestampB = globalClockDelta.localToNetworkTime(realTime)
                    serverTime = realTime - globalClockDelta.getDelta()
                    self.d_suggestResync(self.cr.localAvatarDoId, timestamp, timestampB, serverTime, globalClockDelta.getUncertainty())
            self.smoother.setTimestamp(local)
            self.smoother.markPosition()
        if not self.localControl and not self.smoothStarted and self.smoother.getLatestPosition():
            self.smoother.applySmoothPosHpr(self, self)
        return

    def getComponentL(self):
        return self.zoneId

    def getComponentX(self):
        return self.getX()

    def getComponentY(self):
        return self.getY()

    def getComponentZ(self):
        return self.getZ()

    def getComponentH(self):
        return self.getH()

    def getComponentP(self):
        return self.getP()

    def getComponentR(self):
        return self.getR()

    def getComponentT(self):
        return 0

    @report(types=['args'], dConfigParam='smoothnode')
    def clearSmoothing(self, bogus = None):
        self.smoother.clearPositions(1)

    @report(types=['args'], dConfigParam='smoothnode')
    def wrtReparentTo(self, parent):
        if self.smoothStarted:
            if self._smoothWrtReparents:
                self.smoother.handleWrtReparent(self.getParent(), parent)
                NodePath.wrtReparentTo(self, parent)
            else:
                self.forceToTruePosition()
                NodePath.wrtReparentTo(self, parent)
                self.reloadPosition()
        else:
            NodePath.wrtReparentTo(self, parent)

    @report(types=['args'], dConfigParam='smoothnode')
    def d_setParent(self, parentToken):
        DistributedNode.DistributedNode.d_setParent(self, parentToken)
        self.forceToTruePosition()
        self.sendCurrentPosition()

    def d_suggestResync(self, avId, timestampA, timestampB, serverTime, uncertainty):
        serverTimeSec = math.floor(serverTime)
        serverTimeUSec = (serverTime - serverTimeSec) * 10000.0
        self.sendUpdate('suggestResync', [avId,
         timestampA,
         timestampB,
         serverTimeSec,
         serverTimeUSec,
         uncertainty])

    def suggestResync(self, avId, timestampA, timestampB, serverTimeSec, serverTimeUSec, uncertainty):
        serverTime = float(serverTimeSec) + float(serverTimeUSec) / 10000.0
        result = self.peerToPeerResync(avId, timestampA, serverTime, uncertainty)
        if result >= 0 and globalClockDelta.getUncertainty() != None:
            other = self.cr.doId2do.get(avId)
            if not other:
                pass
            elif hasattr(other, 'd_returnResync') and hasattr(self.cr, 'localAvatarDoId'):
                realTime = globalClock.getRealTime()
                serverTime = realTime - globalClockDelta.getDelta()
                other.d_returnResync(self.cr.localAvatarDoId, timestampB, serverTime, globalClockDelta.getUncertainty())
        return

    def d_returnResync(self, avId, timestampB, serverTime, uncertainty):
        serverTimeSec = math.floor(serverTime)
        serverTimeUSec = (serverTime - serverTimeSec) * 10000.0
        self.sendUpdate('returnResync', [avId,
         timestampB,
         serverTimeSec,
         serverTimeUSec,
         uncertainty])

    def returnResync(self, avId, timestampB, serverTimeSec, serverTimeUSec, uncertainty):
        serverTime = float(serverTimeSec) + float(serverTimeUSec) / 10000.0
        self.peerToPeerResync(avId, timestampB, serverTime, uncertainty)

    def peerToPeerResync(self, avId, timestamp, serverTime, uncertainty):
        gotSync = globalClockDelta.peerToPeerResync(avId, timestamp, serverTime, uncertainty)
        if not gotSync:
            if self.cr.timeManager != None:
                self.cr.timeManager.synchronize('suggested by %d' % avId)
        return gotSync

    def activateSmoothing(self, smoothing, prediction):
        if smoothing and EnableSmoothing:
            if prediction and EnablePrediction:
                self.smoother.setSmoothMode(SmoothMover.SMOn)
                self.smoother.setPredictionMode(SmoothMover.PMOn)
                self.smoother.setDelay(PredictionLag)
            else:
                self.smoother.setSmoothMode(SmoothMover.SMOn)
                self.smoother.setPredictionMode(SmoothMover.PMOff)
                self.smoother.setDelay(Lag)
        else:
            self.smoother.setSmoothMode(SmoothMover.SMOff)
            self.smoother.setPredictionMode(SmoothMover.PMOff)
            self.smoother.setDelay(0.0)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedSmoothNode.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:06 Pacific Daylight Time
