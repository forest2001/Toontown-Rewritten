# 2013.08.22 22:12:59 Pacific Daylight Time
# Embedded file name: dummy_thread
__author__ = 'Brett Cannon'
__email__ = 'brett@python.org'
__all__ = ['error',
 'start_new_thread',
 'exit',
 'get_ident',
 'allocate_lock',
 'interrupt_main',
 'LockType']
import traceback as _traceback

class error(Exception):
    __module__ = __name__

    def __init__(self, *args):
        self.args = args


def start_new_thread(function, args, kwargs = {}):
    global _interrupt
    global _main
    if type(args) != type(tuple()):
        raise TypeError('2nd arg must be a tuple')
    if type(kwargs) != type(dict()):
        raise TypeError('3rd arg must be a dict')
    _main = False
    try:
        function(*args, **kwargs)
    except SystemExit:
        pass
    except:
        _traceback.print_exc()

    _main = True
    if _interrupt:
        _interrupt = False
        raise KeyboardInterrupt


def exit():
    raise SystemExit


def get_ident():
    return -1


def allocate_lock():
    return LockType()


class LockType(object):
    __module__ = __name__

    def __init__(self):
        self.locked_status = False

    def acquire(self, waitflag = None):
        if waitflag is None:
            self.locked_status = True
            return
        elif not waitflag:
            if not self.locked_status:
                self.locked_status = True
                return True
            else:
                return False
        else:
            self.locked_status = True
            return True
        return

    def release(self):
        if not self.locked_status:
            raise error
        self.locked_status = False
        return True

    def locked(self):
        return self.locked_status


_interrupt = False
_main = True

def interrupt_main():
    global _interrupt
    if _main:
        raise KeyboardInterrupt
    else:
        _interrupt = True
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\dummy_thread.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:59 Pacific Daylight Time
