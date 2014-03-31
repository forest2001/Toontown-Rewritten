from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *

class DistributedAprilToonsMgrAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.events = {
            'random-toon-dialogues' : True,
            'random-toon-effects' : True,
        }
    
    def getEvents(self):
        return self.events
        
    def isEventActive(self, event):
        if not self.air.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False
        if event in self.events:
            return self.events.get(event)
        return False
        
    def setEventActive(self, event, active):
        if event in self.getEvents():
            self.events[event] = active
            return True
        return False

@magicWord(category=CATEGORY_OVERRIDE, types=[str, str])
def apriltoons(event, active):
    activebool = True if active=='on' else False
    if hasattr(simbase.air, 'aprilToonsMgr') and event in simbase.air.aprilToonsMgr.getEvents():
        simbase.air.aprilToonsMgr.setEventActive(event, activebool)
        return 'April Toons event %s set to %s.' % (event, active)
    return 'Unable to set April Toons event %s to %s.' % (event, active)