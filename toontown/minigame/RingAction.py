# 2013.08.22 22:22:57 Pacific Daylight Time
# Embedded file name: toontown.minigame.RingAction
from direct.directnotify import DirectNotifyGlobal
import RingTrack

class RingAction():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('RingAction')

    def __init__(self):
        pass

    def eval(self, t):
        return (0, 0)


class RingActionStaticPos(RingAction):
    __module__ = __name__

    def __init__(self, pos):
        RingAction.__init__(self)
        self.__pos = pos

    def eval(self, t):
        return self.__pos


class RingActionFunction(RingAction):
    __module__ = __name__

    def __init__(self, func, args):
        RingAction.__init__(self)
        self.__func = func
        self.__args = args

    def eval(self, t):
        return self.__func(t, *self.__args)


class RingActionRingTrack(RingAction):
    __module__ = __name__

    def __init__(self, ringTrack):
        RingAction.__init__(self)
        self.__track = ringTrack

    def eval(self, t):
        return self.__track.eval(t)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\RingAction.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:58 Pacific Daylight Time
