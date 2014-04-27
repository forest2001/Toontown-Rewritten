from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.task import Task
from toontown.toonbase.AprilToonsGlobals import *

class DistributedAprilToonsMgrAI(DistributedObjectAI):  
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        # Define the default events we want for this year
        self.events = [EventRandomDialogue,
                       EventRandomEffects,
                       EventEstateGravity,
                       EventGlobalGravity]
    
    def getEvents(self):
        return self.events
    
    def isEventActive(self, eventId):
        if not self.air.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False
        return eventId in self.events
    
    def requestEventsList(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'requestEventsListResp', [self.getEvents()])
    
    def toggleEvent(self, eventId):
        if eventId in self.getEvents():
            del self.getEvents()[eventId]
            self.sendUpdate('setEventActive', [eventId, False])
        else:
            self.getEvents().append(eventId)
            self.sendUpdate('setEventActive', [eventId, True])


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
        taskMgr.doMethodLater(random.randint(RandomCheesyMinTime, RandomCheesyMaxTime), av.randomToonEffects, av.uniqueName('random-toon-effects'))
    else:
        av.b_setCheesyEffect(0, 0, 0)
    return "random-toon-effects %s for %s." % (enabledOrDisabled, av.getName())
    