# 2013.08.22 22:23:10 Pacific Daylight Time
# Embedded file name: toontown.parties.activityFSMs
from direct.directnotify import DirectNotifyGlobal
from BaseActivityFSM import BaseActivityFSM
from activityFSMMixins import IdleMixin
from activityFSMMixins import RulesMixin
from activityFSMMixins import ActiveMixin
from activityFSMMixins import DisabledMixin
from activityFSMMixins import ConclusionMixin
from activityFSMMixins import WaitForEnoughMixin
from activityFSMMixins import WaitToStartMixin
from activityFSMMixins import WaitClientsReadyMixin
from activityFSMMixins import WaitForServerMixin

class FireworksActivityFSM(BaseActivityFSM, IdleMixin, ActiveMixin, DisabledMixin):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FireworksActivityFSM')

    def __init__(self, activity):
        FireworksActivityFSM.notify.debug('__init__')
        BaseActivityFSM.__init__(self, activity)
        self.defaultTransitions = {'Idle': ['Active', 'Disabled'],
         'Active': ['Disabled'],
         'Disabled': []}


class CatchActivityFSM(BaseActivityFSM, IdleMixin, ActiveMixin, ConclusionMixin):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CatchActivityFSM')

    def __init__(self, activity):
        CatchActivityFSM.notify.debug('__init__')
        BaseActivityFSM.__init__(self, activity)
        self.defaultTransitions = {'Idle': ['Active', 'Conclusion'],
         'Active': ['Conclusion'],
         'Conclusion': ['Idle']}


class TrampolineActivityFSM(BaseActivityFSM, IdleMixin, RulesMixin, ActiveMixin):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TrampolineActivityFSM')

    def __init__(self, activity):
        TrampolineActivityFSM.notify.debug('__init__')
        BaseActivityFSM.__init__(self, activity)
        self.defaultTransitions = {'Idle': ['Rules', 'Active'],
         'Rules': ['Active', 'Idle'],
         'Active': ['Idle']}


class DanceActivityFSM(BaseActivityFSM, IdleMixin, ActiveMixin, DisabledMixin):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DanceActivityFSM')

    def __init__(self, activity):
        DanceActivityFSM.notify.debug('__init__')
        BaseActivityFSM.__init__(self, activity)
        self.defaultTransitions = {'Active': ['Disabled'],
         'Disabled': ['Active']}


class TeamActivityAIFSM(BaseActivityFSM, WaitForEnoughMixin, WaitToStartMixin, WaitClientsReadyMixin, ActiveMixin, ConclusionMixin):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TeamActivityAIFSM')

    def __init__(self, activity):
        BaseActivityFSM.__init__(self, activity)
        self.notify.debug('__init__')
        self.defaultTransitions = {'WaitForEnough': ['WaitToStart'],
         'WaitToStart': ['WaitForEnough', 'WaitClientsReady'],
         'WaitClientsReady': ['WaitForEnough', 'Active'],
         'Active': ['WaitForEnough', 'Conclusion'],
         'Conclusion': ['WaitForEnough']}


class TeamActivityFSM(BaseActivityFSM, WaitForEnoughMixin, WaitToStartMixin, RulesMixin, WaitForServerMixin, ActiveMixin, ConclusionMixin):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TeamActivityFSM')

    def __init__(self, activity):
        BaseActivityFSM.__init__(self, activity)
        self.defaultTransitions = {'WaitForEnough': ['WaitToStart'],
         'WaitToStart': ['WaitForEnough', 'Rules'],
         'Rules': ['WaitForServer', 'Active', 'WaitForEnough'],
         'WaitForServer': ['Active', 'WaitForEnough'],
         'Active': ['Conclusion', 'WaitForEnough'],
         'Conclusion': ['WaitForEnough']}
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\activityFSMs.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:10 Pacific Daylight Time
