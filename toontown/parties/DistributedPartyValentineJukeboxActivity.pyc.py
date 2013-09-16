# 2013.08.22 22:23:27 Pacific Daylight Time
# Embedded file name: toontown.parties.DistributedPartyValentineJukeboxActivity
from toontown.parties.DistributedPartyJukeboxActivityBase import DistributedPartyJukeboxActivityBase
from toontown.parties import PartyGlobals

class DistributedPartyValentineJukeboxActivity(DistributedPartyJukeboxActivityBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPartyJukeboxActivity')

    def __init__(self, cr):
        DistributedPartyJukeboxActivityBase.__init__(self, cr, PartyGlobals.ActivityIds.PartyValentineJukebox, PartyGlobals.PhaseToMusicData)

    def load(self):
        DistributedPartyJukeboxActivityBase.load(self)
        newTexture = loader.loadTexture('phase_13/maps/tt_t_ara_pty_jukeboxValentineA.jpg', 'phase_13/maps/tt_t_ara_pty_jukeboxValentineA_a.rgb')
        case = self.jukebox.find('**/jukeboxGlass')
        if not case.isEmpty():
            case.setTexture(newTexture, 1)
        body = self.jukebox.find('**/jukeboxBody')
        if not body.isEmpty():
            body.setTexture(newTexture, 1)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\DistributedPartyValentineJukeboxActivity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:27 Pacific Daylight Time
