# 2013.08.22 22:14:53 Pacific Daylight Time
# Embedded file name: direct.stdpy.threading2
import sys as _sys
from direct.stdpy import thread
from direct.stdpy.thread import stack_size, _local as local
from pandac import PandaModules as pm
_sleep = pm.Thread.sleep
from time import time as _time
from traceback import format_exc as _format_exc
from collections import deque
__all__ = ['activeCount',
 'Condition',
 'currentThread',
 'enumerate',
 'Event',
 'Lock',
 'RLock',
 'Semaphore',
 'BoundedSemaphore',
 'Thread',
 'Timer',
 'setprofile',
 'settrace',
 'local',
 'stack_size']
_start_new_thread = thread.start_new_thread
_allocate_lock = thread.allocate_lock
_get_ident = thread.get_ident
ThreadError = thread.error
del thread
_VERBOSE = False

class _Verbose(object):
    __module__ = __name__

    def __init__(self, verbose = None):
        pass

    def _note(self, *args):
        pass


_profile_hook = None
_trace_hook = None

def setprofile(func):
    global _profile_hook
    _profile_hook = func


def settrace(func):
    global _trace_hook
    _trace_hook = func


Lock = _allocate_lock

def RLock(*args, **kwargs):
    return _RLock(*args, **kwargs)


class _RLock(_Verbose):
    __module__ = __name__

    def __init__(self, verbose = None):
        _Verbose.__init__(self, verbose)
        self.__block = _allocate_lock()
        self.__owner = None
        self.__count = 0
        return

    def __repr__(self):
        return '<%s(%s, %d)>' % (self.__class__.__name__, self.__owner and self.__owner.getName(), self.__count)

    def acquire(self, blocking = 1):
        me = currentThread()
        if self.__owner is me:
            self.__count = self.__count + 1
            return 1
        rc = self.__block.acquire(blocking)
        if rc:
            self.__owner = me
            self.__count = 1
        return rc

    __enter__ = acquire

    def release(self):
        me = currentThread()
        self.__count = count = self.__count - 1
        if not count:
            self.__owner = None
            self.__block.release()
        return

    def __exit__(self, t, v, tb):
        self.release()

    def _acquire_restore(self, (count, owner)):
        self.__block.acquire()
        self.__count = count
        self.__owner = owner

    def _release_save(self):
        count = self.__count
        self.__count = 0
        owner = self.__owner
        self.__owner = None
        self.__block.release()
        return (count, owner)

    def _is_owned(self):
        return self.__owner is currentThread()


def Condition(*args, **kwargs):
    return _Condition(*args, **kwargs)


class _Condition(_Verbose):
    __module__ = __name__

    def __init__(self, lock = None, verbose = None):
        _Verbose.__init__(self, verbose)
        if lock is None:
            lock = RLock()
        self.__lock = lock
        self.acquire = lock.acquire
        self.release = lock.release
        try:
            self._release_save = lock._release_save
        except AttributeError:
            pass

        try:
            self._acquire_restore = lock._acquire_restore
        except AttributeError:
            pass

        try:
            self._is_owned = lock._is_owned
        except AttributeError:
            pass

        self.__waiters = []
        return

    def __enter__(self):
        return self.__lock.__enter__()

    def __exit__(self, *args):
        return self.__lock.__exit__(*args)

    def __repr__(self):
        return '<Condition(%s, %d)>' % (self.__lock, len(self.__waiters))

    def _release_save(self):
        self.__lock.release()

    def _acquire_restore(self, x):
        self.__lock.acquire()

    def _is_owned(self):
        if self.__lock.acquire(0):
            self.__lock.release()
            return False
        else:
            return True

    def wait(self, timeout = None):
        waiter = _allocate_lock()
        waiter.acquire()
        self.__waiters.append(waiter)
        saved_state = self._release_save()
        try:
            if timeout is None:
                waiter.acquire()
            else:
                endtime = _time() + timeout
                delay = 0.0005
                while True:
                    gotit = waiter.acquire(0)
                    if gotit:
                        break
                    remaining = endtime - _time()
                    if remaining <= 0:
                        break
                    delay = min(delay * 2, remaining, 0.05)
                    _sleep(delay)

                if not gotit:
                    try:
                        self.__waiters.remove(waiter)
                    except ValueError:
                        pass

        finally:
            self._acquire_restore(saved_state)

        return

    def notify(self, n = 1):
        __waiters = self.__waiters
        waiters = __waiters[:n]
        if not waiters:
            return
        self._note('%s.notify(): notifying %d waiter%s', self, n, n != 1 and 's' or '')
        for waiter in waiters:
            waiter.release()
            try:
                __waiters.remove(waiter)
            except ValueError:
                pass

    def notifyAll(self):
        self.notify(len(self.__waiters))


