from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.hood import ZoneUtil

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
                
    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])
        
    def friendDetails(self, avId, inventory, trackAccess, trophies, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel):
        fields = [
            ['setExperience' , experience],
            ['setTrackAccess' , trackAccess],
            ['setTrackBonusLevel' , trackBonusLevel],
            ['setInventory' , inventory],
            ['setHp' , hp],
            ['setMaxHp' , maxHp],
            ['setDefaultShard' , defaultShard],
            ['setLastHood' , lastHood],
            ['setDNAString' , dnaString],
        ]
        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)
        
    def d_teleportQuery(self, toId):
        self.sendUpdate('routeTeleportQuery', [toId])
        
    def teleportQuery(self, fromId):
        if not base.localAvatar.getTeleportAvailable() or base.localAvatar.ghostMode:
            base.localAvatar.setSystemMessage(0, '%s tried to visit you.' % base.cr.identifyFriend(fromId).getName())
            self.sendUpdate('routeTeleportResponse', [
                fromId,
                0,
                0,
                0,
                0
            ])
            return
            
        base.localAvatar.setSystemMessage(0, '%s is coming to visit you.' % base.cr.identifyFriend(fromId).getName())
        self.sendUpdate('routeTeleportResponse', [
            fromId,
            base.localAvatar.getTeleportAvailable(),
            base.localAvatar.defaultShard,
            ZoneUtil.getCanonicalHoodId(base.localAvatar.getZoneId()),
            base.localAvatar.getZoneId()
        ])
        
    def teleportResponse(self, fromId, available, shardId, hoodId, zoneId):
        base.localAvatar.teleportResponse(fromId, available, shardId, hoodId, zoneId)
