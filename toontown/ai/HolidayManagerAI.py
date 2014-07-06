from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.task import Task

from toontown.toonbase import ToontownGlobals
from toontown.parties import PartyGlobals

from toontown.effects.DistributedFireworkShowAI import DistributedFireworkShowAI
from toontown.effects import FireworkShows

import random
import time

class HolidayManagerAI:
	# notify = directNotify.newCategory('HolidayManagerAI')
    def __init__(self, air):
    	self.air = air
        self.currentHolidays = []

        # TODO: Properly create a holiday manager to run this.
        if config.GetBool('want-hourly-fireworks', False):
            self.__startFireworksTick()

    """
    Fireworks Stuff
    """
    def __startFireworksTick(self):
        # Check seconds until next hour.
        ts = time.time()
        nextHour = 3600 - (ts % 3600)
        taskMgr.doMethodLater(nextHour, self.__fireworksTick, 'hourly-fireworks')

    def __fireworksTick(self, task):
        # The next tick will occur in exactly an hour.
        task.delayTime = 3600

        showName = config.GetString('hourly-fireworks-type', 'july4')

        if showName == 'july4':
            showType = ToontownGlobals.JULY4_FIREWORKS

        elif showName == 'newyears':
            showType = ToontownGlobals.NEWYEARS_FIREWORKS

        elif showName == 'summer':
            showType = PartyGlobals.FireworkShows.Summer

        elif showName == 'random':
            shows = [ToontownGlobals.JULY4_FIREWORKS, ToontownGlobals.NEWYEARS_FIREWORKS, PartyGlobals.FireworkShows.Summer]
            showType = random.choice(shows)
        else:
            raise AttributeError('%s is an invalid firework type' % showName)
            return

        numShows = len(FireworkShows.shows.get(showType, []))
        showIndex = random.randint(0, numShows - 1)
        for hood in self.air.hoods:
            if hood.HOOD == ToontownGlobals.GolfZone:
                continue
            fireworksShow = DistributedFireworkShowAI(self.air)
            fireworksShow.generateWithRequired(hood.HOOD)
            fireworksShow.b_startShow(showType, showIndex, globalClockDelta.getRealNetworkTime())
        return task.again
        
    def isHolidayRunning(self, *args):
        return True
        #TODO: this function needs to actually check holidays
