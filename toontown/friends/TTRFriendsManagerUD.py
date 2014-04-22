from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.FSM import FSM
import functools

class GetToonDataFSM(FSM):
    """
    A quick implementation to fetch a toon's fields from the
    database and return it back to the TTRFMUD via a callback.
    """
    
    def __init__(self, mgr, requesterId, avId, callback):
        FSM.__init__(self, 'GetToonDataFSM')
        self.mgr = mgr
        self.requesterId = requesterId
        self.avId = avId
        self.callback
        
    def start(self):
        self.demand('QueryDB')
        
    def enterQueryDB(self):
        self.mgr.air.queryObject(self.mgr.air.dbId, self.avId, self.__queryResponse)
        
    def __queryResponse(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['DistributedToonUD']:
            self.demand('Failure', 'Invalid dclass for avId %s!' % self.avId)
            return
        self.fields = fields
        self.fields['ID'] = self.avId
        self.demand('Finished')
        
    def enterFinished(self):
        self.callback(success=True, self.requesterId, self.fields)
            
    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success=False, None, None)

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('TTRFriendsManagerUD')
    pass
