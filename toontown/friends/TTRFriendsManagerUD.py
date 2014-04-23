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
        self.callback = callback
        
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
        
class UpdateToonFieldFSM(FSM):
    """
    A quick implementation to update a toon's fields in the
    database and return a callback to the TTRFMUD.
    """
    
    def __init__(self, mgr, requesterId, avId, callback):
        FSM.__init__(self, 'UpdateToonDataFSM')
        self.mgr = mgr
        self.requesterId = requesterId
        self.avId = avId
        self.callback = callback
        
    def start(self, field, value):
        self.field = field
        self.value = value
        self.demand('GetToonOnline')
        
    def enterGetToonOnline(self):
        self.mgr.air.getActivated(avId, self.__toonOnlineResp)
        
    def __toonOnlineResp(self, avId, activated):
        if self.state != 'GetToonOnline':
            self.demand('Failure', 'Received __toonOnlineResp while not in GetToonOnline state.')
            return
        self.online = activated
        self.demand('UpdateDB')
       
    def enterUpdateDB(self):
        if self.online:
            dg = self.mgr.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                    self.field, self.avId, self.avId, self.mgr.air.ourChannel, [self.value]
                )
            self.mgr.air.send(dg)
        else:
            self.mgr.air.dbInterface.updateObject(
                self.mgr.air.dbId,
                self.avId,
                self.mgr.air.dclassesByName['DistributedToonUD'],
                { self.field : [self.value] }
            )
        self.demand('Finished')
        
    def enterFinished(self):
        self.callback(success=True)
    
    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success=False)
        

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    """
    The Toontown Rewritten Friends Manager UberDOG, or TTRFMUD for short.
    
    This object is responsible for all requests related to global friends, such as
    friends coming online, friends going offline, fetching a friends data etc.
    """
    
    notify = directNotify.newCategory('TTRFriendsManagerUD')
    
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        # requesterId : fsm
        self.fsms = {}
