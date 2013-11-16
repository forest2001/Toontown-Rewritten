from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State

class DistributedBoatAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBoatAI")
    PIER_TIME = 5.0
    TRAVEL_TIME = 20.0
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.state = ''
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.fsm = ClassicFSM.ClassicFSM('DistributedBoat', [
          State.State('DockedEast', self.enterDockedEast, self.exitDockedEast, ['SailingWest', 'SailingEast', 'DockedWest']),
          State.State('SailingWest', self.enterSailingWest, self.exitSailingWest, ['DockedWest', 'SailingEast', 'DockedEast']),
          State.State('DockedWest', self.enterDockedWest, self.exitDockedWest, ['SailingEast', 'SailingWest', 'DockedEast']),
          State.State('SailingEast', self.enterSailingEast, self.exitSailingEast, ['DockedEast', 'DockedWest', 'SailingWest'])
        ], 'DockedEast', 'DockedEast')
        self.fsm.enterInitialState()

    def enterDockedEast(self):
        self.setState('DockedEast')
        self.sailWestTask = taskMgr.doMethodLater(self.PIER_TIME, self.__sailWest, 'boatSailingTask')
    def exitDockedEast(self):
        taskMgr.remove(self.sailWestTask)
    def __sailWest(self, task):
        self.fsm.request('SailingWest')
        return task.done

    def enterSailingWest(self):
        self.setState('SailingWest')
        self.dockWestTask = taskMgr.doMethodLater(self.TRAVEL_TIME, self.__dockWest, 'boatDockingTask')
    def exitSailingWest(self):
        taskMgr.remove(self.dockWestTask)
    def __dockWest(self, task):
        self.fsm.request('DockedWest')
        return task.done

    def enterDockedWest(self):
        self.setState('DockedWest')
        self.sailEastTask = taskMgr.doMethodLater(self.PIER_TIME, self.__sailEast, 'boatSailingTask')
    def exitDockedWest(self):
        taskMgr.remove(self.sailEastTask)
    def __sailEast(self, task):
        self.fsm.request('SailingEast')
        return task.done

    def enterSailingEast(self):
        self.setState('SailingEast')
        self.dockEastTask = taskMgr.doMethodLater(self.TRAVEL_TIME, self.__dockEast, 'boatDockingTask')
    def exitSailingEast(self):
        taskMgr.remove(self.dockEastTask)
    def __dockEast(self, task):
        self.fsm.request('DockedEast')
        return task.done

    def setState(self, state):
        self.state = state
        self.stateTime = globalClockDelta.getRealNetworkTime()
        if hasattr(self, 'doId') and not self.doId is None:
            self.sendUpdate('setState', [self.state, self.stateTime])

    def getState(self):
        return (self.state, self.stateTime)
