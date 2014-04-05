from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import AprilToonsGlobals

class DistributedAprilToonsMgr(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('AprilToonsMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        cr.aprilToonsMgr = self
        self.events = []

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.d_requestEventsList()
        
    def d_requestEventsList(self):
        self.notify.debug("Requesting events list from AI.")
        self.sendUpdate('requestEventsList', [])
        
    def requestEventsListResp(self, eventIds):
        self.events = eventIds
        self.checkActiveEvents()

    def isEventActive(self, eventId):
        # NOTE: Possible race condition where the client checks for if an event is active
        # *before* it gets a response from the AI.
        if not base.cr.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False
        return eventId in self.events

    def setEventActive(self, eventId, active):
        if active and eventId not in self.events:
            self.events.append(eventId)
        elif not active and eventId in self.events:
            del self.events[eventId]

    def checkActiveEvents(self):
        if self.isEventActive(AprilToonsGlobals.GLOBAL_LOW_GRAVITY):
            base.localAvatar.controlManager.currentControls.setGravity(ToontownGlobals.GravityValue * 0.75)