def Semaphore(*args, **kwargs):
    return _Semaphore(*args, **kwargs)


class _Semaphore(_Verbose):
    __module__ = __name__

    def __init__(self, value = 1, verbose = None):
        _Verbose.__init__(self, verbose)
        self.__cond = Condition(Lock())
        self.__value = value

    def acquire(self, blocking = 1):
        rc = False
        self.__cond.acquire()
        while self.__value == 0:
            if not blocking:
                break
            self.__cond.wait()
        else:
            self.__value = self.__value - 1
            rc = True

        self.__cond.release()
        return rc

    __enter__ = acquire

    def release(self):
        self.__cond.acquire()
        self.__value = self.__value + 1
        self.__cond.notify()
        self.__cond.release()

    def __exit__(self, t, v, tb):
        self.release()


def BoundedSemaphore(*args, **kwargs):
    return _BoundedSemaphore(*args, **kwargs)


class _BoundedSemaphore(_Semaphore):
    __module__ = __name__

    def __init__(self, value = 1, verbose = None):
        _Semaphore.__init__(self, value, verbose)
        self._initial_value = value

    def release(self):
        if self._Semaphore__value >= self._initial_value:
            raise ValueError, 'Semaphore released too many times'
        return _Semaphore.release(self)


def Event(*args, **kwargs):
    return _Event(*args, **kwargs)


class _Event(_Verbose):
    __module__ = __name__

    def __init__(self, verbose = None):
        _Verbose.__init__(self, verbose)
        self.__cond = Condition(Lock())
        self.__flag = False

    def isSet(self):
        return self.__flag

    def set(self):
        self.__cond.acquire()
        try:
            self.__flag = True
            self.__cond.notifyAll()
        finally:
            self.__cond.release()

    def clear(self):
        self.__cond.acquire()
        try:
            self.__flag = False
        finally:
            self.__cond.release()

    def wait(self, timeout = None):
        self.__cond.acquire()
        try:
            if not self.__flag:
                self.__cond.wait(timeout)
        finally:
            self.__cond.release()


_counter = 0

def _newname(template = 'Thread-%d'):
    global _counter
    _counter = _counter + 1
    return template % _counter


_active_limbo_lock = _allocate_lock()
_active = {}
_limbo = {}

