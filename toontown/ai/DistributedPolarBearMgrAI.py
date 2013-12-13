from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toon.ToonDNA import ToonDNA

class DistributedPolarBearMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPolarBearMgrAI")
    
    def requestPolarBearTransformation(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av: return
        
        if av.dna.getAnimal() == 'bear' and av.dna.headColor != 0x00:
            newDNA = ToonDNA()
            newDNA.makeFromNetString(av.getDNAString())
            newDNA.headColor = 0x00
            newDNA.armColor = 0x00
            newDNA.legColor = 0x00
            taskMgr.doMethodLater(1.0, lambda task: av.b_setDNAString(newDNA.makeNetString()), 'transform-%d' %avId)
            
        self.sendUpdate('doPolarBearTransformation', [avId])
