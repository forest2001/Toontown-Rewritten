# 2013.08.22 22:12:52 Pacific Daylight Time
# Embedded file name: bisect


def insort_right(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        else:
            lo = mid + 1

    a.insert(lo, x)
    return


insort = insort_right

def bisect_right(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        else:
            lo = mid + 1

    return lo


bisect = bisect_right

def insort_left(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid

    a.insert(lo, x)
    return


def bisect_left(a, x, lo = 0, hi = None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid

    return lo


try:
    from _bisect import bisect_right, bisect_left, insort_left, insort_right, insort, bisect
except ImportError:
    pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\bisect.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:12:52 Pacific Daylight Time