class Thread(_Verbose):
    __module__ = __name__
    __initialized = False
    __exc_info = _sys.exc_info

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, verbose = None):
        _Verbose.__init__(self, verbose)
        if kwargs is None:
            kwargs = {}
        self.__target = target
        self.__name = str(name or _newname())
        self.__args = args
        self.__kwargs = kwargs
        self.__daemonic = self._set_daemon()
        self.__started = False
        self.__stopped = False
        self.__block = Condition(Lock())
        self.__initialized = True
        self.__stderr = _sys.stderr
        return

    def _set_daemon(self):
        return currentThread().isDaemon()

    def __repr__(self):
        status = 'initial'
        if self.__started:
            status = 'started'
        if self.__stopped:
            status = 'stopped'
        if self.__daemonic:
            status = status + ' daemon'
        return '<%s(%s, %s)>' % (self.__class__.__name__, self.__name, status)

    def start(self):
        _active_limbo_lock.acquire()
        _limbo[self] = self
        _active_limbo_lock.release()
        _start_new_thread(self.__bootstrap, ())
        self.__started = True
        _sleep(1e-06)

    def run(self):
        if self.__target:
            self.__target(*self.__args, **self.__kwargs)

    def __bootstrap(self):
        try:
            self.__started = True
            _active_limbo_lock.acquire()
            _active[_get_ident()] = self
            del _limbo[self]
            _active_limbo_lock.release()
            if _trace_hook:
                self._note('%s.__bootstrap(): registering trace hook', self)
                _sys.settrace(_trace_hook)
            if _profile_hook:
                self._note('%s.__bootstrap(): registering profile hook', self)
                _sys.setprofile(_profile_hook)
            try:
                self.run()
            except SystemExit:
                pass
            except:
                if _sys:
                    _sys.stderr.write('Exception in thread %s:\n%s\n' % (self.getName(), _format_exc()))
                else:
                    exc_type, exc_value, exc_tb = self.__exc_info()
                    try:
                        print >> self.__stderr, 'Exception in thread ' + self.getName() + ' (most likely raised during interpreter shutdown):'
                        print >> self.__stderr, 'Traceback (most recent call last):'
                        while exc_tb:
                            print >> self.__stderr, '  File "%s", line %s, in %s' % (exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_name)
                            exc_tb = exc_tb.tb_next

                        print >> self.__stderr, '%s: %s' % (exc_type, exc_value)
                    finally:
                        del exc_type
                        del exc_value
                        del exc_tb

        finally:
            self.__stop()
            try:
                self.__delete()
            except:
                pass

    def __stop(self):
        self.__block.acquire()
        self.__stopped = True
        self.__block.notifyAll()
        self.__block.release()

    def __delete(self):
        _active_limbo_lock.acquire()
        try:
            del _active[_get_ident()]
        except KeyError:
            if 'dummy_threading' not in _sys.modules:
                raise
        finally:
            _active_limbo_lock.release()

    def join(self, timeout = None):
        self.__block.acquire()
        try:
            if timeout is None:
                while not self.__stopped:
                    self.__block.wait()

            else:
                deadline = _time() + timeout
                while not self.__stopped:
                    delay = deadline - _time()
                    if delay <= 0:
                        break
                    self.__block.wait(delay)

        finally:
            self.__block.release()

        return

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = str(name)

    def isAlive(self):
        return self.__started and not self.__stopped

    def isDaemon(self):
        return self.__daemonic

    def setDaemon(self, daemonic):
        self.__daemonic = daemonic


def Timer(*args, **kwargs):
    return _Timer(*args, **kwargs)


class _Timer(Thread):
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


class _MainThread(Thread):
    __module__ = __name__

    def __init__(self):
        Thread.__init__(self, name='MainThread')
        self._Thread__started = True
        _active_limbo_lock.acquire()
        _active[_get_ident()] = self
        _active_limbo_lock.release()

    def _set_daemon(self):
        return False

    def _exitfunc(self):
        self._Thread__stop()
        t = _pickSomeNonDaemonThread()
        if t:
            pass
        while t:
            t.join()
            t = _pickSomeNonDaemonThread()

        self._Thread__delete()


def _pickSomeNonDaemonThread():
    for t in enumerate():
        if not t.isDaemon() and t.isAlive():
            return t

    return None


class _DummyThread(Thread):
    __module__ = __name__

    def __init__(self):
        Thread.__init__(self, name=_newname('Dummy-%d'))
        del self._Thread__block
        self._Thread__started = True
        _active_limbo_lock.acquire()
        _active[_get_ident()] = self
        _active_limbo_lock.release()

    def _set_daemon(self):
        return True

    def join(self, timeout = None):
        pass


def currentThread():
    try:
        return _active[_get_ident()]
    except KeyError:
        return _DummyThread()


def activeCount():
    _active_limbo_lock.acquire()
    count = len(_active) + len(_limbo)
    _active_limbo_lock.release()
    return count


def enumerate():
    _active_limbo_lock.acquire()
    active = _active.values() + _limbo.values()
    _active_limbo_lock.release()
    return active


_shutdown = _MainThread()._exitfunc

def _test():

    class BoundedQueue(_Verbose):
        __module__ = __name__

        def __init__(self, limit):
            _Verbose.__init__(self)
            self.mon = RLock()
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
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\stdpy\threading2.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:54 Pacific Daylight Time
