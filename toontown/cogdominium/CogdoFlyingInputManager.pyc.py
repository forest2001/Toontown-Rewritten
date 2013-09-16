# 2013.08.22 22:17:36 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.CogdoFlyingInputManager
from pandac.PandaModules import CollisionSphere, CollisionNode, BitMask32, CollisionHandlerEvent, CollisionRay
from toontown.minigame import ArrowKeys

class CogdoFlyingInputManager():
    __module__ = __name__

    def __init__(self):
        self.arrowKeys = ArrowKeys.ArrowKeys()
        self.arrowKeys.disable()

    def enable(self):
        self.arrowKeys.setPressHandlers([self.__upArrowPressed,
         self.__downArrowPressed,
         self.__leftArrowPressed,
         self.__rightArrowPressed,
         self.__controlPressed])
        self.arrowKeys.enable()

    def disable(self):
        self.arrowKeys.clearPressHandlers()
        self.arrowKeys.disable()

    def destroy(self):
        self.disable()
        self.arrowKeys.destroy()
        self.arrowKeys = None
        self.refuelLerp = None
        return

    def __upArrowPressed(self):
        pass

    def __downArrowPressed(self):
        pass

    def __leftArrowPressed(self):
        pass

    def __rightArrowPressed(self):
        pass

    def __controlPressed(self):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\CogdoFlyingInputManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:36 Pacific Daylight Time
