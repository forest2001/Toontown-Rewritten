from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class DistributedAprilToonsMgr(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('AprilToonsMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.events = {}

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.d_requestEventsList()
        
    def d_requestEventsList(self):
        self.notify.debug("Requesting events list from AI.")
        self.sendUpdate('requestEventsList', [])
        
    def requestEventsListResp(self, activeEvents, inactiveEvents):
        self.notify.debug("Got events list response from AI.")
        for event in activeEvents:
            self.events[event] = True
        for event in inactiveEvents:
            self.events[event] = False

    def isEventActive(self, event):
        # NOTE: Possible race condition where the client checks for if an event is active
        # *before* it gets a response from the AI.
    
        if not base.cr.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False
            
        return self.events.get(event, False)

    def setEventActive(self, event, active):
        if event in self.getEvents():
            self.events[event] = active
            return True
        return False
