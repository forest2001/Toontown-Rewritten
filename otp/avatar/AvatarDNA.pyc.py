# 2013.08.22 22:15:08 Pacific Daylight Time
# Embedded file name: otp.avatar.AvatarDNA
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
notify = directNotify.newCategory('AvatarDNA')

class AvatarDNA():
    __module__ = __name__

    def __str__(self):
        return 'avatar parent class: type undefined'

    def makeNetString(self):
        notify.error('called makeNetString on avatarDNA parent class')

    def printNetString(self):
        string = self.makeNetString()
        dg = PyDatagram(string)
        dg.dumpHex(ostream)

    def makeFromNetString(self, string):
        notify.error('called makeFromNetString on avatarDNA parent class')

    def getType(self):
        notify.error('Invalid DNA type: ', self.type)
        return type
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\avatar\AvatarDNA.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:08 Pacific Daylight Time
