from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from toontown.suit.DistributedSuitBase import DistributedSuitBase
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals
from InvasionSuitBase import InvasionSuitBase

class DistributedInvasionSuit(DistributedSuitBase, InvasionSuitBase, FSM):
    def __init__(self, cr):
        DistributedSuitBase.__init__(self, cr)
        InvasionSuitBase.__init__(self)
        FSM.__init__(self, 'InvasionSuitFSM')

        self.spawnPointId = 0
        self.moveTask = None

        self._lerpTimestamp = 0
        self._turnInterval = None
        self._staticPoint = (0, 0, 0)

    def delete(self):
        self.demand('Off')

        self.stopMoveTask()
        DistributedSuitBase.delete(self)

    def announceGenerate(self):
        DistributedSuitBase.announceGenerate(self)
        self.corpMedallion.hide()
        self.healthBar.show()
        self.updateHealthBar(0, 1)

        # Set ourselves up for a good pieing:
        colNode = self.find('**/distAvatarCollNode*')
        colNode.setTag('pieCode', str(ToontownGlobals.PieCodeInvasionSuit))

    def setSpawnPoint(self, spawnPointId):
        self.spawnPointId = spawnPointId
        x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.freezeLerp(x, y)
        self.setPos(x, y, z)
        self.setH(h)

    def setHP(self, hp):
        currHP = getattr(self, 'currHP', 0)
        if currHP > hp:
            self.showHpText(hp - currHP)

        DistributedSuitBase.setHP(self, hp)

        self.updateHealthBar(0, 1)

    def setState(self, state, timestamp):
        self.request(state, globalClockDelta.localElapsedTime(timestamp))

    def setStaticPoint(self, x, y, h):
        self._staticPoint = (x, y, h)
        if self.state != 'March':
            self.__moveToStaticPoint()

    def __moveToStaticPoint(self):
        x, y, h = self._staticPoint
        self.setX(x)
        self.setY(y)

        if self._turnInterval:
            self._turnInterval.finish()
        q = Quat()
        q.setHpr((h, 0, 0))
        self._turnInterval = self.quatInterval(0.1, q, blendType='easeOut')
        self._turnInterval.start()

        # And set the Z properly:
        self.__placeOnGround()

    def enterFlyDown(self, time):
        x, y, z, h = SafezoneInvasionGlobals.SuitSpawnPoints[self.spawnPointId]
        self.loop('neutral', 0)
        self.mtrack = self.beginSupaFlyMove(Point3(x, y, z), 1, 'fromSky',
                                            walkAfterLanding=False)
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

    def enterExplode(self, time):
        loseActor = self.getLoseActor()
        loseActor.reparentTo(render)
        self.stash()

        # TODO: This animation is incomplete. There's no sound, particles, or
        # proper clipping at the end.
        self._explosionInterval = ActorInterval(loseActor, 'lose')
        self._explosionInterval.start(time)

    def exitExplode(self):
        self._explosionInterval.finish()
        self.cleanupLoseActor()

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

    def exitMarch(self):
        self.loop('neutral', 0)
        self.stopMoveTask()

        self.__moveToStaticPoint()

    def startMoveTask(self):
        if self.moveTask:
            return
        self.moveTask = taskMgr.add(self.__move, self.uniqueName('move-task'))

    def stopMoveTask(self):
        if self.moveTask:
            self.moveTask.remove()
            self.moveTask = None

    def __move(self, task):
        x, y = self.getPosAt(globalClockDelta.localElapsedTime(self._lerpTimestamp))
        self.setX(x)
        self.setY(y)

        self.__placeOnGround()

        return task.cont

    def __placeOnGround(self):
        # This schedules a task to fire after the shadow-culling to place the
        # suit directly on his shadow.
        taskMgr.add(self.__placeOnGroundTask, self.uniqueName('place-on-ground'), sort=31)

    def __placeOnGroundTask(self, task):
        if getattr(self, 'shadowPlacer', None) and \
           getattr(self.shadowPlacer, 'shadowNodePath', None):
            self.setZ(self.shadowPlacer.shadowNodePath, 0.025)
        return task.done
