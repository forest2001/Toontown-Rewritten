# 2013.08.22 22:26:56 Pacific Daylight Time
# Embedded file name: toontown.uberdog.TTSpeedchatRelay
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog.SpeedchatRelay import SpeedchatRelay
from otp.uberdog import SpeedchatRelayGlobals

class TTSpeedchatRelay(SpeedchatRelay):
    __module__ = __name__

    def __init__(self, cr):
        SpeedchatRelay.__init__(self, cr)

    def sendSpeedchatToonTask(self, receiverId, taskId, toNpcId, toonProgress, msgIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.TOONTOWN_QUEST, [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\uberdog\TTSpeedchatRelay.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:56 Pacific Daylight Time
