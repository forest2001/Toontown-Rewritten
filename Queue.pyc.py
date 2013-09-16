# 2013.08.22 22:13:23 Pacific Daylight Time
# Embedded file name: Queue
from time import time as _time
from collections import deque
__all__ = ['Empty', 'Full', 'Queue']

class Empty(Exception):
    __module__ = __name__


class Full(Exception):
    __module__ = __name__


class Queue():
    __module__ = __name__

    def __init__(self, maxsize = 0):
        try:
            import threading
        except ImportError:
            import dummy_threading as threading

        self._init(maxsize)
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)

    def qsize(self):
        self.mutex.acquire()
        n = self._qsize()
        self.mutex.release()
        return n

    def empty(self):
        self.mutex.acquire()
        n = self._empty()
        self.mutex.release()
        return n

    def full(self):
        self.mutex.acquire()
        n = self._full()
        self.mutex.release()
        return n

    def put(self, item, block = True, timeout = None):
        self.not_full.acquire()
        try:
            if not block:
                if self._full():
                    raise Full
            elif timeout is None:
                while self._full():
                    self.not_full.wait()

            else:
                if timeout < 0:
                    raise ValueError("'timeout' must be a positive number")
                endtime = _time() + timeout
                while self._full():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Full
                    self.not_full.wait(remaining)

            self._put(item)
            self.not_empty.notify()
        finally:
            self.not_full.release()

        return

    def put_nowait(self, item):
        return self.put(item, False)

    def get(self, block = True, timeout = None):
        self.not_empty.acquire()
        try:
            if not block:
                if self._empty():
                    raise Empty
            elif timeout is None:
                while self._empty():
                    self.not_empty.wait()

            else:
                if timeout < 0:
                    raise ValueError("'timeout' must be a positive number")
                endtime = _time() + timeout
                while self._empty():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)

            item = self._get()
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

        return

    def get_nowait(self):
        return self.get(False)

    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = deque()

    def _qsize(self):
        return len(self.queue)

    def _empty(self):
        return not self.queue

    def _full(self):
        return self.maxsize > 0 and len(self.queue) == self.maxsize

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.popleft()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\Queue.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:23 Pacific Daylight Time
