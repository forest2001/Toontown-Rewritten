# 2013.08.22 22:17:30 Pacific Daylight Time
# Embedded file name: toontown.classicchars.DistributedSockHopDaisy
from direct.showbase.ShowBaseGlobal import *
import DistributedCCharBase
import DistributedDaisy
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import TTHood

class DistributedSockHopDaisy(DistributedDaisy.DistributedDaisy):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSockHopDaisy')

    def __init__(self, cr):
        try:
            self.DistributedSockHopDaisy_initialized
        except:
            self.DistributedSockHopDaisy_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr, TTLocalizer.SockHopDaisy, 'shdd')
            self.fsm = ClassicFSM.ClassicFSM(self.getName(), [State.State('Off', self.enterOff, self.exitOff, ['Neutral']), State.State('Neutral', self.enterNeutral, self.exitNeutral, ['Walk']), State.State('Walk', self.enterWalk, self.exitWalk, ['Neutral'])], 'Off', 'Off')
            self.fsm.enterInitialState()
            self.nametag.setName(TTLocalizer.Daisy)
            self.handleHolidays()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\classicchars\DistributedSockHopDaisy.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:31 Pacific Daylight Time
