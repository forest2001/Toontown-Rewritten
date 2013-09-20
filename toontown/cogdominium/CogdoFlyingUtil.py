# 2013.08.22 22:17:43 Pacific Daylight Time
# Embedded file name: toontown.cogdominium.CogdoFlyingUtil
from otp.otpbase import OTPGlobals
from CogdoFlyingShadowPlacer import CogdoFlyingShadowPlacer

def loadMockup(fileName, dmodelsAlt = 'coffin'):
    try:
        model = loader.loadModel(fileName)
    except IOError:
        model = loader.loadModel('phase_4/models/props/%s' % dmodelsAlt)

    return model


def swapAvatarShadowPlacer(avatar, name):
    avatar.setActiveShadow(0)
    avatar.deleteDropShadow()
    avatar.initializeDropShadow()
    if avatar.shadowPlacer:
        avatar.shadowPlacer.delete()
        avatar.shadowPlacer = None
    shadowPlacer = CogdoFlyingShadowPlacer(base.shadowTrav, avatar.dropShadow, OTPGlobals.WallBitmask, OTPGlobals.FloorBitmask, name)
    avatar.shadowPlacer = shadowPlacer
    avatar.setActiveShadow(0)
    avatar.setActiveShadow(1)
    return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\cogdominium\CogdoFlyingUtil.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:43 Pacific Daylight Time
