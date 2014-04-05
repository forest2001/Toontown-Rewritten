from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class DistributedAprilToonsMgr(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('AprilToonsMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.events = None


    def getEvents(self):
        return self.events

    def isEventActive(self, event):
        if not base.cr.config.GetBool('want-april-toons', False):
            # If this DO is generated but we don't want april toons, always return
            # false regardless.
            return False

        if self.events == None:
            self.events = self.sendUpdate('getEvents', [])
            self.notify.debug('Pinged the server to ask for April Toons events. Got events %s' % self.events)

        if event in self.events:
            return self.events.get(event)
        return False

    def setEventActive(self, event, active):
        if event in self.getEvents():
            self.events[event] = active
            return True
        return False
