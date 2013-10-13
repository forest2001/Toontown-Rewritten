from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.PyDatagram import *

class ClientServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ClientServicesManagerUD')

    def login(self, cookie):
        self.notify.debug('Received login cookie %r from %d' % (cookie, self.air.getMsgSender()))

        pdg = PyDatagram()
        pdg.addServerHeader(self.air.getMsgSender(), self.air.ourChannel, 3110)
        pdg.addUint16(2)
        self.air.send(pdg)

        self.sendUpdateToChannel(self.air.getMsgSender(), 'acceptLogin', [])

    def requestAvatars(self):
        self.notify.debug('Received avatar list request from %d' % (self.air.getMsgSender()))

        av = [123,
              'Shockley',
              't\x05\x01\x01\x01\x01\t\x01\t\x00\r\x1a\x00\x1a\x1a',
              1,
              0]

        avs = [av]

        self.sendUpdateToChannel(self.air.getMsgSender(), 'setAvatars', [avs])
