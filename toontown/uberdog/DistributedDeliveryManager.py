# 2013.08.22 22:26:55 Pacific Daylight Time
# Embedded file name: toontown.uberdog.DistributedDeliveryManager
from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem

class DistributedDeliveryManager(DistributedObject):
    __module__ = __name__
    neverDisable = 1

    def sendHello(self, message):
        self.sendUpdate('hello', [message])

    def rejectHello(self, message):
        print 'rejected', message

    def helloResponse(self, message):
        print 'accepted', message

    def sendAck(self):
        self.sendUpdate('requestAck', [])

    def returnAck(self):
        messenger.send('DeliveryManagerAck')

    def test(self):
        print 'Distributed Delviery Manager Stub Test'
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\uberdog\DistributedDeliveryManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:55 Pacific Daylight Time
