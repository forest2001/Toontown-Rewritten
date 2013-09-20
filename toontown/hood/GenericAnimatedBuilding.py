# 2013.08.22 22:20:52 Pacific Daylight Time
# Embedded file name: toontown.hood.GenericAnimatedBuilding
from toontown.hood import GenericAnimatedProp

class GenericAnimatedBuilding(GenericAnimatedProp.GenericAnimatedProp):
    __module__ = __name__

    def __init__(self, node):
        GenericAnimatedProp.GenericAnimatedProp.__init__(self, node)

    def enter(self):
        if base.config.GetBool('buildings-animate', False):
            GenericAnimatedProp.GenericAnimatedProp.enter(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\GenericAnimatedBuilding.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:52 Pacific Daylight Time
