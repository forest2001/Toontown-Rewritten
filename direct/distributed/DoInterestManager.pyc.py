# 2013.08.22 22:14:08 Pacific Daylight Time
# Embedded file name: direct.distributed.DoInterestManager
from pandac.PandaModules import *
from MsgTypes import *
from direct.showbase.PythonUtil import *
from direct.showbase import DirectObject
from PyDatagram import PyDatagram
from direct.directnotify.DirectNotifyGlobal import directNotify
import types
from direct.showbase.PythonUtil import report

class InterestState():
    __module__ = __name__
    StateActive = 'Active'
    StatePendingDel = 'PendingDel'

    def __init__(self, desc, state, context, event, parentId, zoneIdList, eventCounter, auto = False):
        self.desc = desc
        self.state = state
        self.context = context
        self.events = []
        self.eventCounter = eventCounter
        if event:
            self.addEvent(event)
        self.parentId = parentId
        self.zoneIdList = zoneIdList
        self.auto = auto

    def addEvent(self, event):
        self.events.append(event)
        self.eventCounter.num += 1

    def getEvents(self):
        return list(self.events)

    def clearEvents(self):
        self.eventCounter.num -= len(self.events)
        self.events = []

    def sendEvents(self):
        for event in self.events:
            messenger.send(event)

        self.clearEvents()

    def setDesc(self, desc):
        self.desc = desc

    def isPendingDelete(self):
        return self.state == InterestState.StatePendingDel

    def __repr__(self):
        return 'InterestState(desc=%s, state=%s, context=%s, event=%s, parentId=%s, zoneIdList=%s)' % (self.desc,
         self.state,
         self.context,
         self.events,
         self.parentId,
         self.zoneIdList)


class InterestHandle():
    __module__ = __name__

    def __init__(self, id):
        self._id = id

    def asInt(self):
        return self._id

    def __eq__(self, other):
        if type(self) == type(other):
            return self._id == other._id
        return self._id == other

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._id)


NO_CONTEXT = 0

