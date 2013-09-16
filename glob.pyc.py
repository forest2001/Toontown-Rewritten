# 2013.08.22 22:13:03 Pacific Daylight Time
# Embedded file name: glob
import os
import fnmatch
import re
__all__ = ['glob']

def glob(pathname):
    if not has_magic(pathname):
        if os.path.lexists(pathname):
            return [pathname]
        else:
            return []
    dirname, basename = os.path.split(pathname)
    if not dirname:
        return glob1(os.curdir, basename)
    elif has_magic(dirname):
        list = glob(dirname)
    else:
        list = [dirname]
    if not has_magic(basename):
        result = []
        for dirname in list:
            if basename or os.path.isdir(dirname):
                name = os.path.join(dirname, basename)
                if os.path.lexists(name):
                    result.append(name)

    else:
        result = []
        for dirname in list:
            sublist = glob1(dirname, basename)
            for name in sublist:
                result.append(os.path.join(dirname, name))

    return result


def glob1(dirname, pattern):
    if not dirname:
        dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except os.error:
        return []

    if pattern[0] != '.':
        names = filter(lambda x: x[0] != '.', names)
    return fnmatch.filter(names, pattern)


magic_check = re.compile('[*?[]')

def has_magic(s):
    return magic_check.search(s) is not None
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\glob.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:03 Pacific Daylight Time
