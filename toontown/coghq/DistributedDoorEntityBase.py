# 2013.08.22 22:18:34 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedDoorEntityBase


def stubFunction(*args):
    pass


class LockBase():
    __module__ = __name__
    stateNames = ['off',
     'locking',
     'locked',
     'unlocking',
     'unlocked']
    stateDurations = [None,
     3.5,
     None,
     4.0,
     None]


class DistributedDoorEntityBase():
    __module__ = __name__
    stateNames = ['off',
     'opening',
     'open',
     'closing',
     'closed']
    stateDurations = [None,
     5.0,
     1.0,
     6.0,
     None]
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedDoorEntityBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:34 Pacific Daylight Time
