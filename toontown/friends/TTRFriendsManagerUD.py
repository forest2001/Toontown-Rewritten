from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    
    def removeFriend(self, friendId):
        avId = self.air.getAvatarIdFromSender()
        
        DistributedToon = self.air.dclassesByName['DistributedToonUD']
        
        def handleRemover(dclass, fields):
            if dclass != DistributedToon:
                return
            friendsList = fields['setFriendsList'][0]
            newList = []
            for i in range(len(friendsList)):
                if friendsList[i][0] == friendId:
                    continue
                newList.append(friendsList[i])
            dg = DistributedToon.aiFormatUpdate('setFriendsList', avId, avId,
                                                  self.air.ourChannel, [newList])
            self.air.send(dg)
            
        def handleRemovee(dclass, fields):
            if dclass != DistributedToon:
                self.air.writeServerEvent('suspicious', avId, 'Toon tried to remove a non-Toon from their friends list!')
            friendsList = fields['setFriendsList'][0]
            newList = []
            for i in range(len(friendsList)):
                if friendsList[i][0] == avId:
                    continue
                newList.append(friendsList[i])
            dg = DistributedToon.aiFormatUpdate('setFriendsList', friendId, friendId,
                                                  self.air.ourChannel, [newList])
            self.air.send(dg)
            self.air.dbInterface.updateObject(self.air.dbId, friendId, self.air.dclassesByName['DistributedToonUD'], {'setFriendsList' : [newList]})

        
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleRemover)
        self.air.dbInterface.queryObject(self.air.dbId, friendId, handleRemovee)
        
    def requestAvatarInfo(self, friendIds):
        return
        
    def requestFriendsList(self):
        return    
