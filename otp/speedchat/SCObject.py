# 2013.08.22 22:15:49 Pacific Daylight Time
# Embedded file name: otp.speedchat.SCObject
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

class SCObject(DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('SpeedChat')

    def __init__(self):
        self.settingsRef = None
        self.__visible = 0
        self.__dirty = 1
        return

    def destroy(self):
        self.ignoreAll()
        if self.isVisible():
            self.exitVisible()

    def enterVisible(self):
        self.__visible = 1

    def exitVisible(self):
        self.__visible = 0

    def isVisible(self):
        return self.__visible

    def invalidate(self):
        self.__dirty = 1

    def isDirty(self):
        return self.__dirty

    def validate(self):
        self.__dirty = 0

    def finalize(self):
        pass

    def getEventName(self, name):
        return '%s%s' % (self.settingsRef.eventPrefix, name)

    def getColorScheme(self):
        return self.settingsRef.colorScheme

    def isWhispering(self):
        return self.settingsRef.whisperMode

    def getSubmenuOverlap(self):
        return self.settingsRef.submenuOverlap

    def getTopLevelOverlap(self):
        if self.settingsRef.topLevelOverlap is None:
            return self.getSubmenuOverlap()
        else:
            return self.settingsRef.topLevelOverlap
        return

    def privSetSettingsRef(self, settingsRef):
        self.settingsRef = settingsRef

    def privAdoptSCObject(self, scObj):
        scObj.privSetSettingsRef(self.settingsRef)

    def invalidateAll(self):
        self.invalidate()

    def finalizeAll(self):
        self.finalize()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\speedchat\SCObject.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:49 Pacific Daylight Time
