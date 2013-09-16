# 2013.08.22 22:23:10 Pacific Daylight Time
# Embedded file name: toontown.parties.BaseActivityFSM
from direct.fsm.FSM import FSM
from direct.directnotify import DirectNotifyGlobal

class BaseActivityFSM(FSM):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BaseActivityFSM')

    def __init__(self, activity):
        FSM.__init__(self, self.__class__.__name__)
        self.activity = activity
        self.defaultTransitions = None
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\BaseActivityFSM.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:10 Pacific Daylight Time
