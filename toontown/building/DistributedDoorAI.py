from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task
from direct.fsm import ClassicFSM, State
from direct.distributed.ClockDelta import *
import DoorTypes

class DistributedDoorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDoorAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.state = 'closed'
        self.exitState = 'closed'
        self.zoneId = 0
        self.block = 0
        self.swing = 0
        self.DoorType = 0
        self.doorIndex = 0
        self.otherZoneId = 0
        self.otherDoId = 0
        self.fsm = ClassicFSM.ClassicFSM('DistributedDoor_right', [
         State.State('closing', self.enterClosing, self.exitClosing, ['closed', 'opening']),
         State.State('closed', self.enterClosed, self.exitClosed, ['opening']),
         State.State('opening', self.enterOpening, self.exitOpening, ['open']),
         State.State('open', self.enterOpen, self.exitOpen, ['closing', 'open'])], 'closed', 'closed')
        self.fsm.enterInitialState()
        self.exitDoorFSM = ClassicFSM.ClassicFSM('DistributedDoor_left', [
         State.State('closing', self.exitDoorEnterClosing, self.exitDoorExitClosing, ['closed', 'opening']),
         State.State('closed', self.exitDoorEnterClosed, self.exitDoorExitClosed, ['opening']),
         State.State('opening', self.exitDoorEnterOpening, self.exitDoorExitOpening, ['open']),
         State.State('open', self.exitDoorEnterOpen, self.exitDoorExitOpen, ['closing', 'open'])], 'closed', 'closed')
        self.exitDoorFSM.enterInitialState()

    def enterClosing(self):
        self.setState('closing')
        self.closingTask = taskMgr.doMethodLater(3, self.__close, 'doorClosingTask')

    def exitClosing(self):
        taskMgr.remove(self.closingTask)

    def enterClosed(self):
        self.setState('closed')

    def exitClosed(self):
        pass

    def enterOpening(self):
        self.setState('opening')
        self.openingTask = taskMgr.doMethodLater(2, self.__open, 'doorOpeningTask')

    def exitOpening(self):
        taskMgr.remove(self.openingTask)

    def enterOpen(self):
        self.setState('open')
        self.doClosingTask = taskMgr.doMethodLater(2, self.__doClosing, 'doorDoClosingTask')

    def exitOpen(self):
         taskMgr.remove(self.doClosingTask)

    def __close(self, task):
        self.fsm.request('closed')
        return task.done

    def __open(self, task):
        self.fsm.request('open')
        return task.done
    
    def __doClosing(self, task):
        self.fsm.request('closing')
        return task.done

    def exitDoorEnterClosing(self):
        self.setExitDoorState('closing')
        self.exitDoorClosingTask = taskMgr.doMethodLater(2, self.__exitDoorClose, 'doorClosingTask')

    def exitDoorExitClosing(self):
        taskMgr.remove(self.exitDoorClosingTask)

    def exitDoorEnterClosed(self):
        self.setExitDoorState('closed')

    def exitDoorExitClosed(self):
        pass

    def exitDoorEnterOpening(self):
        self.setExitDoorState('opening')
        self.exitDoorOpeningTask = taskMgr.doMethodLater(2, self.__exitDoorOpen, 'doorOpeningTask')

    def exitDoorExitOpening(self):
        taskMgr.remove(self.exitDoorOpeningTask)

    def exitDoorEnterOpen(self):
        self.setExitDoorState('open')
        self.exitDoorDoClosingTask = taskMgr.doMethodLater(2, self.__exitDoorDoClosing, 'doorDoClosingTask')

    def exitDoorExitOpen(self):
        taskMgr.remove(self.exitDoorDoClosingTask)

    def __exitDoorClose(self, task):
        self.exitDoorFSM.request('closed')
        return task.done

    def __exitDoorOpen(self, task):
        self.exitDoorFSM.request('open')
        return task.done

    def __exitDoorDoClosing(self, task):
        self.exitDoorFSM.request('closing')
        return task.done

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def getZoneIdAndBlock(self):
        return (self.zoneId, self.block)

    def setSwing(self, swing):
        self.swing = swing
        if hasattr(self, 'doId') and not self.doId is None:
            self.sendUpdate('setSwing', [self.leftSwing | (self.rightSwing<<1)])

    def getSwing(self):
        return self.swing

    def setDoorType(self, doorType):
        self.doorType = doorType

    def getDoorType(self):
        return self.doorType

    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex

    def getDoorIndex(self):
        return self.doorIndex

    def setOtherZoneIdAndDoId(self, zoneId, doId):
        self.otherZoneId = zoneId
        self.otherDoId = doId

    def getOtherZoneIdAndDoId(self):
        return (self.otherZoneId, self.otherDoId)

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        self.avatarEnter(avId)

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        self.avatarExit(avId)

    def rejectEnter(self, avId, reason):
        self.sendUpdateToAvatarId(avId, 'rejectEnter', [reason])

    def avatarEnter(self, avId):
        self.sendUpdate('avatarEnter', [avId])
        self.sendUpdateToAvatarId(avId, 'setOtherZoneIdAndDoId', [self.otherZoneId, self.otherDoId])
        self.fsm.request('opening')

    def avatarExit(self, avId):
        self.sendUpdate('avatarExit', [avId])
        self.exitDoorFSM.request('opening')

    def setState(self, state):
        self.state = state
        if hasattr(self, 'doId') and not self.doId is None:
            self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])
    
    def getState(self):
        return (self.state, 0)

    def setExitDoorState(self, state):
        self.exitState = state
        if hasattr(self, 'doId') and not self.doId is None:
            self.sendUpdate('setExitDoorState', [state, globalClockDelta.getRealNetworkTime()])

    def getExitDoorState(self):
        return (self.exitState, 0)
