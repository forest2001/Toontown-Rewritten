# 2013.08.22 22:17:20 Pacific Daylight Time
# Embedded file name: toontown.char.DistributedChar
from otp.avatar import DistributedAvatar
import Char

class DistributedChar(DistributedAvatar.DistributedAvatar, Char.Char):
    __module__ = __name__

    def __init__(self, cr):
        try:
            self.DistributedChar_initialized
        except:
            self.DistributedChar_initialized = 1
            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            Char.Char.__init__(self)

    def delete(self):
        try:
            self.DistributedChar_deleted
        except:
            self.DistributedChar_deleted = 1
            Char.Char.delete(self)
            DistributedAvatar.DistributedAvatar.delete(self)

    def setDNAString(self, dnaString):
        Char.Char.setDNAString(self, dnaString)

    def setDNA(self, dna):
        Char.Char.setDNA(self, dna)

    def playDialogue(self, *args):
        Char.Char.playDialogue(self, *args)

    def setHp(self, hp):
        self.hp = hp
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\char\DistributedChar.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:20 Pacific Daylight Time
