from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify

class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')

    def performLogin(self, doneEvent):
        self.doneEvent = doneEvent

        cookie = self.cr.playToken or 'dev'

        self.notify.debug('Sending login cookie: ' + cookie)
        self.sendUpdate('login', [cookie])

    def acceptLogin(self):
        messenger.send(self.doneEvent)
