# 2013.08.22 22:14:37 Pacific Daylight Time
# Embedded file name: direct.showbase.LerpBlendHelpers
__all__ = ['getBlend']
from pandac.PandaModules import *
easeIn = EaseInBlendType()
easeOut = EaseOutBlendType()
easeInOut = EaseInOutBlendType()
noBlend = NoBlendType()

def getBlend(blendType):
    if blendType == 'easeIn':
        return easeIn
    elif blendType == 'easeOut':
        return easeOut
    elif blendType == 'easeInOut':
        return easeInOut
    elif blendType == 'noBlend':
        return noBlend
    else:
        raise Exception('Error: LerpInterval.__getBlend: Unknown blend type')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\LerpBlendHelpers.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:37 Pacific Daylight Time
