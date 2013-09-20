# 2013.08.22 22:20:40 Pacific Daylight Time
# Embedded file name: toontown.friends.TTPlayerFriendsManager
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.friends.PlayerFriendsManager import PlayerFriendsManager

class TTPlayerFriendsManager(PlayerFriendsManager):
    __module__ = __name__

    def __init__(self, cr):
        PlayerFriendsManager.__init__(self, cr)

    def sendRequestInvite(self, playerId):
        self.sendUpdate('requestInvite', [0, playerId, False])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\friends\TTPlayerFriendsManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:40 Pacific Daylight Time
