# 2013.08.22 22:13:42 Pacific Daylight Time
# Embedded file name: _threading_local


class _localbase(object):
    __module__ = __name__
    __slots__ = ('_local__key', '_local__args', '_local__lock')

    def __new__(cls, *args, **kw):
        self = object.__new__(cls)
        key = ('_local__key', 'thread.local.' + str(id(self)))
        object.__setattr__(self, '_local__key', key)
        object.__setattr__(self, '_local__args', (args, kw))
        object.__setattr__(self, '_local__lock', RLock())
        if args or kw and cls.__init__ is object.__init__:
            raise TypeError('Initialization arguments are not supported')
        dict = object.__getattribute__(self, '__dict__')
        currentThread().__dict__[key] = dict
        return self


def _patch(self):
    key = object.__getattribute__(self, '_local__key')
    d = currentThread().__dict__.get(key)
    if d is None:
        d = {}
        currentThread().__dict__[key] = d
        object.__setattr__(self, '__dict__', d)
        cls = type(self)
        if cls.__init__ is not object.__init__:
            args, kw = object.__getattribute__(self, '_local__args')
            cls.__init__(self, *args, **kw)
    else:
        object.__setattr__(self, '__dict__', d)
    return


class local(_localbase):
    __module__ = __name__

    def __getattribute__(self, name):
        lock = object.__getattribute__(self, '_local__lock')
        lock.acquire()
        try:
            _patch(self)
            return object.__getattribute__(self, name)
        finally:
            lock.release()

    def __setattr__(self, name, value):
        lock = object.__getattribute__(self, '_local__lock')
        lock.acquire()
        try:
            _patch(self)
            return object.__setattr__(self, name, value)
        finally:
            lock.release()

    def __delattr__(self, name):
        lock = object.__getattribute__(self, '_local__lock')
        lock.acquire()
        try:
            _patch(self)
            return object.__delattr__(self, name)
        finally:
            lock.release()

    def __del__():
        threading_enumerate = enumerate
        __getattribute__ = object.__getattribute__

        def __del__(self):
            key = __getattribute__(self, '_local__key')
            try:
                threads = list(threading_enumerate())
            except:
                return

            for thread in threads:
                try:
                    __dict__ = thread.__dict__
                except AttributeError:
                    continue

                if key in __dict__:
                    try:
                        del __dict__[key]
                    except KeyError:
                        pass

        return __del__

    __del__ = __del__()


from threading import currentThread, enumerate, RLock
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\_threading_local.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:43 Pacific Daylight Time
