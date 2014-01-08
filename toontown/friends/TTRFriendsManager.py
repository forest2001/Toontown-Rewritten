from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

class TTRFriendsManager(DistributedObjectGlobal):
    
    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])
        
    def d_requestAvatarInfo(self, friendIds):
        self.sendUpdate('requestAvatarInfo', [friendIds])
        
    def d_requestFriendsList(self):
        self.sendUpdate('requestFriendsList', [])
    
    def friendInfo(self, resp):
        base.cr.handleGetFriendsListExtended(resp)
        
    def friendList(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id, commonChatFlags, whitelistChatFlags):
        base.cr.handleFriendOnline(id, commonChatFlags, whitelistChatFlags)
        
    def friendOffline(self, id):
        base.cr.handleFriendOffline(id)
        
    def d_goingOffline(self):
        self.sendUpdate('goingOffline', [])
        
    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])
        
    def friendDetails(self, avId, inventory, trackAccess, trophies, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel):
        base.cr.n_handleGetAvatarDetailsResp(avId, inventory, trackAccess, trophies, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel)
