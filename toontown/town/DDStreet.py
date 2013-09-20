# 2013.08.22 22:26:47 Pacific Daylight Time
# Embedded file name: toontown.town.DDStreet
import Street

class DDStreet(Street.Street):
    __module__ = __name__

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)

    def enter(self, requestStatus):
        self.loader.hood.setWhiteFog()
        Street.Street.enter(self, requestStatus)

    def exit(self):
        self.loader.hood.setNoFog()
        Street.Street.exit(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\town\DDStreet.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:47 Pacific Daylight Time
