from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.task import Task

class DistributedAprilToonsMgrAI(DistributedObjectAI):  
    # Temp globals.
    RANDOM_CE_MIN_TIME = 3
    RANDOM_CE_MAX_TIME = 60
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.events = {
            'random-toon-dialogues' : True,
            'random-toon-effects' : True,
            'estate-low-gravity' : True,
            'global-low-gravity' : True,
        }
    
    def getEvents(self):
        return self.events
    
    def isEventActive(self, event):
        if not self.air.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False
        return self.events.get(event, False)
    
    def requestEventsList(self):
        avId = self.air.getAvatarIdFromSender()
        activeEvents = []
        inactiveEvents = []
        for event, active in self.events.iteritems():
            if active:
                activeEvents.append(event)
            else:
                inactiveEvents.append(event)
        self.sendUpdateToAvatarId(avId, 'requestEventsListResp', [activeEvents, inactiveEvents])
    
    def setEventActive(self, event, active):
        if event in self.getEvents():
            self.events[event] = active
            self.sendUpdate('setEventActive', [event, active])

@magicWord(category=CATEGORY_OVERRIDE, types=[str, str])
def apriltoons(event, active):
    activebool = True if active=='on' else False
    if hasattr(simbase.air, 'aprilToonsMgr') and event in simbase.air.aprilToonsMgr.getEvents():
        simbase.air.aprilToonsMgr.setEventActive(event, activebool)
        return 'April Toons event %s set to %s.' % (event, active)
    return 'Unable to set April Toons event %s to %s.' % (event, active)
    
@magicWord(category=CATEGORY_OVERRIDE, access=300)
def randomce():
    """Add a flag to the target toon to enable/disable random cheesy effects (April Fools event)"""
    if not hasattr(simbase.air, 'aprilToonsMgr'):
        return "The AIR doesn't have the April Toons Manager generated."
    mgr = simbase.air.aprilToonsMgr
    if not mgr.isEventActive('random-toon-effects'):
        return "random-toon-effects is currently disabled!"
    av = spellbook.getTarget()
    av.wantRandomEffects = not av.wantRandomEffects
    enabledOrDisabled = "enabled" if av.wantRandomEffects else "disabled"
    if av.wantRandomEffects:
        # Start a task which loops to give the effect(s).
        taskMgr.doMethodLater(random.randint(mgr.RANDOM_CE_MIN_TIME, mgr.RANDOM_CE_MAX_TIME), av.randomToonEffects, av.uniqueName('random-toon-effects'))
    else:
        av.b_setCheesyEffect(0, 0, 0)
    return "random-toon-effects %s for %s." % (enabledOrDisabled, av.getName())
    