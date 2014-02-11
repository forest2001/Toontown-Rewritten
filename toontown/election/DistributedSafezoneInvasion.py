from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.toonbase import ToontownGlobals

class DistributedSafezoneInvasion(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.accept('localPieSplat', self.__localPieSplat)

    def delete(self):
        DistributedObject.delete(self)

        self.ignoreAll()

    def __localPieSplat(self, pieCode, entry):
        if pieCode == ToontownGlobals.PieCodeToon:
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Toon %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
                return
            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                self.d_hitToon(doId)
        elif pieCode == ToontownGlobals.PieCodeInvasionSuit:
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Suit %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
                return
            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                self.d_hitSuit(doId)

    def d_hitToon(self, doId):
        self.sendUpdate('hitToon', [doId])

    def d_hitSuit(self, doId):
        self.sendUpdate('hitSuit', [doId])
