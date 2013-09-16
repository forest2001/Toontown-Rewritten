# 2013.08.22 22:14:11 Pacific Daylight Time
# Embedded file name: direct.fsm.FSM
__all__ = ['FSMException', 'FSM']
from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil
from direct.stdpy.threading import RLock
import types
import string

class FSMException(Exception):
    __module__ = __name__


class AlreadyInTransition(FSMException):
    __module__ = __name__


class RequestDenied(FSMException):
    __module__ = __name__


class FSM(DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FSM')
    SerialNum = 0
    defaultTransitions = None

    def __init__(self, name):
        self.fsmLock = RLock()
        self.name = name
        self.stateArray = []
        self._serialNum = FSM.SerialNum
        FSM.SerialNum += 1
        self._broadcastStateChanges = False
        self.state = 'Off'
        self.__requestQueue = []

    def cleanup(self):
        self.fsmLock.acquire()
        try:
            if self.state != 'Off':
                self.__setState('Off')
        finally:
            self.fsmLock.release()

    def setBroadcastStateChanges(self, doBroadcast):
        self._broadcastStateChanges = doBroadcast

    def getStateChangeEvent(self):
        return 'FSM-%s-%s-stateChange' % (self._serialNum, self.name)

    def getCurrentFilter(self):
        if not self.state:
            error = 'FSM cannot determine current filter while in transition (%s -> %s).' % (self.oldState, self.newState)
            raise AlreadyInTransition, error
        filter = getattr(self, 'filter' + self.state, None)
        if not filter:
            filter = self.defaultFilter
        return filter

    def getCurrentOrNextState(self):
        self.fsmLock.acquire()
        try:
            if self.state:
                return self.state
            return self.newState
        finally:
            self.fsmLock.release()

    def getCurrentStateOrTransition(self):
        self.fsmLock.acquire()
        try:
            if self.state:
                return self.state
            return '%s -> %s' % (self.oldState, self.newState)
        finally:
            self.fsmLock.release()

    def isInTransition(self):
        self.fsmLock.acquire()
        try:
            return self.state == None
        finally:
            self.fsmLock.release()

        return

    def forceTransition(self, request, *args):
        self.fsmLock.acquire()
        try:
            self.notify.debug('%s.forceTransition(%s, %s' % (self.name, request, str(args)[1:]))
            if not self.state:
                self.__requestQueue.append(PythonUtil.Functor(self.forceTransition, request, *args))
                return
            self.__setState(request, *args)
        finally:
            self.fsmLock.release()

    def demand(self, request, *args):
        self.fsmLock.acquire()
        try:
            self.notify.debug('%s.demand(%s, %s' % (self.name, request, str(args)[1:]))
            if not self.state:
                self.__requestQueue.append(PythonUtil.Functor(self.demand, request, *args))
                return
            if not self.request(request, *args):
                raise RequestDenied, '%s (from state: %s)' % (request, self.state)
        finally:
            self.fsmLock.release()

    def request(self, request, *args):
        self.fsmLock.acquire()
        try:
            self.notify.debug('%s.request(%s, %s' % (self.name, request, str(args)[1:]))
            filter = self.getCurrentFilter()
            result = filter(request, args)
            if result:
                if isinstance(result, types.StringTypes):
                    result = (result,) + args
                self.__setState(*result)
            return result
        finally:
            self.fsmLock.release()

    def defaultEnter(self, *args):
        pass

    def defaultExit(self):
        pass

    def defaultFilter(self, request, args):
        if request == 'Off':
            return (request,) + args
        if self.defaultTransitions is None:
            if request[0] in string.uppercase:
                return (request,) + args
        else:
            if request in self.defaultTransitions.get(self.state, []):
                return (request,) + args
            if request[0] in string.uppercase:
                raise RequestDenied, '%s (from state: %s)' % (request, self.state)
        return

    def filterOff(self, request, args):
        if request[0] in string.uppercase:
            return (request,) + args
        return self.defaultFilter(request, args)

    def setStateArray(self, stateArray):
        self.fsmLock.acquire()
        try:
            self.stateArray = stateArray
        finally:
            self.fsmLock.release()

    def requestNext(self, *args):
        self.fsmLock.acquire()
        try:
            if self.stateArray:
                if self.state not in self.stateArray:
                    self.request(self.stateArray[0])
                else:
                    cur_index = self.stateArray.index(self.state)
                    new_index = (cur_index + 1) % len(self.stateArray)
                    self.request(self.stateArray[new_index], args)
        finally:
            self.fsmLock.release()

    def requestPrev(self, *args):
        self.fsmLock.acquire()
        try:
            if self.stateArray:
                if self.state not in self.stateArray:
                    self.request(self.stateArray[0])
                else:
                    cur_index = self.stateArray.index(self.state)
                    new_index = (cur_index - 1) % len(self.stateArray)
                    self.request(self.stateArray[new_index], args)
        finally:
            self.fsmLock.release()

    def __setState(self, newState, *args):
        self.oldState = self.state
        self.newState = newState
        self.state = None
        try:
            if not self.__callFromToFunc(self.oldState, self.newState, *args):
                self.__callExitFunc(self.oldState)
                self.__callEnterFunc(self.newState, *args)
        except:
            self.state = 'InternalError'
            del self.oldState
            del self.newState
            raise

        if self._broadcastStateChanges:
            messenger.send(self.getStateChangeEvent())
        self.state = newState
        del self.oldState
        del self.newState
        if self.__requestQueue:
            request = self.__requestQueue.pop(0)
            request()
        return

    def __callEnterFunc(self, name, *args):
        func = getattr(self, 'enter' + name, None)
        if not func:
            func = self.defaultEnter
        func(*args)
        return

    def __callFromToFunc(self, oldState, newState, *args):
        func = getattr(self, 'from%sTo%s' % (oldState, newState), None)
        if func:
            func(*args)
            return True
        return False

    def __callExitFunc(self, name):
        func = getattr(self, 'exit' + name, None)
        if not func:
            func = self.defaultExit
        func()
        return

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self.fsmLock.acquire()
        try:
            className = self.__class__.__name__
            if self.state:
                str = '%s FSM:%s in state "%s"' % (className, self.name, self.state)
            else:
                str = "%s FSM:%s in transition from '%s' to '%s'" % (className,
                 self.name,
                 self.oldState,
                 self.newState)
            return str
        finally:
            self.fsmLock.release()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\fsm\FSM.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:11 Pacific Daylight Time
