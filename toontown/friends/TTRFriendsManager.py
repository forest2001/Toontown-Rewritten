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
        if not hasattr(base, 'localAvatar'):
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not hasattr(base.localAvatar, 'getTeleportAvailable') or not hasattr(base.localAvatar, 'ghostMode'):
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not base.localAvatar.getTeleportAvailable() or base.localAvatar.ghostMode:
            if hasattr(base.cr.identifyFriend(fromId), 'getName'):
                base.localAvatar.setSystemMessage(0, '%s tried to visit you.' % base.cr.identifyFriend(fromId).getName())
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            return  
        if base.cr.estateMgr.atEstate:
            hoodId = 30000 # TODO: Get from TTGlobals (too lazy right now)
            
            # TEMPORARY, UNTIL TPING TO FRIENDS ESTATES WORKS
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            base.localAvatar.setSystemMesssage(0,' %s tried to visit you, but estate teleporting is currently disabled.' % bbase.cr.identifyFriend(fromId).getName())
            return
            # TEMPORARY, UNTIL TPING TO FRIENDS ESTATES WORKS
        else:
            hoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.getZoneId())
        if hasattr(base.cr.identifyFriend(fromId), 'getName'):
            base.localAvatar.setSystemMessage(0, '%s is coming to visit you.' % base.cr.identifyFriend(fromId).getName())
        self.sendUpdate('routeTeleportResponse', [
            fromId,
            base.localAvatar.getTeleportAvailable(),
            base.localAvatar.defaultShard,
            hoodId,
            base.localAvatar.getZoneId()
        ])
        
    def teleportResponse(self, fromId, available, shardId, hoodId, zoneId):
        base.localAvatar.teleportResponse(fromId, available, shardId, hoodId, zoneId)
        
    def d_whisperSCTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCTo', [toId, msgIndex])
        
    def setWhisperSCFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCFrom'):
            return
        base.localAvatar.setWhisperSCFrom(fromId, msgIndex)
        
    def d_whisperSCCustomTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCCustomTo', [toId, msgIndex])
      
    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCCustomFrom'):
            return
        base.localAvatar.setWhisperSCCustomFrom(fromId, msgIndex)
        
    def d_whisperSCEmoteTo(self, toId, emoteId):
        self.sendUpdate('whisperSCEmoteTo', [toId, emoteId])
        
    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCEmoteFrom'):
            return
        base.localAvatar.setWhisperSCEmoteFrom(fromId, emoteId)
