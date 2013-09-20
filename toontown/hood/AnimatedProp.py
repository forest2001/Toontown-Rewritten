# 2013.08.22 22:20:50 Pacific Daylight Time
# Embedded file name: toontown.hood.AnimatedProp
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal

class AnimatedProp(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('AnimatedProp')

    def __init__(self, node):
        self.node = node

    def delete(self):
        pass

    def uniqueName(self, name):
        return name + '-' + str(self.node.this)

    def enter(self):
        self.notify.debug('enter')

    def exit(self):
        self.notify.debug('exit')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\AnimatedProp.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:50 Pacific Daylight Time
