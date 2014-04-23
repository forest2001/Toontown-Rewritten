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
        self.callback(success=True, requesterId=self.requesterId, online=self.online)
    
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
        
    def deleteFSM(self, requesterId):
        fsm = self.fsms.get(requesterId)
        if not fsm:
            # Just print debug incase we ever have issues.
            self.notify.debug('%d tried to delete non-existent FSM!' % requesterId)
            return
        if fsm.state != 'Off':
            fsm.demand('Failure')
        del self.fsms[requesterId]
        
    def removeFriend(self, avId):
        requesterId = self.air.getAvatarIdFromSender()
        if requesterId in self.fsms:
            # Looks like the requester already has an FSM running. In the future we
            # may want to handle this, but for now just ignore it.
            return
        # We need to get the friends list of the requester.
        fsm = GetToonFieldsFSM(self, requesterId, requesterId, functools.partial(self.__rfGotToonFields, avId=avId))
        fsm.start()
        self.fsms[requsterId] = fsm
        
    def __rfGotToonFields(self, success, requesterId, fields, avId=None, final=False):
        if not (success and avId):
            # Something went wrong... Delete the FSM and stop.
            self.deleteFSM(requesterId)
            return
        if fields['ID'] not in [requesterId, avId]:
            # Wtf? We got a db response for a toon that we didn't want
            # to edit! DEFCON 5!
            self.deleteFSM(requesterId)
            self.notify.warning('TTRFMUD.__rfGotToonFields received wrong toon fields from db, requesterId=%d' % requesterId)
            return
        friendsList = fields['setFriendsList'][0]
        for index, friendId in enumerate(friendsList):
            if friendId[0] == avId:
                del friendsList[index]
                break
        self.deleteFSM(requesterId)
        fsm = UpdateToonFieldFSM(self, requesterId, requesterId, functools.partial(self.__removeFriendCallback, avId=avId, final=final))
        fsm.start('setFriendsList', friendsList)
        self.fsms[requesterId] = fsm
        
    def __removeFriendCallback(self, success, requesterId, online=False, avId=None, final=False):
        if not (success and avId):
            # Something went wrong... Delete the FSM and stop.
            self.deleteFSM(requesterId)
            return
        if not final:
            # Toon was deleted from the friends list successfully! Now we need to modify
            # the other toons friends list...
            self.deleteFSM(requesterId)
            fsm = GetToonFieldsFSM(self, requesterId, avId, functools.partial(self.__rfGotToonFields, avId=avId, final=True))
            fsm.start()
            self.fsms[requesterId] = fsm
        else:
            # We're finished with everything!
            if online:
                # Lets notify their friend that they went bye bye!
                # Sad times for this toon. :(...
                dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                    'friendsNotify', avId, avId, self.air.ourChannel, [requesterId, 1]
                )
                self.air.send(dg)
            # Clean up our mess and we are finished!
            self.deleteFSM(requesterId)
