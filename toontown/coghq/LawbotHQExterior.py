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
