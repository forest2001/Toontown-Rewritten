# 2013.08.22 22:13:08 Pacific Daylight Time
# Embedded file name: linecache
import sys
import os
__all__ = ['getline', 'clearcache', 'checkcache']

def getline(filename, lineno):
    lines = getlines(filename)
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1]
    else:
        return ''


cache = {}

def clearcache():
    global cache
    cache = {}


def getlines(filename):
    if filename in cache:
        return cache[filename][2]
    else:
        return updatecache(filename)


def checkcache(filename = None):
    if filename is None:
        filenames = cache.keys()
    elif filename in cache:
        filenames = [filename]
    else:
        return
    for filename in filenames:
        size, mtime, lines, fullname = cache[filename]
        try:
            stat = os.stat(fullname)
        except os.error:
            del cache[filename]
            continue

        if size != stat.st_size or mtime != stat.st_mtime:
            del cache[filename]

    return


def updatecache(filename):
    if filename in cache:
        del cache[filename]
    if not filename or filename[0] + filename[-1] == '<>':
        return []
    fullname = filename
    try:
        stat = os.stat(fullname)
    except os.error as msg:
        basename = os.path.split(filename)[1]
        for dirname in sys.path:
            try:
                fullname = os.path.join(dirname, basename)
            except (TypeError, AttributeError):
                pass
            else:
                try:
                    stat = os.stat(fullname)
                    break
                except os.error:
                    pass

        else:
            return []

    try:
        fp = open(fullname, 'rU')
        lines = fp.readlines()
        fp.close()
    except IOError as msg:
        return []

    size, mtime = stat.st_size, stat.st_mtime
    cache[filename] = (size,
     mtime,
     lines,
     fullname)
    return lines
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\linecache.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:08 Pacific Daylight Time
