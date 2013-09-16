# 2013.08.22 22:14:11 Pacific Daylight Time
# Embedded file name: direct.fsm.StateData
__all__ = ['StateData']
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal

class StateData(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('StateData')

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.doneStatus = None
        self.isLoaded = 0
        self.isEntered = 0
        return

    def enter(self):
        if self.isEntered:
            return 0
        if not self.isLoaded:
            self.notify.warning('entered StateData before it was loaded')
            self.load()
        self.isEntered = 1
        StateData.notify.debug('enter()')
        return 1

    def exit(self):
        if not self.isEntered:
            return 0
        self.isEntered = 0
        StateData.notify.debug('exit()')
        return 1

    def load(self):
        if self.isLoaded:
            return 0
        self.isLoaded = 1
        StateData.notify.debug('load()')
        return 1

    def unload(self):
        if not self.isLoaded:
            return 0
        if self.isEntered:
            self.notify.warning('unloaded StateData before it was exited')
            self.exit()
        self.isLoaded = 0
        StateData.notify.debug('unload()')
        return 1

    def getDoneStatus(self):
        return self.doneStatus
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\fsm\StateData.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:12 Pacific Daylight Time
