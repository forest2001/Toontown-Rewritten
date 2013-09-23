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
