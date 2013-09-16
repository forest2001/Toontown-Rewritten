# 2013.08.22 22:19:11 Pacific Daylight Time
# Embedded file name: toontown.coghq.LawbotOfficeExterior
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.building import Elevator
from pandac.PandaModules import *
import FactoryExterior

class LawbotOfficeExterior(FactoryExterior.FactoryExterior):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotOfficeExterior')

    def enterWalk(self, teleportIn = 0):
        FactoryExterior.FactoryExterior.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\LawbotOfficeExterior.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:11 Pacific Daylight Time
