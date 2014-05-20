from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.otpbase import OTPLocalizer
from toontown.hood import ZoneUtil
import cPickle

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
        
    def friendDetails(self, friendId, details):
        fields = cPickle.loads(details)
        base.cr.n_handleGetAvatarDetailsResp(friendId, fields=fields)