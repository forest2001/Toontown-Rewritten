# 2013.08.22 22:14:56 Pacific Daylight Time
# Embedded file name: distutils.log
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5
import sys

class Log():
    __module__ = __name__

    def __init__(self, threshold = WARN):
        self.threshold = threshold

    def _log(self, level, msg, args):
        if level >= self.threshold:
            print msg % args
            sys.stdout.flush()

    def log(self, level, msg, *args):
        self._log(level, msg, args)

    def debug(self, msg, *args):
        self._log(DEBUG, msg, args)

    def info(self, msg, *args):
        self._log(INFO, msg, args)

    def warn(self, msg, *args):
        self._log(WARN, msg, args)

    def error(self, msg, *args):
        self._log(ERROR, msg, args)

    def fatal(self, msg, *args):
        self._log(FATAL, msg, args)


_global_log = Log()
log = _global_log.log
debug = _global_log.debug
info = _global_log.info
warn = _global_log.warn
error = _global_log.error
fatal = _global_log.fatal

def set_threshold(level):
    old = _global_log.threshold
    _global_log.threshold = level
    return old


def set_verbosity(v):
    if v <= 0:
        set_threshold(WARN)
    elif v == 1:
        set_threshold(INFO)
    elif v >= 2:
        set_threshold(DEBUG)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\distutils\log.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:56 Pacific Daylight Time
