# 2013.08.22 22:23:23 Pacific Daylight Time
# Embedded file name: toontown.parties.DistributedPartyJukeboxActivity
from toontown.parties.DistributedPartyJukeboxActivityBase import DistributedPartyJukeboxActivityBase
from toontown.parties import PartyGlobals

class DistributedPartyJukeboxActivity(DistributedPartyJukeboxActivityBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPartyJukeboxActivity')

    def __init__(self, cr):
        DistributedPartyJukeboxActivityBase.__init__(self, cr, PartyGlobals.ActivityIds.PartyJukebox, PartyGlobals.PhaseToMusicData)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\DistributedPartyJukeboxActivity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:23 Pacific Daylight Time
