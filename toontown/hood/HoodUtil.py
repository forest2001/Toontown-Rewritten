# 2013.08.22 22:20:53 Pacific Daylight Time
# Embedded file name: toontown.hood.HoodUtil
from toontown.toonbase import ToontownGlobals

def calcPropType(node):
    propType = ToontownGlobals.AnimPropTypes.Unknown
    fullString = str(node)
    if 'hydrant' in fullString:
        propType = ToontownGlobals.AnimPropTypes.Hydrant
    elif 'trashcan' in fullString:
        propType = ToontownGlobals.AnimPropTypes.Trashcan
    elif 'mailbox' in fullString:
        propType = ToontownGlobals.AnimPropTypes.Mailbox
    return propType
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\hood\HoodUtil.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:53 Pacific Daylight Time
