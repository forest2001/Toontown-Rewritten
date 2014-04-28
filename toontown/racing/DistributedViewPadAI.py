from direct.directnotify import DirectNotifyGlobal
from toontown.racing.DistributedKartPadAI import DistributedKartPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedViewingBlockAI
from direct.distributed.ClockDelta import *
from toontown.dna.DNASpawnerAI import *
from toontown.dna.DNANode import DNANode
from toontown.dna.DNAProp import DNAProp

class DistributedViewPadAI(DistributedKartPadAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedViewPadAI")
    
    def __init__(self, air):
        DistributedKartPadAI.__init__(self, air)
        self.timestamp = globalClockDelta.getRealNetworkTime()
    
    def setLastEntered(self, timestamp):
        self.timestamp = timestamp
        
    def d_setLastEntered(self, timestamp):
        self.sendUpdate('setLastEntered', [timestamp])
        
    def b_setLastEntered(self, timestamp):
        self.setLastEntered(timestamp)
        self.d_setLastEntered(timestamp)
        
    def getLastEntered(self):
        return self.timestamp
        
    def updateTimer(self):
        self.b_setLastEntered(globalClockDelta.getRealNetworkTime())

@dnaSpawn(DNANode, 'viewing_pad')
def spawn(air, zone, element, match):
    pad = DistributedViewPadAI(air)
    pad.setArea(zone)
    pad.generateWithRequired(zone)
    for child in element.children:
        if isinstance(child, DNAProp) and child.code == 'gs_showblock':
            x, y, z = child.getPos()
            h, p, r = child.getHpr()
            startingBlock = DistributedViewingBlockAI(air)
            startingBlock.setPosHpr(x, y, z, h, p, r)
            startingBlock.setPadDoId(pad.getDoId())
            startingBlock.setPadLocationId(0)
            startingBlock.generateWithRequired(zone)
            pad.addStartingBlock(startingBlock)
