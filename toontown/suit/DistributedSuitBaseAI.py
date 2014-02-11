from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from SuitBase import SuitBase
from SuitDNA import SuitDNA

class DistributedSuitBaseAI(DistributedObjectAI, SuitBase):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitBaseAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        SuitBase.__init__(self)

        self.dna = SuitDNA()
        self.name = ''
        self.skeleRevives = 0

    def b_setHP(self, hp):
        self.d_setHP(hp)
        self.setHP(hp)

    def d_setHP(self, hp):
        self.sendUpdate('setHP', [hp])

    def setHP(self, hp):
        self.currHP = hp

    def getHP(self):
        return self.currHP

    def getLevelDist(self):
        return self.level

    def getSkeleRevives(self):
        return self.skeleRevives

    def b_setDNAString(self, string):
        self.d_setDNAString(string)
        self.setDNAString(string)

    def d_setDNAString(self, string):
        self.sendUpdate('setDNAString', [string])

    def setDNAString(self, string):
        self.dna.makeFromNetString(string)

    def getDNAString(self):
        return self.dna.makeNetString()

    def setDisplayName(self, name):
        pass # This only exists because SuitBase tries to call it.
