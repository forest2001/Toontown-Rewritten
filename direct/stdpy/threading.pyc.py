# 2013.08.22 22:14:52 Pacific Daylight Time
# Embedded file name: direct.stdpy.threading
import direct
from pandac import PandaModules as pm
from direct.stdpy import thread as _thread
import sys as _sys
import weakref
__all__ = ['Thread',
 'Lock',
 'RLock',
 'Condition',
 'Semaphore',
 'BoundedSemaphore',
 'Event',
 'Timer',
 'local',
 'current_thread',
 'currentThread',
 'enumerate',
 'active_count',
 'activeCount',
 'settrace',
 'setprofile',
 'stack_size']
local = _thread._local

class ThreadBase():
    __module__ = __name__

    def __init__(self):
        pass

    def getName(self):
        return self.name

    def is_alive(self):
        return self.__thread.isStarted()

    def isAlive(self):
        return self.__thread.isStarted()

    def isDaemon(self):
        return self.daemon

    def setDaemon(self, daemon):
        if self.is_alive():
            raise RuntimeError
        self.__dict__['daemon'] = daemon

    def __setattr__(self, key, value):
        if key == 'name':
            self.setName(value)
        elif key == 'ident':
            raise AttributeError
        elif key == 'daemon':
            self.setDaemon(value)
        else:
            self.__dict__[key] = value


ThreadBase.forceYield = pm.Thread.forceYield
ThreadBase.considerYield = pm.Thread.considerYield

class Thread(ThreadBase):
    __module__ = __name__

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = {}):
        ThreadBase.__init__(self)
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        if not name:
            import threading2
            name = threading2._newname()
        current = current_thread()
        self.__dict__['daemon'] = current.daemon
        self.__dict__['name'] = name
        self.__thread = pm.PythonThread(self.run, None, name, name)
        threadId = _thread._add_thread(self.__thread, weakref.proxy(self))
        self.__dict__['ident'] = threadId
        return

    def __del__(self):
        if _thread and _thread._remove_thread_id:
            _thread._remove_thread_id(self.ident)

    def start(self):
        if self.__thread.isStarted():
            raise RuntimeError
        if not self.__thread.start(pm.TPNormal, True):
            raise RuntimeError

    def run(self):
        global _setprofile_func
        global _settrace_func
        if _settrace_func:
            _sys.settrace(_settrace_func)
        if _setprofile_func:
            _sys.setprofile(_setprofile_func)
        self.__target(*self.__args, **self.__kwargs)

    def join(self, timeout = None):
        self.__thread.join()
        self.__thread = None
        return

    def setName(self, name):
        self.__dict__['name'] = name
        self.__thread.setName(name)


class ExternalThread(ThreadBase):
    __module__ = __name__

    def __init__(self, extThread, threadId):
        ThreadBase.__init__(self)
        self.__thread = extThread
        self.__dict__['daemon'] = True
        self.__dict__['name'] = self.__thread.getName()
        self.__dict__['ident'] = threadId

    def start(self):
        raise RuntimeError

    def run(self):
        raise RuntimeError

    def join(self, timeout = None):
        raise RuntimeError

    def setDaemon(self, daemon):
        raise RuntimeError


class MainThread(ExternalThread):
    __module__ = __name__

    def __init__(self, extThread, threadId):
        ExternalThread.__init__(self, extThread, threadId)
        self.__dict__['daemon'] = False


class Lock(pm.Mutex):
    __module__ = __name__

    def __init__(self, name = 'PythonLock'):
        pm.Mutex.__init__(self, name)

    def acquire(self, blocking = True):
        if blocking:
            pm.Mutex.acquire(self)
            return True
        else:
            return pm.Mutex.tryAcquire(self)

    __enter__ = acquire

    def __exit__(self, t, v, tb):
        self.release()


class RLock(pm.ReMutex):
    __module__ = __name__

    def __init__(self, name = 'PythonRLock'):
        pm.ReMutex.__init__(self, name)

    def acquire(self, blocking = True):
        if blocking:
            pm.ReMutex.acquire(self)
            return True
        else:
            return pm.ReMutex.tryAcquire(self)

    __enter__ = acquire

    def __exit__(self, t, v, tb):
        self.release()


class Condition(pm.ConditionVarFull):
    __module__ = __name__

    def __init__(self, lock = None):
        if not lock:
            lock = Lock()
        self.__lock = lock
        pm.ConditionVarFull.__init__(self, self.__lock)

    def acquire(self, *args, **kw):
        return self.__lock.acquire(*args, **kw)

    def release(self):
        self.__lock.release()

    def wait(self, timeout = None):
        if timeout is None:
            pm.ConditionVarFull.wait(self)
        else:
            pm.ConditionVarFull.wait(self, timeout)
        return

    def notifyAll(self):
        pm.ConditionVarFull.notifyAll(self)

    notify_all = notifyAll
    __enter__ = acquire

    def __exit__(self, t, v, tb):
        self.release()


