# 2013.08.22 22:26:54 Pacific Daylight Time
# Embedded file name: toontown.uberdog.DataStoreGlobals
from toontown.uberdog.ScavengerHuntDataStore import *
from toontown.uberdog.DataStore import *
SH = 1
GEN = 2
TYPES = {SH: (ScavengerHuntDataStore,),
 GEN: (DataStore,)}

def getStoreClass(type):
    storeClass = TYPES.get(type, None)
    if storeClass:
        return storeClass[0]
    return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\uberdog\DataStoreGlobals.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:26:54 Pacific Daylight Time