class DoInterestManager(DirectObject.DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('DoInterestManager')
    try:
        tempbase = base
    except:
        tempbase = simbase

    InterestDebug = tempbase.config.GetBool('interest-debug', False)
    del tempbase
    _HandleSerialNum = 0
    _HandleMask = 32767
    _ContextIdSerialNum = 100
    _ContextIdMask = 1073741823
    _interests = {}
    _SerialGen = SerialNumGen()
    _SerialNum = serialNum()

    def __init__(self):
        DirectObject.DirectObject.__init__(self)
        self._addInterestEvent = uniqueName('DoInterestManager-Add')
        self._removeInterestEvent = uniqueName('DoInterestManager-Remove')
        self._noNewInterests = False
        self._completeDelayedCallback = None
        self._completeEventCount = ScratchPad(num=0)
        self._allInterestsCompleteCallbacks = []
        return

    def __verbose(self):
        return self.InterestDebug or self.getVerbose()

    def _getAnonymousEvent(self, desc):
        return 'anonymous-%s-%s' % (desc, DoInterestManager._SerialGen.next())

    def setNoNewInterests(self, flag):
        self._noNewInterests = flag

    def noNewInterests(self):
        return self._noNewInterests

    def setAllInterestsCompleteCallback(self, callback):
        if self._completeEventCount.num == 0 and self._completeDelayedCallback is None:
            callback()
        else:
            self._allInterestsCompleteCallbacks.append(callback)
        return

    def getAllInterestsCompleteEvent(self):
        return 'allInterestsComplete-%s' % DoInterestManager._SerialNum

    def resetInterestStateForConnectionLoss(self):
        DoInterestManager._interests.clear()
        self._completeEventCount = ScratchPad(num=0)

    def isValidInterestHandle(self, handle):
        if not isinstance(handle, InterestHandle):
            return False
        return DoInterestManager._interests.has_key(handle.asInt())

    def updateInterestDescription(self, handle, desc):
        iState = DoInterestManager._interests.get(handle.asInt())
        if iState:
            iState.setDesc(desc)

    def addInterest(self, parentId, zoneIdList, description, event = None):
        handle = self._getNextHandle()
        if self._noNewInterests:
            DoInterestManager.notify.warning('addInterest: addingInterests on delete: %s' % handle)
            return
        if parentId not in (self.getGameDoId(),):
            parent = self.getDo(parentId)
            if not parent:
                DoInterestManager.notify.error('addInterest: attempting to add interest under unknown object %s' % parentId)
            elif not parent.hasParentingRules():
                DoInterestManager.notify.error('addInterest: no setParentingRules defined in the DC for object %s (%s)' % (parentId, parent.__class__.__name__))
        if event:
            contextId = self._getNextContextId()
        else:
            contextId = 0
        DoInterestManager._interests[handle] = InterestState(description, InterestState.StateActive, contextId, event, parentId, zoneIdList, self._completeEventCount)
        if self.__verbose():
            print 'CR::INTEREST.addInterest(handle=%s, parentId=%s, zoneIdList=%s, description=%s, event=%s)' % (handle,
             parentId,
             zoneIdList,
             description,
             event)
        self._sendAddInterest(handle, contextId, parentId, zoneIdList, description)
        if event:
            messenger.send(self._getAddInterestEvent(), [event])
        return InterestHandle(handle)

    def addAutoInterest(self, parentId, zoneIdList, description):
        handle = self._getNextHandle()
        if self._noNewInterests:
            DoInterestManager.notify.warning('addInterest: addingInterests on delete: %s' % handle)
            return
        if parentId not in (self.getGameDoId(),):
            parent = self.getDo(parentId)
            if not parent:
                DoInterestManager.notify.error('addInterest: attempting to add interest under unknown object %s' % parentId)
            elif not parent.hasParentingRules():
                DoInterestManager.notify.error('addInterest: no setParentingRules defined in the DC for object %s (%s)' % (parentId, parent.__class__.__name__))
        DoInterestManager._interests[handle] = InterestState(description, InterestState.StateActive, 0, None, parentId, zoneIdList, self._completeEventCount, True)
        if self.__verbose():
            print 'CR::INTEREST.addInterest(handle=%s, parentId=%s, zoneIdList=%s, description=%s)' % (handle,
             parentId,
             zoneIdList,
             description)
        return InterestHandle(handle)

    def removeInterest(self, handle, event = None):
        existed = False
        if not event:
            event = self._getAnonymousEvent('removeInterest')
        handle = handle.asInt()
        if DoInterestManager._interests.has_key(handle):
            existed = True
            intState = DoInterestManager._interests[handle]
            if event:
                messenger.send(self._getRemoveInterestEvent(), [event, intState.parentId, intState.zoneIdList])
            if intState.isPendingDelete():
                self.notify.warning('removeInterest: interest %s already pending removal' % handle)
                if event is not None:
                    intState.addEvent(event)
            else:
                if len(intState.events) > 0:
                    intState.clearEvents()
                intState.state = InterestState.StatePendingDel
                contextId = self._getNextContextId()
                intState.context = contextId
                if event:
                    intState.addEvent(event)
                self._sendRemoveInterest(handle, contextId)
                if not event:
                    self._considerRemoveInterest(handle)
                if self.__verbose():
                    print 'CR::INTEREST.removeInterest(handle=%s, event=%s)' % (handle, event)
        else:
            DoInterestManager.notify.warning('removeInterest: handle not found: %s' % handle)
        return existed

    def removeAutoInterest(self, handle):
        existed = False
        handle = handle.asInt()
        if DoInterestManager._interests.has_key(handle):
            existed = True
            intState = DoInterestManager._interests[handle]
            if intState.isPendingDelete():
                self.notify.warning('removeInterest: interest %s already pending removal' % handle)
            else:
                if len(intState.events) > 0:
                    self.notify.warning('removeInterest: abandoning events: %s' % intState.events)
                    intState.clearEvents()
                intState.state = InterestState.StatePendingDel
                self._considerRemoveInterest(handle)
                if self.__verbose():
                    print 'CR::INTEREST.removeAutoInterest(handle=%s)' % handle
        else:
            DoInterestManager.notify.warning('removeInterest: handle not found: %s' % handle)
        return existed

    @report(types=['args'], dConfigParam='guildmgr')
    def removeAIInterest(self, handle):
        self._sendRemoveAIInterest(handle)

    def alterInterest(self, handle, parentId, zoneIdList, description = None, event = None):
        handle = handle.asInt()
        if self._noNewInterests:
            DoInterestManager.notify.warning('alterInterest: addingInterests on delete: %s' % handle)
            return
        exists = False
        if event is None:
            event = self._getAnonymousEvent('alterInterest')
        if DoInterestManager._interests.has_key(handle):
            if description is not None:
                DoInterestManager._interests[handle].desc = description
            else:
                description = DoInterestManager._interests[handle].desc
            if DoInterestManager._interests[handle].context != NO_CONTEXT:
                DoInterestManager._interests[handle].clearEvents()
            contextId = self._getNextContextId()
            DoInterestManager._interests[handle].context = contextId
            DoInterestManager._interests[handle].parentId = parentId
            DoInterestManager._interests[handle].zoneIdList = zoneIdList
            DoInterestManager._interests[handle].addEvent(event)
            if self.__verbose():
                print 'CR::INTEREST.alterInterest(handle=%s, parentId=%s, zoneIdList=%s, description=%s, event=%s)' % (handle,
                 parentId,
                 zoneIdList,
                 description,
                 event)
            self._sendAddInterest(handle, contextId, parentId, zoneIdList, description, action='modify')
            exists = True
        else:
            DoInterestManager.notify.warning('alterInterest: handle not found: %s' % handle)
        return exists

    def openAutoInterests(self, obj):
        if hasattr(obj, '_autoInterestHandle'):
            self.notify.debug('openAutoInterests(%s): interests already open' % obj.__class__.__name__)
            return
        autoInterests = obj.getAutoInterests()
        obj._autoInterestHandle = None
        if not len(autoInterests):
            return
        obj._autoInterestHandle = self.addAutoInterest(obj.doId, autoInterests, '%s-autoInterest' % obj.__class__.__name__)
        return

    def closeAutoInterests(self, obj):
        if not hasattr(obj, '_autoInterestHandle'):
            self.notify.debug('closeAutoInterests(%s): interests already closed' % obj)
            return
        if obj._autoInterestHandle is not None:
            self.removeAutoInterest(obj._autoInterestHandle)
        del obj._autoInterestHandle
        return

    def _getAddInterestEvent(self):
        return self._addInterestEvent

    def _getRemoveInterestEvent(self):
        return self._removeInterestEvent

    def _getInterestState(self, handle):
        return DoInterestManager._interests[handle]

    def _getNextHandle(self):
        handle = DoInterestManager._HandleSerialNum
        while True:
            handle = handle + 1 & DoInterestManager._HandleMask
            if handle not in DoInterestManager._interests:
                break
            DoInterestManager.notify.warning('interest %s already in use' % handle)

        DoInterestManager._HandleSerialNum = handle
        return DoInterestManager._HandleSerialNum

    def _getNextContextId(self):
        contextId = DoInterestManager._ContextIdSerialNum
        while True:
            contextId = contextId + 1 & DoInterestManager._ContextIdMask
            if contextId != NO_CONTEXT:
                break

        DoInterestManager._ContextIdSerialNum = contextId
        return DoInterestManager._ContextIdSerialNum

    def _considerRemoveInterest(self, handle):
        if DoInterestManager._interests.has_key(handle):
            if DoInterestManager._interests[handle].isPendingDelete():
                if DoInterestManager._interests[handle].context == NO_CONTEXT:
                    del DoInterestManager._interests[handle]

    def _sendAddInterest(self, handle, contextId, parentId, zoneIdList, description, action = None):
        if parentId == 0:
            DoInterestManager.notify.error('trying to set interest to invalid parent: %s' % parentId)
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_ADD_INTEREST)
        datagram.addUint16(handle)
        datagram.addUint32(contextId)
        datagram.addUint32(parentId)
        if isinstance(zoneIdList, types.ListType):
            vzl = list(zoneIdList)
            vzl.sort()
            uniqueElements(vzl)
            for zone in vzl:
                datagram.addUint32(zone)

        else:
            datagram.addUint32(zoneIdList)
        self.send(datagram)

    def _sendRemoveInterest(self, handle, contextId):
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_REMOVE_INTEREST)
        datagram.addUint16(handle)
        if contextId != 0:
            datagram.addUint32(contextId)
        self.send(datagram)

    def _sendRemoveAIInterest(self, handle):
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_REMOVE_INTEREST)
        datagram.addUint16((1 << 15) + handle)
        self.send(datagram)

    def cleanupWaitAllInterestsComplete(self):
        if self._completeDelayedCallback is not None:
            self._completeDelayedCallback.destroy()
            self._completeDelayedCallback = None
        return

    def queueAllInterestsCompleteEvent(self, frames = 5):

        def checkMoreInterests():
            return self._completeEventCount.num > 0

        def sendEvent():
            messenger.send(self.getAllInterestsCompleteEvent())
            for callback in self._allInterestsCompleteCallbacks:
                callback()

            self._allInterestsCompleteCallbacks = []

        self.cleanupWaitAllInterestsComplete()
        self._completeDelayedCallback = FrameDelayedCall('waitForAllInterestCompletes', callback=sendEvent, frames=frames, cancelFunc=checkMoreInterests)
        checkMoreInterests = None
        sendEvent = None
        return

    def handleInterestDoneMessage(self, di):
        handle = di.getUint16()
        contextId = di.getUint32()
        if self.__verbose():
            print 'CR::INTEREST.interestDone(handle=%s)' % handle
        DoInterestManager.notify.debug('handleInterestDoneMessage--> Received handle %s, context %s' % (handle, contextId))
        if DoInterestManager._interests.has_key(handle):
            eventsToSend = []
            if contextId == DoInterestManager._interests[handle].context:
                DoInterestManager._interests[handle].context = NO_CONTEXT
                eventsToSend = list(DoInterestManager._interests[handle].getEvents())
                DoInterestManager._interests[handle].clearEvents()
            else:
                DoInterestManager.notify.debug('handleInterestDoneMessage--> handle: %s: Expecting context %s, got %s' % (handle, DoInterestManager._interests[handle].context, contextId))
            self._considerRemoveInterest(handle)
            for event in eventsToSend:
                messenger.send(event)

        else:
            DoInterestManager.notify.warning('handleInterestDoneMessage: handle not found: %s' % handle)
        if self._completeEventCount.num == 0:
            self.queueAllInterestsCompleteEvent()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DoInterestManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:09 Pacific Daylight Time
