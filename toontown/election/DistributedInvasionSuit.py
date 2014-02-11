from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from toontown.suit.DistributedSuitBase import DistributedSuitBase
import SafezoneInvasionGlobals
from InvasionSuitBase import InvasionSuitBase

class DistributedInvasionSuit(DistributedSuitBase, InvasionSuitBase, FSM):
    def __init__(self, cr):
        DistributedSuitBase.__init__(self, cr)
        InvasionSuitBase.__init__(self)
        FSM.__init__(self, 'InvasionSuitFSM')

        self.spawnPointId = 0
        self.moveTask = None

        self._stateTimestamp = 0
        self._lerpTimestamp = 0
        self._turnInterval = None

    def delete(self):
        DistributedSuitBase.delete(self)
        self.stopMoveTask()

    def setSpawnPoint(self, spawnPointId):
        self.spawnPointId = spawnPointId
        x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.freezeLerp(x, y)
        self.setPos(x, y, z)
        self.setH(h)

    def setState(self, state, timestamp):
        self._stateTimestamp = timestamp
        self.__applyLerpPosition()
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def enterFlyDown(self, time):
        x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.loop('neutral', 0)
        self.mtrack = self.beginSupaFlyMove(Point3(x, y, z), 1, 'fromSky')
        self.mtrack.start(time)

    def exitFlyDown(self):
        self.mtrack.finish()
        del self.mtrack
        self.detachPropeller()

    def enterIdle(self, time):
        self.loop('neutral', 0)

    def enterMarch(self, time):
        self.loop('walk', 0)
        self.startMoveTask()

    def setMarchLerp(self, x1, y1, x2, y2, timestamp):
        self.setLerpPoints(x1, y1, x2, y2)
        self._lerpTimestamp = timestamp

        # Also turn to our new ideal "H":
        if self._turnInterval:
            self._turnInterval.finish()
        q = Quat()
        q.setHpr((self._idealH, 0, 0))
        self._turnInterval = self.quatInterval(0.1, q, blendType='easeOut')
        self._turnInterval.start()

        self.__applyLerpPosition()

    def __applyLerpPosition(self):
        lerpStartedAgo = globalClockDelta.localElapsedTime(self._lerpTimestamp)
        stateStartedAgo = globalClockDelta.localElapsedTime(self._stateTimestamp)

        if lerpStartedAgo > stateStartedAgo:
            self.__setPositionAt(lerpStartedAgo - stateStartedAgo)

    def exitMarch(self):
        self.loop('neutral', 0)
        self.stopMoveTask()

        if self._turnInterval:
            self._turnInterval.finish()

    def startMoveTask(self):
        if self.moveTask:
            return
        self.moveTask = taskMgr.add(self.__move, self.uniqueName('move-task'))

    def stopMoveTask(self):
        if self.moveTask:
            self.moveTask.remove()
            self.moveTask = None

    def __move(self, task):
        self.__setPositionAt(globalClockDelta.localElapsedTime(self._lerpTimestamp))
        return task.cont

    def __setPositionAt(self, t):
        x, y = self.getPosAt(t)
        self.setX(x)
        self.setY(y)

        # We need to pin ourselves to the ground. I'm lazy so I'll just keep
        # putting the suit on top of the shadow.
        self.setZ(self.shadowPlacer.shadowNodePath, 0.025)
