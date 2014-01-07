from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    
    def removeFriend(self, friendId):
        # Messy - I don't know the UberDOG too well. Somebody should probably clean this up.
        avId = self.air.getAvatarIdFromSender()
        
        DistributedToon = self.air.dclassesByName['DistributedToonUD']
        
        
        # Callbacks for the DBI
        def handleRemover(dclass, fields):
            # This shouldn't ever happen.
            if dclass != DistributedToon:
                return
            friendsList = fields['setFriendsList'][0]
            newList = []
            print type(newList).__name__
            for i in range(len(friendsList)):
                if friendsList[i][0] == friendId:
                    print type(friendsList[i]).__name__
                    continue
                newList.append(friendsList[i])
            # We don't need to send the update to the DB interface - the DBSS should be listening for updates to this object no matter what as *somebody* had to be online for the request to happen.
            dg = DistributedToon.aiFormatUpdate('setFriendsList', avId, avId,
                                                  self.air.ourChannel, [newList])
            self.air.send(dg)
            
        def handleRemovee(dclass, fields):
            if dclass != DistributedToon:
                self.air.writeServerEvent('suspicious', avId, 'Toon tried to remove a non-Toon from their friends list!')
            friendsList = fields['setFriendsList'][0]
            newList = []
            # bad code!
            for i in range(len(friendsList)):
                if friendsList[i][0] == avId:
                    continue
                newList.append(friendsList[i])
            dg = DistributedToon.aiFormatUpdate('setFriendsList', friendId, friendId,
                                                  self.air.ourChannel, [newList])
            self.air.send(dg)
            # However, here, we have no idea whether or not the Toon is loaded. Send it as an update so the client, if it exists, sees the change instantly and then also to the DB in case the client doesn't exist.
            self.air.dbInterface.updateObject(self.air.dbId, friendId, self.air.dclassesByName['DistributedToonUD'], {'setFriendsList' : [newList]})

        
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleRemover)
        self.air.dbInterface.queryObject(self.air.dbId, friendId, handleRemovee)
        
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
                print 'sending friends list!'
                self.sendUpdateToAvatarId(avId, 'friendList', [self.resp])
        
        def handleAv(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            friendsList = fields['setFriendsList'][0]
            self.numFriends = len(friendsList)
            for friend in friendsList:
                self.currFriend = friend[0]
                self.air.dbInterface.queryObject(self.air.dbId, friend[0], addFriend)
                
        
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleAv)
