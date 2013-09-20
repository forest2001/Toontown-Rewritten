# 2013.08.22 22:15:20 Pacific Daylight Time
# Embedded file name: otp.distributed.PotentialAvatar


class PotentialAvatar():
    __module__ = __name__

    def __init__(self, id, names, dna, position, allowedName, creator = 1, shared = 1, online = 0, wishState = 'CLOSED', wishName = '', defaultShard = 0, lastLogout = 0):
        self.id = id
        self.name = names[0]
        self.dna = dna
        self.avatarType = None
        self.position = position
        self.wantName = names[1]
        self.approvedName = names[2]
        self.rejectedName = names[3]
        self.allowedName = allowedName
        self.wishState = wishState
        self.wishName = wishName
        self.creator = creator
        self.shared = shared
        self.online = online
        self.defaultShard = defaultShard
        self.lastLogout = lastLogout
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\distributed\PotentialAvatar.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:20 Pacific Daylight Time