class Semaphore(pm.Semaphore):
    __module__ = __name__

    def __init__(self, value = 1):
        pm.Semaphore.__init__(self, value)

    def acquire(self, blocking = True):
        if blocking:
            pm.Semaphore.acquire(self)
            return True
        else:
            return pm.Semaphore.tryAcquire(self)

    __enter__ = acquire

    def __exit__(self, t, v, tb):
        self.release()


class BoundedSemaphore(Semaphore):
    __module__ = __name__

    def __init__(self, value = 1):
        self.__max = value
        Semaphore.__init__(value)

    def release(self):
        if self.getCount() > value:
            raise ValueError
        Semaphore.release(self)


class Event():
    __module__ = __name__

    def __init__(self):
        self.__lock = pm.Lock('Python Event')
        self.__cvar = pm.ConditionVarFull(self.__lock)
        self.__flag = False

    def is_set(self):
        return self.__flag

    isSet = is_set

    def set(self):
        self.__lock.acquire()
        try:
            self.__flag = True
            self.__cvar.signalAll()
        finally:
            self.__lock.release()

    def clear(self):
        self.__lock.acquire()
        try:
            self.__flag = False
        finally:
            self.__lock.release()

    def wait(self, timeout = None):
        self.__lock.acquire()
        try:
            if timeout is None:
                while not self.__flag:
                    self.__cvar.wait()

            else:
                clock = pm.TrueClock.getGlobalPtr()
                expires = clock.getShortTime() + timeout
                while not self.__flag:
                    wait = expires - clock.getShortTime()
                    if wait < 0:
                        return
                    self.__cvar.wait(wait)

        finally:
            self.__lock.release()

        return


class Timer(Thread):
    __module__ = __name__

    def __init__(self, interval, function, args = [], kwargs = {}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.isSet():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


def _create_thread_wrapper(t, threadId):
    if isinstance(t, pm.MainThread):
        pyt = MainThread(t, threadId)
    else:
        pyt = ExternalThread(t, threadId)
    return pyt


def current_thread():
    t = pm.Thread.getCurrentThread()
    return _thread._get_thread_wrapper(t, _create_thread_wrapper)


currentThread = current_thread

def enumerate():
    tlist = []
    _thread._threadsLock.acquire()
    try:
        for thread, locals, wrapper in _thread._threads.values():
            if wrapper and thread.isStarted():
                tlist.append(wrapper)

        return tlist
    finally:
        _thread._threadsLock.release()


def active_count():
    return len(enumerate())


activeCount = active_count
_settrace_func = None

def settrace(func):
    global _settrace_func
    _settrace_func = func


_setprofile_func = None

def setprofile(func):
    global _setprofile_func
    _setprofile_func = func


def stack_size(size = None):
    raise ThreadError


def _test():
    from collections import deque
    _sleep = pm.Thread.sleep
    _VERBOSE = False

    class _Verbose(object):
        __module__ = __name__

        def __init__(self, verbose = None):
            if verbose is None:
                verbose = _VERBOSE
            self.__verbose = verbose
            return

        def _note(self, format, *args):
            if self.__verbose:
                format = format % args
                format = '%s: %s\n' % (currentThread().getName(), format)
                _sys.stderr.write(format)

    class BoundedQueue(_Verbose):
        __module__ = __name__

        def __init__(self, limit):
            _Verbose.__init__(self)
            self.mon = Lock(name='BoundedQueue.mon')
            self.rc = Condition(self.mon)
            self.wc = Condition(self.mon)
            self.limit = limit
            self.queue = deque()

        def put(self, item):
            self.mon.acquire()
            while len(self.queue) >= self.limit:
                self._note('put(%s): queue full', item)
                self.wc.wait()

            self.queue.append(item)
            self._note('put(%s): appended, length now %d', item, len(self.queue))
            self.rc.notify()
            self.mon.release()

        def get(self):
            self.mon.acquire()
            while not self.queue:
                self._note('get(): queue empty')
                self.rc.wait()

            item = self.queue.popleft()
            self._note('get(): got %s, %d left', item, len(self.queue))
            self.wc.notify()
            self.mon.release()
            return item

    class ProducerThread(Thread):
        __module__ = __name__

        def __init__(self, queue, quota):
            Thread.__init__(self, name='Producer')
            self.queue = queue
            self.quota = quota

        def run(self):
            from random import random
            counter = 0
            while counter < self.quota:
                counter = counter + 1
                self.queue.put('%s.%d' % (self.getName(), counter))
                _sleep(random() * 1e-05)

    class ConsumerThread(Thread):
        __module__ = __name__

        def __init__(self, queue, count):
            Thread.__init__(self, name='Consumer')
            self.queue = queue
            self.count = count

        def run(self):
            while self.count > 0:
                item = self.queue.get()
                print item
                self.count = self.count - 1

    NP = 3
    QL = 4
    NI = 5
    Q = BoundedQueue(QL)
    P = []
    for i in range(NP):
        t = ProducerThread(Q, NI)
        t.setName('Producer-%d' % (i + 1))
        P.append(t)

    C = ConsumerThread(Q, NI * NP)
    for t in P:
        t.start()
        _sleep(1e-06)

    C.start()
    for t in P:
        t.join()

    C.join()


if __name__ == '__main__':
    _test()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\stdpy\threading.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:53 Pacific Daylight Time
