from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from direct.distributed.ClockDelta import *
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from toontown.toonbase import ToontownGlobals

import FireworkShows
import random

class DistributedFireworkShowAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFireworkShowAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
    
    def startShow(self, eventId, style, timeStamp):
        taskMgr.doMethodLater(FireworkShows.getShowDuration(eventId, style), self.requestDelete, 'delete%i' % self.doId, [])
        
    def d_startShow(self, eventId, style, timeStamp):
        self.sendUpdate('startShow', [eventId, style, timeStamp])
    
    def b_startShow(self, eventId, style, timeStamp):
        self.startShow(eventId, style, timeStamp)
        self.d_startShow(eventId, style, timeStamp)

    def requestFirework(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def shootFirework(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass


@magicWord(category=CATEGORY_OVERRIDE, types=[str])
def fireworks(showName='july4'):
    if showName == 'july4':
        showType = ToontownGlobals.JULY4_FIREWORKS
    elif showName == 'newyears':
        showType = ToontownGlobals.NEWYEARS_FIREWORKS
    else:
        return 'Invalid firework show type!'
    numShows = len(FireworkShows.shows.get(showType, []))
    showIndex = random.randint(0, numShows - 1)
    for hood in simbase.air.hoods:
        if hood.safezone == ToontownGlobals.GolfZone:
            continue
        fireworksShow = DistributedFireworkShowAI(simbase.air)
        fireworksShow.generateWithRequired(hood.safezone)
        fireworksShow.b_startShow(showType, showIndex, globalClockDelta.getRealNetworkTime())
    return 'Started fireworks in all playgrounds!'