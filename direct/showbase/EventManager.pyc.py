# 2013.08.22 22:14:34 Pacific Daylight Time
# Embedded file name: direct.showbase.EventManager
__all__ = ['EventManager']
from MessengerGlobal import *
from direct.directnotify.DirectNotifyGlobal import *

class EventManager():
    __module__ = __name__
    notify = None
    PStatCollector = None
    EventStorePandaNode = None
    EventQueue = None
    EventHandler = None

    def __init__(self, eventQueue = None):
        if EventManager.notify == None:
            EventManager.notify = directNotify.newCategory('EventManager')
        self.eventQueue = eventQueue
        self.eventHandler = None
        self._wantPstats = None
        return

    def doEvents(self):
        if self._wantPstats is None:
            self._wantPstats = config.GetBool('pstats-eventmanager', 0)
            from pandac.PandaModules import PStatCollector
            EventManager.PStatCollector = PStatCollector
        if self._wantPstats:
            processFunc = self.processEventPstats
        else:
            processFunc = self.processEvent
        while not self.eventQueue.isQueueEmpty():
            processFunc(self.eventQueue.dequeueEvent())

        return

    def eventLoopTask(self, task):
        self.doEvents()
        messenger.send('event-loop-done')
        return task.cont

    def parseEventParameter(self, eventParameter):
        if eventParameter.isInt():
            return eventParameter.getIntValue()
        elif eventParameter.isDouble():
            return eventParameter.getDoubleValue()
        elif eventParameter.isString():
            return eventParameter.getStringValue()
        elif eventParameter.isWstring():
            return eventParameter.getWstringValue()
        elif eventParameter.isTypedRefCount():
            return eventParameter.getTypedRefCountValue()
        elif eventParameter.isEmpty():
            return
        else:
            ptr = eventParameter.getPtr()
            if EventManager.EventStorePandaNode is None:
                from pandac.PandaModules import EventStorePandaNode
                EventManager.EventStorePandaNode = EventStorePandaNode
            if isinstance(ptr, EventManager.EventStorePandaNode):
                ptr = ptr.getValue()
            return ptr
        return

    def processEvent(self, event):
        eventName = event.getName()
        if eventName:
            paramList = []
            for i in range(event.getNumParameters()):
                eventParameter = event.getParameter(i)
                eventParameterData = self.parseEventParameter(eventParameter)
                paramList.append(eventParameterData)

            if EventManager.notify.getDebug() and eventName != 'NewFrame':
                EventManager.notify.debug('received C++ event named: ' + eventName + ' parameters: ' + repr(paramList))
            if paramList:
                messenger.send(eventName, paramList)
            else:
                messenger.send(eventName)
            if self.eventHandler:
                self.eventHandler.dispatchEvent(event)
        else:
            EventManager.notify.warning('unnamed event in processEvent')

    def processEventPstats(self, event):
        eventName = event.getName()
        if eventName:
            paramList = []
            for i in range(event.getNumParameters()):
                eventParameter = event.getParameter(i)
                eventParameterData = self.parseEventParameter(eventParameter)
                paramList.append(eventParameterData)

            if EventManager.notify.getDebug() and eventName != 'NewFrame':
                EventManager.notify.debug('received C++ event named: ' + eventName + ' parameters: ' + repr(paramList))
            if self._wantPstats:
                name = eventName
                hyphen = name.find('-')
                if hyphen >= 0:
                    name = name[0:hyphen]
                pstatCollector = EventManager.PStatCollector('App:Show code:eventManager:' + name)
                pstatCollector.start()
                if self.eventHandler:
                    cppPstatCollector = EventManager.PStatCollector('App:Show code:eventManager:' + name + ':C++')
            if paramList:
                messenger.send(eventName, paramList)
            else:
                messenger.send(eventName)
            if self.eventHandler:
                if self._wantPstats:
                    cppPstatCollector.start()
                self.eventHandler.dispatchEvent(event)
            if self._wantPstats:
                if self.eventHandler:
                    cppPstatCollector.stop()
                pstatCollector.stop()
        else:
            EventManager.notify.warning('unnamed event in processEvent')

    def restart(self):
        if None in (EventManager.EventQueue, EventManager.EventHandler):
            from pandac.PandaModules import EventQueue, EventHandler
            EventManager.EventQueue = EventQueue
            EventManager.EventHandler = EventHandler
        if self.eventQueue == None:
            self.eventQueue = EventManager.EventQueue.getGlobalEventQueue()
        if self.eventHandler == None:
            if self.eventQueue == EventManager.EventQueue.getGlobalEventQueue():
                self.eventHandler = EventManager.EventHandler.getGlobalEventHandler()
            else:
                self.eventHandler = EventManager.EventHandler(self.eventQueue)
        from direct.task.TaskManagerGlobal import taskMgr
        taskMgr.add(self.eventLoopTask, 'eventManager')
        return

    def shutdown(self):
        from direct.task.TaskManagerGlobal import taskMgr
        taskMgr.remove('eventManager')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\EventManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:34 Pacific Daylight Time
