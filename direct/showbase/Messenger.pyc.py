# 2013.08.22 22:14:38 Pacific Daylight Time
# Embedded file name: direct.showbase.Messenger
__all__ = ['Messenger']
from PythonUtil import *
from direct.directnotify import DirectNotifyGlobal
import types

class Lock():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('Messenger.Lock')

    def __init__(self):
        self.locked = 0

    def acquire(self):
        if self.locked:
            return self.__getLock()
        self.locked += 1
        if self.locked > 1:
            self.locked -= 1
            return self.__getLock()

    def release(self):
        if self.locked:
            self.locked -= 1
            return
        self.release = self.lock.release
        return self.lock.release()

    def __getLock(self):
        self.notify.info('Acquiring Panda lock for the first time.')
        from pandac.PandaModules import Thread, Mutex
        self.__dict__.setdefault('lock', Mutex('Messenger'))
        self.lock.acquire()
        self.acquire = self.lock.acquire
        self.notify.info('Waiting for cheesy lock to be released.')
        while self.locked:
            Thread.forceYield()

        self.notify.info('Got cheesy lock.')


class Messenger():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('Messenger')

    def __init__(self):
        self.__callbacks = {}
        self.__objectEvents = {}
        self._messengerIdGen = 0
        self._id2object = {}
        self._eventQueuesByTaskChain = {}
        self.lock = Lock()
        self.quieting = {'NewFrame': 1,
         'avatarMoving': 1,
         'event-loop-done': 1,
         'collisionLoopFinished': 1}

    def _getMessengerId(self, object):
        if not hasattr(object, '_MSGRmessengerId'):
            object._MSGRmessengerId = (object.__class__.__name__, self._messengerIdGen)
            self._messengerIdGen += 1
        return object._MSGRmessengerId

    def _storeObject(self, object):
        id = self._getMessengerId(object)
        if id not in self._id2object:
            self._id2object[id] = [1, object]
        else:
            self._id2object[id][0] += 1

    def _getObject(self, id):
        return self._id2object[id][1]

    def _getObjects(self):
        self.lock.acquire()
        try:
            objs = []
            for refCount, obj in self._id2object.itervalues():
                objs.append(obj)

            return objs
        finally:
            self.lock.release()

    def _getNumListeners(self, event):
        return len(self.__callbacks.get(event, {}))

    def _getEvents(self):
        return self.__callbacks.keys()

    def _releaseObject(self, object):
        id = self._getMessengerId(object)
        if id in self._id2object:
            record = self._id2object[id]
            record[0] -= 1
            if record[0] <= 0:
                del self._id2object[id]

    def accept(self, event, object, method, extraArgs = [], persistent = 1):
        notifyDebug = Messenger.notify.getDebug()
        if notifyDebug:
            Messenger.notify.debug('object: %s (%s)\n accepting: %s\n method: %s\n extraArgs: %s\n persistent: %s' % (safeRepr(object),
             self._getMessengerId(object),
             event,
             safeRepr(method),
             safeRepr(extraArgs),
             persistent))
        if not isinstance(extraArgs, list):
            raise isinstance(extraArgs, tuple) or isinstance(extraArgs, set) or TypeError, 'A list is required as extraArgs argument'
        self.lock.acquire()
        try:
            acceptorDict = self.__callbacks.setdefault(event, {})
            id = self._getMessengerId(object)
            if id in acceptorDict:
                if notifyDebug:
                    oldMethod = acceptorDict[id][0]
                    if oldMethod == method:
                        self.notify.warning('object: %s was already accepting: "%s" with same callback: %s()' % (object.__class__.__name__, safeRepr(event), method.__name__))
                    else:
                        self.notify.warning('object: %s accept: "%s" new callback: %s() supplanting old callback: %s()' % (object.__class__.__name__,
                         safeRepr(event),
                         method.__name__,
                         oldMethod.__name__))
            acceptorDict[id] = [method, extraArgs, persistent]
            eventDict = self.__objectEvents.setdefault(id, {})
            if event not in eventDict:
                self._storeObject(object)
                eventDict[event] = None
        finally:
            self.lock.release()

        return

    def ignore(self, event, object):
        if Messenger.notify.getDebug():
            Messenger.notify.debug(safeRepr(object) + ' (%s)\n now ignoring: ' % (self._getMessengerId(object),) + safeRepr(event))
        self.lock.acquire()
        try:
            id = self._getMessengerId(object)
            acceptorDict = self.__callbacks.get(event)
            if acceptorDict and id in acceptorDict:
                del acceptorDict[id]
                if len(acceptorDict) == 0:
                    del self.__callbacks[event]
            eventDict = self.__objectEvents.get(id)
            if eventDict and event in eventDict:
                del eventDict[event]
                if len(eventDict) == 0:
                    del self.__objectEvents[id]
                self._releaseObject(object)
        finally:
            self.lock.release()

    def ignoreAll(self, object):
        if Messenger.notify.getDebug():
            Messenger.notify.debug(safeRepr(object) + ' (%s)\n now ignoring all events' % (self._getMessengerId(object),))
        self.lock.acquire()
        try:
            id = self._getMessengerId(object)
            eventDict = self.__objectEvents.get(id)
            if eventDict:
                for event in eventDict.keys():
                    acceptorDict = self.__callbacks.get(event)
                    if acceptorDict and id in acceptorDict:
                        del acceptorDict[id]
                        if len(acceptorDict) == 0:
                            del self.__callbacks[event]
                    self._releaseObject(object)

                del self.__objectEvents[id]
        finally:
            self.lock.release()

    def getAllAccepting(self, object):
        self.lock.acquire()
        try:
            id = self._getMessengerId(object)
            eventDict = self.__objectEvents.get(id)
            if eventDict:
                return eventDict.keys()
            return []
        finally:
            self.lock.release()

    def isAccepting(self, event, object):
        self.lock.acquire()
        try:
            acceptorDict = self.__callbacks.get(event)
            id = self._getMessengerId(object)
            if acceptorDict and id in acceptorDict:
                return 1
            return 0
        finally:
            self.lock.release()

    def whoAccepts(self, event):
        return self.__callbacks.get(event)

    def isIgnoring(self, event, object):
        return not self.isAccepting(event, object)

    def send(self, event, sentArgs = [], taskChain = None):
        if Messenger.notify.getDebug() and not self.quieting.get(event):
            pass
        self.lock.acquire()
        try:
            foundWatch = 0
            acceptorDict = self.__callbacks.get(event)
            if not acceptorDict:
                return
            if taskChain:
                from direct.task.TaskManagerGlobal import taskMgr
                queue = self._eventQueuesByTaskChain.setdefault(taskChain, [])
                queue.append((acceptorDict,
                 event,
                 sentArgs,
                 foundWatch))
                if len(queue) == 1:
                    taskMgr.add(self.__taskChainDispatch, name='Messenger-%s' % taskChain, extraArgs=[taskChain], taskChain=taskChain, appendTask=True)
            else:
                self.__dispatch(acceptorDict, event, sentArgs, foundWatch)
        finally:
            self.lock.release()

    def __taskChainDispatch(self, taskChain, task):
        while True:
            eventTuple = None
            self.lock.acquire()
            try:
                queue = self._eventQueuesByTaskChain.get(taskChain, None)
                if queue:
                    eventTuple = queue[0]
                    del queue[0]
                if not queue:
                    if queue is not None:
                        del self._eventQueuesByTaskChain[taskChain]
                if not eventTuple:
                    return task.done
                self.__dispatch(*eventTuple)
            finally:
                self.lock.release()

        return task.done

    def __dispatch(self, acceptorDict, event, sentArgs, foundWatch):
        for id in acceptorDict.keys():
            callInfo = acceptorDict.get(id)
            if callInfo:
                method, extraArgs, persistent = callInfo
                if not persistent:
                    eventDict = self.__objectEvents.get(id)
                    if eventDict and event in eventDict:
                        del eventDict[event]
                        if len(eventDict) == 0:
                            del self.__objectEvents[id]
                        self._releaseObject(self._getObject(id))
                    del acceptorDict[id]
                    if event in self.__callbacks and len(self.__callbacks[event]) == 0:
                        del self.__callbacks[event]
                self.lock.release()
                try:
                    method(*(extraArgs + sentArgs))
                finally:
                    self.lock.acquire()

    def clear(self):
        self.lock.acquire()
        try:
            self.__callbacks.clear()
            self.__objectEvents.clear()
            self._id2object.clear()
        finally:
            self.lock.release()

    def isEmpty(self):
        return len(self.__callbacks) == 0

    def getEvents(self):
        return self.__callbacks.keys()

    def replaceMethod(self, oldMethod, newFunction):
        import new
        retFlag = 0
        for entry in self.__callbacks.items():
            event, objectDict = entry
            for objectEntry in objectDict.items():
                object, params = objectEntry
                method = params[0]
                if type(method) == types.MethodType:
                    function = method.im_func
                else:
                    function = method
                if function == oldMethod:
                    newMethod = new.instancemethod(newFunction, method.im_self, method.im_class)
                    params[0] = newMethod
                    retFlag += 1

        return retFlag

    def toggleVerbose(self):
        isVerbose = 1 - Messenger.notify.getDebug()
        Messenger.notify.setDebug(isVerbose)
        if isVerbose:
            print 'Verbose mode true.  quiet list = %s' % (self.quieting.keys(),)

    def find(self, needle):
        keys = self.__callbacks.keys()
        keys.sort()
        for event in keys:
            if repr(event).find(needle) >= 0:
                print self.__eventRepr(event),
                return {event: self.__callbacks[event]}

    def findAll(self, needle, limit = None):
        matches = {}
        keys = self.__callbacks.keys()
        keys.sort()
        for event in keys:
            if repr(event).find(needle) >= 0:
                print self.__eventRepr(event),
                matches[event] = self.__callbacks[event]
                if limit > 0:
                    limit -= 1
                    if limit == 0:
                        break

        return matches

    def __methodRepr(self, method):
        if type(method) == types.MethodType:
            functionName = method.im_class.__name__ + '.' + method.im_func.__name__
        else:
            functionName = method.__name__
        return functionName

    def __eventRepr(self, event):
        str = event.ljust(32) + '\t'
        acceptorDict = self.__callbacks[event]
        for key, (method, extraArgs, persistent) in acceptorDict.items():
            str = str + self.__methodRepr(method) + ' '

        str = str + '\n'
        return str

    def __repr__(self):
        str = 'The messenger is currently handling:\n' + '=' * 64 + '\n'
        keys = self.__callbacks.keys()
        keys.sort()
        for event in keys:
            str += self.__eventRepr(event)

        str += '=' * 64 + '\n'
        for key, eventDict in self.__objectEvents.items():
            object = self._getObject(key)
            str += '%s:\n' % repr(object)
            for event in eventDict.keys():
                str += '     %s\n' % repr(event)

        str += '=' * 64 + '\n' + 'End of messenger info.\n'
        return str

    def detailedRepr(self):
        import types
        str = 'Messenger\n'
        str = str + '=' * 50 + '\n'
        keys = self.__callbacks.keys()
        keys.sort()
        for event in keys:
            acceptorDict = self.__callbacks[event]
            str = str + 'Event: ' + event + '\n'
            for key in acceptorDict.keys():
                function, extraArgs, persistent = acceptorDict[key]
                object = self._getObject(key)
                if type(object) == types.InstanceType:
                    className = object.__class__.__name__
                else:
                    className = 'Not a class'
                functionName = function.__name__
                str = str + '\t' + 'Acceptor:     ' + className + ' instance' + '\n\t' + 'Function name:' + functionName + '\n\t' + 'Extra Args:   ' + repr(extraArgs) + '\n\t' + 'Persistent:   ' + repr(persistent) + '\n'
                if type(function) == types.MethodType:
                    str = str + '\t' + 'Method:       ' + repr(function) + '\n\t' + 'Function:     ' + repr(function.im_func) + '\n'
                else:
                    str = str + '\t' + 'Function:     ' + repr(function) + '\n'

        str = str + '=' * 50 + '\n'
        return str
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\Messenger.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:38 Pacific Daylight Time
