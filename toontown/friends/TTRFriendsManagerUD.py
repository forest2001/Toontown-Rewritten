from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.FSM import FSM
import functools
from time import time
import cPickle

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
        # TODO: Propper fix. This is just temporary
        try:
            self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.avId, self.__queryResponse)
        except:
            pass

    def __queryResponse(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['DistributedToonUD']:
            self.demand('Failure', 'Invalid dclass for avId %s!' % self.avId)
            return
        self.fields = fields
        self.fields['ID'] = self.avId
        self.demand('Finished')

    def enterFinished(self):
        # We want to cache the basic information we got for GetFriendsListFSM.
        self.mgr.avBasicInfoCache[self.avId] = {
            'expire' : time() + simbase.config.GetInt('friend-detail-cache-expire', 3600),
            'toonInfo' : [self.avId, self.fields['setName'][0], self.fields['setDNAString'][0], self.fields['setPetId'][0]],
        }
        self.callback(success=True, requesterId=self.requesterId, fields=self.fields)

    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success=False, requesterId=None, fields=None)

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
        self.mgr.air.getActivated(self.avId, self.__toonOnlineResp)

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

class GetFriendsListFSM(FSM):
    """
    This is an FSM class to fetch all the friends on a toons list
    and return their name, dna and petId to the requester. Currently,
    this may have a huge performance impact on the TTRFMUD as it may
    have to search up to 200 friends fields from the database.

    This also checks the cache to check for any existing, non-expired
    data the TTRFMUD has about a toon.
    """

    def __init__(self, mgr, requesterId, callback):
        FSM.__init__(self, 'GetFriendsListFSM')
        self.mgr = mgr
        self.requesterId = requesterId
        self.callback = callback
        self.friendsDetails = []
        self.iterated = 0
        self.getFriendsFieldsFSMs = {}
        self.onlineFriends = []

    def start(self):
        self.demand('GetFriendsList')

    def enterGetFriendsList(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.requesterId, self.__gotFriendsList)

    def __gotFriendsList(self, dclass, fields):
        if self.state != 'GetFriendsList':
            # We're not currently trying to get our friends list.
            self.demand('Failure', '__gotFriendsList called when looking for friends list, avId %d' % self.requesterId)
            return
        if dclass != self.mgr.air.dclassesByName['DistributedToonUD']:
            # We got an invalid class from the database, eww.
            self.demand('Failure', 'Invalid dclass for toonId %d' % self.requesterId)
            return
        self.friendsList = fields['setFriendsList'][0]
        self.demand('GetFriendsDetails')

    def enterGetFriendsDetails(self):
        for friendId, tf in self.friendsList:
            details = self.mgr.avBasicInfoCache.get(friendId)
            if details:
                # We have the toons details in cache.
                expire = details.get('expire')
                toonInfo = details.get('toonInfo')
                if expire and toonInfo:
                    if details.get('expire') > time():
                        # These details haven't expired, use 'em!
                        self.friendsDetails.append(toonInfo)
                        self.iterated += 1
                        self.__testFinished()
                        continue
                    else:
                        # It's expired, delete and continue.
                        del self.mgr.avBasicInfoCache[friendId]
            # We need to fetch their details
            fsm = GetToonDataFSM(self.mgr, self.requesterId, friendId, self.__gotAvatarInfo)
            fsm.start()
            self.getFriendsFieldsFSMs[friendId] = fsm

    def __gotAvatarInfo(self, success, requesterId, fields):
        # We no longer need the FSM!
        if fields['ID'] in self.getFriendsFieldsFSMs:
            del self.getFriendsFieldsFSMs[fields['ID']]
        if self.state != 'GetFriendsDetails':
            self.demand('Failure', '__gotAvatarInfo while not looking for friends details, avId=%d' % self.requesterId)
            return
        if requesterId != self.requesterId:
            self.demand('Failure', '__gotAvatarInfo response for wrong requester. wrongId=%d, rightId=%d' % (self.requesterId, requesterId))
            return
        self.iterated += 1
        self.friendsDetails.append([fields['ID'], fields['setName'][0], fields['setDNAString'][0], fields['setPetId'][0]])
        self.__testFinished()

    def __testFinished(self):
        if self.iterated >= len(self.friendsList) and len(self.getFriendsFieldsFSMs) == 0:
            # We've finished! We can now continue.
            self.demand('CheckFriendsOnline')

    def enterCheckFriendsOnline(self):
        self.iterated = 0
        for friendId, tf in self.friendsList:
            self.mgr.air.getActivated(friendId, self.__gotActivatedResp)

    def __gotActivatedResp(self, avId, activated):
        self.iterated += 1
        if activated:
            self.onlineFriends.append(avId)
        if self.iterated == len(self.friendsList):
            self.demand('Finished')

    def enterFinished(self):
        self.callback(success=True, requesterId=self.requesterId, friendsDetails=self.friendsDetails, onlineFriends=self.onlineFriends)

    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success=False, requesterId=self.requesterId, friendsDetails=None)

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    """
    The Toontown Rewritten Friends Manager UberDOG, or TTRFMUD for short.

    This object is responsible for all requests related to global friends, such as
    friends coming online, friends going offline, fetching a friends data etc.
    """

    notify = directNotify.newCategory('TTRFriendsManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.fsms = {}
        # TODO: Maybe get the AI to refresh the cache?
        self.avBasicInfoCache = {}
        self.tpRequests = {}
        self.air.netMessenger.accept('avatarOnline', self, self.comingOnline)
        self.air.netMessenger.accept('avatarOffline', self, self.goingOffline)

    def deleteFSM(self, requesterId):
        fsm = self.fsms.get(requesterId)
        if not fsm:
            # Just print debug incase we ever have issues.
            self.notify.debug('%d tried to delete non-existent FSM!' % requesterId)
            return
        if fsm.state != 'Off':
            fsm.demand('Off')
        del self.fsms[requesterId]

    def comingOnline(self, avId, friends):
        # This is sent from the CSMUD, so no sanity checks needed here.
        # This is sent when the avatar is set.
        for friendId in friends:
            # Is our friend online?
            self.air.getActivated(friendId, functools.partial(self.__comingOnlineFriendOnline, otherId=avId))

    def __comingOnlineFriendOnline(self, avId, activated, otherId=None):
        if not (otherId and activated):
            #??!?!?
            return
        # Declare our avatar to their friend.
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(avId), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
        dg.addUint32(otherId)
        dg.addUint16(self.air.dclassesByName['DistributedToonUD'].getNumber())
        self.air.send(dg)

        # Declare the friend to the avatar.
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(otherId), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
        dg.addUint32(avId)
        dg.addUint16(self.air.dclassesByName['DistributedToonUD'].getNumber())
        self.air.send(dg)

        # Tell the client their friend is online.
        self.sendUpdateToAvatarId(avId, 'friendOnline', [otherId, 0, 0])

    def goingOffline(self, avId):
        # This is sent from the MD, so no sanity checks needed here.
        # Since this is a post remove, it means the client has disconnected.
        # Therefore this FSM doesn't need to be saved in self.fsms as a client
        # may already be running an FSM.
        fsm = GetToonDataFSM(self, avId, avId, self.__offlineGotToonFields)
        fsm.start()

    def __offlineGotToonFields(self, success, requesterId, fields):
        if not success:
            # Something went wrong... abort.
            return
        for friendId, tf in fields['setFriendsList'][0]:
            self.air.getActivated(friendId, functools.partial(self.__offlineToonOnline, otherId=requesterId, accId=fields['setDISLid'][0]))

    def __offlineToonOnline(self, avId, activated, otherId=None, accId=None):
        if not (otherId and activated and accId):
            return
        # Undeclare to the friend!
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(avId), self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        dg.addUint32(otherId)
        self.air.send(dg)

        # Undeclare to our now-offline avId (they may still be around, about to log into a new toon!)
        dg = PyDatagram()
        dg.addServerHeader(self.GetAccountConnectionChannel(accId), self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        dg.addUint32(avId)
        self.air.send(dg)

        # Tell them they're offline!
        self.sendUpdateToAvatarId(avId, 'friendOffline', [otherId])

    def clearList(self, avId):
        # This is sent from the CSMUD when a toon is deleted.
        # First we need the avId's friendsList.
        fsm = GetToonDataFSM(self, avId, avId, self.__clearListGotFriendsList)
        fsm.start()
        self.fsms[avId] = fsm

    def __clearListGotFriendsList(self, success, requesterId, fields):
        if not success:
            # We couldn't get the avatar's friends list. Abort!
            return
        if requesterId != fields['ID']:
            # Wtf, we got the wrong toon's data!
            return
        friendIds = fields['setFriendsList'][0][:]
        friendIds.append((requesterId, 1))
        if friendIds[0][0] == requesterId:
            # This toon has no friends, no point doing database operations.
            return
        fsm = GetToonDataFSM(self, requesterId, friendIds[0][0], functools.partial(self.__clearListGotFriendData, friendIds=friendIds[1:]))
        fsm.start()
        self.fsms[requesterId] = fsm

    def __clearListGotFriendData(self, success, requesterId, fields, friendIds=[]):
        # Delete the FSM, we no longer need it.
        self.deleteFSM(requesterId)
        # Normally we would check if success is false, and stop if it is, but in this
        # case, we have to continue to clean up everyone else's friends list.
        if not success:
            if friendIds:
                # Move on to the next friend.
                fsm = GetToonDataFSM(self, requesterId, friendIds[0][0], functools.partial(self.__clearListGotFriendData, friendIds=friendIds[1:]))
                fsm.start()
                self.fsms[requesterId] = fsm
            else:
                # No more friends, we can now stop.
                return
        # Now we need to remove the requesterId from the friend's fields.
        friendsIds = fields['setFriendsList'][0][:]
        if requesterId == fields['ID']:
            # Delete our friends list entirely.
            friendsIds = []
        else:
            for friend in friendsIds:
                if friend[0] == requesterId:
                    # Remove ourself from our friend's list.
                    friendsIds.remove(friend)
        fsm = UpdateToonFieldFSM(self, requesterId, fields['ID'], functools.partial(self.__clearListUpdatedToonField, avId=fields['ID'], friendIds=friendIds[1:]))
        fsm.start('setFriendsList', friendsIds)
        self.fsms[requesterId] = fsm

    def __clearListUpdatedToonField(self, success, requesterId, online=False, avId=None, friendIds=[]):
        # Delete the FSM, we no longer need it.
        self.deleteFSM(requesterId)
        # Normally we would check if success is false, and stop if it is, but in this
        # case, we have to continue to clean up everyone else's friends list.
        if success and online:
            dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                'friendsNotify', avId, avId, self.air.ourChannel, [requesterId, 1]
            )
            self.air.send(dg)
        if not friendIds:
            # We can now stop, since we have no friends left to clear.
            return
        fsm = GetToonDataFSM(self, requesterId, friendIds[0], functools.partial(self.__clearListGotFriendData, friendIds=friendIds[1:]))
        fsm.start()
        self.fsms[requesterId] = fsm


    def removeFriend(self, avId):
        requesterId = self.air.getAvatarIdFromSender()
        if requesterId in self.fsms:
            # Looks like the requester already has an FSM running. In the future we
            # may want to handle this, but for now just ignore it.
            return
        # We need to get the friends list of the requester.
        fsm = GetToonDataFSM(self, requesterId, requesterId, functools.partial(self.__rfGotToonFields, avId=avId))
        fsm.start()
        self.fsms[requesterId] = fsm

    def __rfGotToonFields(self, success, requesterId, fields, avId=None, final=False):
        # We no longer need the FSM.
        self.deleteFSM(requesterId)
        if not (success and avId):
            # Something went wrong... abort.
            return
        if fields['ID'] not in [requesterId, avId]:
            # Wtf? We got a db response for a toon that we didn't want
            # to edit! DEFCON 5!
            self.notify.warning('TTRFMUD.__rfGotToonFields received wrong toon fields from db, requesterId=%d' % requesterId)
            return
        friendsList = fields['setFriendsList'][0]
        searchId = requesterId if final else avId
        for index, friend in enumerate(friendsList):
            if friend[0] == searchId:
                del friendsList[index]
                break
        fsm = UpdateToonFieldFSM(self, requesterId, avId if final else requesterId, functools.partial(self.__removeFriendCallback, avId=avId, final=final))
        fsm.start('setFriendsList', friendsList)
        self.fsms[requesterId] = fsm

    def __removeFriendCallback(self, success, requesterId, online=False, avId=None, final=False):
        # We no longer need the FSM.
        self.deleteFSM(requesterId)
        if not (success and avId):
            # Something went wrong... abort.
            return
        if not final:
            # Toon was deleted from the friends list successfully! Now we need to modify
            # the other toons friends list...
            fsm = GetToonDataFSM(self, requesterId, avId, functools.partial(self.__rfGotToonFields, avId=avId, final=True))
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
            # We are now finished, woo!

    def requestAvatarInfo(self, avIds):
        requesterId = self.air.getAvatarIdFromSender()
        if requesterId in self.fsms:
            # Looks like the requester already has an FSM running. In the future we
            # may want to handle this, but for now just ignore it.
            return
        if not avIds:
            # The list is empty. This is suspicious as the client shouldn't send
            # a blank list.
            self.notify.warning('Received blank list of avIds for requestAvatarInfo from avId %d' % requesterId)
            self.air.writeServerEvent('suspicious', avId=requesterId, issue='Sent a blank list of avIds for requestAvatarInfo in TTRFMUD')
            return
        fsm = GetToonDataFSM(self, requesterId, avIds[0], functools.partial(self.__avInfoCallback, avIds=avIds[1:]))
        fsm.start()
        self.fsms[requesterId] = fsm

    def __avInfoCallback(self, success, requesterId, fields, avIds):
        # We no longer need the FSM.
        self.deleteFSM(requesterId)
        if not success:
            # Something went wrong... abort.
            return
        self.sendUpdateToAvatarId(
            requesterId, 'friendInfo',
            [ fields['ID'], fields['setName'][0], fields['setDNAString'][0], fields['setPetId'][0] ]
        )
        if avIds:
            # We still have more to go... oh boy.
            fsm = GetToonDataFSM(self, requesterId, avIds[0], functools.partial(self.__avInfoCallback, avIds=avIds[1:]))
            fsm.start()
            self.fsms[requesterId] = fsm

    def requestFriendsList(self):
        requesterId = self.air.getAvatarIdFromSender()
        if requesterId in self.fsms:
            # Looks like the requester already has an FSM running. In the future we
            # may want to handle this, but for now just ignore it.
            return
        fsm = GetFriendsListFSM(self, requesterId, self.__gotFriendsList)
        fsm.start()
        self.fsms[requesterId] = fsm

    def __gotFriendsList(self, success, requesterId, friendsDetails, onlineFriends):
        # We no longer need the FSM.
        self.deleteFSM(requesterId)
        if not success:
            # Something went wrong... abort.
            return
        # Ship it!
        self.sendUpdateToAvatarId(requesterId, 'friendList', [friendsDetails])
        for friendId in onlineFriends:
            # For each online friend, announce it to the client.
            self.sendUpdateToAvatarId(requesterId, 'friendOnline', [friendId, 0, 0])

    def getAvatarDetails(self, friendId):
        requesterId = self.air.getAvatarIdFromSender()
        if requesterId in self.fsms:
            # Looks like the requester already has an FSM running. In the future we
            # may want to handle this, but for now just ignore it.
            return
        fsm = GetToonDataFSM(self, requesterId, friendId, self.__gotAvatarDetails)
        fsm.start()
        self.fsms[requesterId] = fsm

    def __gotAvatarDetails(self, success, requesterId, fields):
        # We no longer need the FSM.
        self.deleteFSM(requesterId)
        if not success:
            # Something went wrong... abort.
            return
        details = [
            ['setExperience' , fields['setExperience'][0]],
            ['setTrackAccess' , fields['setTrackAccess'][0]],
            ['setTrackBonusLevel' , fields['setTrackBonusLevel'][0]],
            ['setInventory' , fields['setInventory'][0]],
            ['setHp' , fields['setHp'][0]],
            ['setMaxHp' , fields['setMaxHp'][0]],
            ['setDefaultShard' , fields['setDefaultShard'][0]],
            ['setLastHood' , fields['setLastHood'][0]],
            ['setDNAString' , fields['setDNAString'][0]],
        ]
        self.sendUpdateToAvatarId(requesterId, 'friendDetails', [fields['ID'], cPickle.dumps(details)])
