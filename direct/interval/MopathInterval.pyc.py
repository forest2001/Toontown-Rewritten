# 2013.08.22 22:14:24 Pacific Daylight Time
# Embedded file name: direct.interval.MopathInterval
__all__ = ['MopathInterval']
import LerpInterval
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *

class MopathInterval(LerpInterval.LerpFunctionInterval):
    __module__ = __name__
    mopathNum = 1
    notify = directNotify.newCategory('MopathInterval')

    def __init__(self, mopath, node, fromT = 0, toT = None, duration = None, blendType = 'noBlend', name = None):
        if toT == None:
            toT = mopath.getMaxT()
        if duration == None:
            duration = abs(toT - fromT)
        if name == None:
            name = 'Mopath-%d' % MopathInterval.mopathNum
            MopathInterval.mopathNum += 1
        LerpInterval.LerpFunctionInterval.__init__(self, self.__doMopath, fromData=fromT, toData=toT, duration=duration, blendType=blendType, name=name)
        self.mopath = mopath
        self.node = node
        return

    def destroy(self):
        self.function = None
        return

    def __doMopath(self, t):
        self.mopath.goTo(self.node, t)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\interval\MopathInterval.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:24 Pacific Daylight Time
