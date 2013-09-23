

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
