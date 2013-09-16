# 2013.08.22 22:12:51 Pacific Daylight Time
# Embedded file name: anydbm


class error(Exception):
    __module__ = __name__


_names = ['dbhash',
 'gdbm',
 'dbm',
 'dumbdbm']
_errors = [error]
_defaultmod = None
for _name in _names:
    try:
        _mod = __import__(_name)
    except ImportError:
        continue

    if not _defaultmod:
        _defaultmod = _mod
    _errors.append(_mod.error)

if not _defaultmod:
    raise ImportError, 'no dbm clone found; tried %s' % _names
error = tuple(_errors)

def open(file, flag = 'r', mode = 438):
    from whichdb import whichdb
    result = whichdb(file)
    if result is None:
        if 'c' in flag or 'n' in flag:
            mod = _defaultmod
        else:
            raise error, "need 'c' or 'n' flag to open new db"
    elif result == '':
        raise error, 'db type could not be determined'
    else:
        mod = __import__(result)
    return mod.open(file, flag, mode)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\anydbm.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:51 Pacific Daylight Time
