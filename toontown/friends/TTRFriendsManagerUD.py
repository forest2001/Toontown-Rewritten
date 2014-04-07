from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
import functools

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('TTRFriendsManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.onlineToons = []
        self.tpRequests = {}
        self.friendsLists = {}
        self.friendIndexes = {}
        self.listResponses = {}
    
    def removeFriend(self, friendId):
        avId = self.air.getAvatarIdFromSender()
        self.__removeFromFriendsList(avId, friendId)
        self.__removeFromFriendsList(friendId, avId, True)
        
    def __removeFromFriendsList(self, t1, t2, notify=False):
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            newList = []
            friendsList = fields['setFriendsList'][0]
            for i in range(len(friendsList)):
                if friendsList[i][0] == t2:
                    continue
                newList.append(friendsList[i])
            if t1 in self.onlineToons:
                dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                        'setFriendsList', t1, t1, self.air.ourChannel,
                         [newList])
                self.air.send(dg)
                if notify:
                    dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                         'friendsNotify', t1, t1, self.air.ourChannel, [t2, 1])
                    self.air.send(dg)
            else:
                self.air.dbInterface.updateObject(self.air.dbId, t1, self.air.dclassesByName['DistributedToonUD'],
                                                  {'setFriendsList' : [newList]})
        self.air.dbInterface.queryObject(self.air.dbId, t1, handleToon)
                
        
        
    def requestAvatarInfo(self, friendIds):
        avId = self.air.getAvatarIdFromSender()
        
        self.currId = 0
        
        def handleFriend(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            name = fields['setName'][0]
            dna = fields['setDNAString'][0]
            petId = fields['setPetId'][0]
            self.sendUpdateToAvatarId(avId, 'friendInfo', [self.currId, name, dna, petId])
            
        
        def handleAv(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            friendsList = fields['setFriendsList'][0]
            for id in friendIds:
                for friend in friendsList:
                    if friend[0] == id:
                        currId = id
                        self.air.dbInterface.queryObject(self.air.dbId, id, handleFriend)
                        break
        
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleAv)
        
    def requestFriendsList(self):
        avId = self.air.getAvatarIdFromSender()
        
        # Writing this function made me hate Python        
        
        def addFriend(dclass, fields, friendId=0, avId=0):
            if not (avId or friendId):
                return
            if dclass == self.air.dclassesByName['DistributedToonUD']:
                self.listResponses[avId].append([friendId, fields['setName'][0], fields['setDNAString'][0], fields['setPetId'][0]])
            if len(self.listResponses[avId]) >= len(self.friendsLists[avId]):
                self.sendUpdateToAvatarId(avId, 'friendList', [self.listResponses[avId]])
                del self.friendsLists[avId]
                del self.friendIndexes[avId]
                del self.listResponses[avId]
            else:
                self.friendIndexes[avId] += 1
                self.air.dbInterface.queryObject(self.air.dbId, self.friendsLists[avId][self.friendIndexes[avId]][0], functools.partial(addFriend, avId=avId, friendId=self.friendsLists[avId][self.friendIndexes[avId]][0]))
        
        def handleAv(dclass, fields, avId=0):
            if not avId:
                return
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            if not avId in self.onlineToons:
                self.onlineToons.append(avId)
                self.toonOnline(avId, fields)
            self.friendsLists[avId] = fields['setFriendsList'][0]
            self.friendIndexes[avId] = 0
            self.listResponses[avId] = []
            if len(self.friendsLists[avId]) <= 0:
                self.sendUpdateToAvatarId(avId, 'friendList', [self.listResponses[avId]])
                del self.friendsLists[avId]
                del self.friendIndexes[avId]
                del self.listResponses[avId]
                return
            self.air.dbInterface.queryObject(self.air.dbId, self.friendsLists[avId][0][0], functools.partial(addFriend, avId=avId, friendId=self.friendsLists[avId][0][0]))
       
        self.air.dbInterface.queryObject(self.air.dbId, avId, functools.partial(handleAv, avId=avId))
        
    def toonOnline(self, doId, fields):
        self.onlineToons.append(doId)
        friendsList = fields['setFriendsList'][0]
        
        channel = self.GetPuppetConnectionChannel(doId)
        dgcleanup = self.dclass.aiFormatUpdate('goingOffline', self.doId, self.doId, self.air.ourChannel, [doId])
        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.air.send(dg)
        
        for friend in friendsList:
            friendId = friend[0]
            if friend[0] in self.onlineToons:
                self.sendUpdateToAvatarId(doId, 'friendOnline', [friendId, 0, 0])
            self.sendUpdateToAvatarId(friendId, 'friendOnline', [doId, 0, 0])
    
    def toonOffline(self, doId):
        if doId not in self.onlineToons:
            return
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            friendsList = fields['setFriendsList'][0]
            for friend in friendsList:
                friendId = friend[0]
                if friendId in self.onlineToons:
                    self.sendUpdateToAvatarId(friendId, 'friendOffline', [doId])
            self.onlineToons.remove(doId)
        self.air.dbInterface.queryObject(self.air.dbId, doId, handleToon)
        
    def clearList(self, doId):
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            friendsList = fields['setFriendsList'][0]
            for friend in friendsList:
                self.__removeFromFriendsList(doId, friend[0])
                self.__removeFromFriendsList(friend[0], doId, True)
        self.air.dbInterface.queryObject(self.air.dbId, doId, handleToon)
        
    def goingOffline(self, avId):
        self.toonOffline(avId)
        
    def getAvatarDetails(self, avId):
        #return
        senderId = self.air.getAvatarIdFromSender()
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            inventory = fields['setInventory'][0]
            trackAccess = fields['setTrackAccess'][0]
            trophies = 0 # fields['setTrophyScore'][0] is not db
            hp = fields['setHp'][0]
            maxHp = fields['setMaxHp'][0]
            defaultShard = fields['setDefaultShard'][0]
            lastHood = 2000 if fields['setLastHood'][0] in [10000, 11000, 12000, 13000] else fields['setLastHood'][0]
            dnaString =  fields['setDNAString'][0]
            experience = fields['setExperience'][0]
            trackBonusLevel = fields['setTrackBonusLevel'][0]
            # We need an actual way to send the fields to the client...............
            # Inventory, trackAccess, trophies, Hp, maxHp, defaultshard, lastHood, dnastring
            self.sendUpdateToAvatarId(senderId, 'friendDetails', [avId, inventory, trackAccess, trophies, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel])
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleToon)
    
    # much client very trust
    
    # The TTRFM Uberdog acts as a 'gateway' between two friends
    # when they cannot directly send updates to one another, for
    # example when they are on different shards. We do this because
    # Astron does not currently support a few things that we need.
    # In this case, we route sent whispers and teleport queries from
    # 1 client to another. We should probably log these, but for now
    # we won't.
    
    def routeTeleportQuery(self, toId):
        fromId = self.air.getAvatarIdFromSender()
        self.tpRequests[fromId] = toId
        self.sendUpdateToAvatarId(toId, 'teleportQuery', [fromId])
        taskMgr.doMethodLater(5, self.giveUpTeleportQuery, 'tp-query-timeout-%d' % fromId, extraArgs=[fromId, toId])
        
    def giveUpTeleportQuery(self, fromId, toId):
        # The client didn't respond to the query within the set time,
        # So we will tell the query sender that the toon is unavailable.
        if fromId in self.tpRequests:
            del self.tpRequests[fromId]
            self.sendUpdateToAvatarId(fromId, 'teleportResponse', [toId, 0, 0, 0, 0])
            self.notify.warning('Teleport request that was sent by %d to %d timed out.' % (fromId, toId))
        
    def routeTeleportResponse(self, toId, available, shardId, hoodId, zoneId):
        # Here is where the toId and fromId swap (because we are now sending it back)
        fromId = self.air.getAvatarIdFromSender()
        
        # We got the query response, so no need to give up!
        if taskMgr.hasTaskNamed('tp-query-timeout-%d' % toId):
            taskMgr.remove('tp-query-timeout-%d' % toId)
            
        if toId not in self.tpRequests:
            return
        if self.tpRequests.get(toId) != fromId:
            self.air.writeServerEvent('suspicious', fromId, 'toon tried to send teleportResponse for a query that isn\'t theirs!')
            return
        self.sendUpdateToAvatarId(toId, 'teleportResponse', [fromId, available, shardId, hoodId, zoneId])
        del self.tpRequests[toId]
        
    def whisperSCTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setWhisperSCFrom', [fromId, msgIndex])
        
    def whisperSCCustomTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setWhisperSCCustomFrom', [fromId, msgIndex])
        
    def whisperSCEmoteTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setWhisperSCEmoteFrom', [fromId, msgIndex])
        
    def sendTalkWhisper(self, toId, message):
        fromId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'receiveTalkWhisper', [fromId, message])
        self.air.writeServerEvent('whisper-said', fromId, toId, message)
