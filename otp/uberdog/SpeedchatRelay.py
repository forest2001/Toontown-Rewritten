# 2013.08.22 22:15:51 Pacific Daylight Time
# Embedded file name: otp.uberdog.SpeedchatRelay
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog import SpeedchatRelayGlobals

class SpeedchatRelay(DistributedObjectGlobal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def sendSpeedchat(self, receiverId, messageIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.NORMAL, [messageIndex])

    def sendSpeedchatCustom(self, receiverId, messageIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.CUSTOM, [messageIndex])

    def sendSpeedchatEmote(self, receiverId, messageIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.EMOTE, [messageIndex])

    def sendSpeedchatToRelay(self, receiverId, speedchatType, parameters):
        self.sendUpdate('forwardSpeedchat', [receiverId,
         speedchatType,
         parameters,
         base.cr.accountDetailRecord.playerAccountId,
         base.cr.accountDetailRecord.playerName + ' RHFM',
         0])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\uberdog\SpeedchatRelay.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:51 Pacific Daylight Time
