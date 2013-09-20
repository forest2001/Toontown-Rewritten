# 2013.08.22 22:19:07 Pacific Daylight Time
# Embedded file name: toontown.coghq.LawbotHQExterior
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.building import Elevator
from pandac.PandaModules import *
from toontown.coghq import CogHQExterior

class LawbotHQExterior(CogHQExterior.CogHQExterior):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotHQExterior')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\LawbotHQExterior.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:07 Pacific Daylight Time
