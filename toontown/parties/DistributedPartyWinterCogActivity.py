from toontown.parties.DistributedPartyCogActivity import DistributedPartyCogActivity

class DistributedPartyWinterCogActivity(DistributedPartyCogActivity):
    __module__ = __name__

    def __init__(self, cr):
        DistributedPartyCogActivity.__init__(self, cr, 'phase_13/models/parties/tt_m_ara_pty_cogPieArenaWinter')
