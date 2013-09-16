# 2013.08.22 22:13:43 Pacific Daylight Time
# Embedded file name: ctypes.decorators
import sys
import ctypes
LOGGING = False

def stdcall(restype, dll, argtypes, logging = False):

    def decorate(func):
        if isinstance(dll, basestring):
            this_dll = ctypes.CDLL(dll)
        else:
            this_dll = dll
        api = ctypes.WINFUNCTYPE(restype, *argtypes)(func.func_name, this_dll)
        func._api_ = api
        if logging or LOGGING:

            def f(*args):
                result = func(*args)
                print >> sys.stderr, '# function call: %s%s -> %s' % (func.func_name, args, result)
                return result

            return f
        else:
            return func

    return decorate


def cdecl(restype, dll, argtypes, logging = False):

    def decorate(func):
        if isinstance(dll, basestring):
            this_dll = ctypes.CDLL(dll)
        else:
            this_dll = dll
        api = ctypes.CFUNCTYPE(restype, *argtypes)(func.func_name, this_dll)
        func._api_ = api
        if logging or LOGGING:

            def f(*args):
                result = func(*args)
                print >> sys.stderr, func.func_name, args, '->', result
                return result

            return f
        else:
            return func

    return decorate
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\ctypes\decorators.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:43 Pacific Daylight Time
