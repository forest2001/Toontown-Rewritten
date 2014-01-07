from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class TTRFriendsManagerUD(DistributedObjectGlobalUD):

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.onlineToons = []
    
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
            self.sendUpdateToAvatarId(avId, 'friendDetails', [self.currId, name, dna, petId])
            
        
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
        
        self.resp = []
        self.currFriend = 0
        self.numFriends = 0
        
        def addFriend(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            self.resp.append((self.currFriend, fields['setName'][0], fields['setDNAString'][0], fields['setPetId'][0]))
            if (len(self.resp) == self.numFriends):
                self.sendUpdateToAvatarId(avId, 'friendList', [self.resp])
        
        def handleAv(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            if not avId in self.onlineToons:
                self.onlineToons.append(avId)
                self.toonOnline(avId, fields)
            friendsList = fields['setFriendsList'][0]
            self.numFriends = len(friendsList)
            for friend in friendsList:
                self.currFriend = friend[0]
                self.air.dbInterface.queryObject(self.air.dbId, friend[0], addFriend)
                
        
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleAv)
        
    def toonOnline(self, doId, fields):
        self.onlineToons.append(doId)
        friendsList = fields['setFriendsList'][0]
        for friend in friendsList:
            friendId = friend[0]
            if friend[0] in self.onlineToons:
                self.sendUpdateToAvatarId(doId, 'friendOnline', [friendId, 0, 0])
            self.sendUpdateToAvatarId(friendId, 'friendOnline', [doId, 0, 0])
    
    def toonOffline(self, doId):
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
