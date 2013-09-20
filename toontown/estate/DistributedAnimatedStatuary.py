# 2013.08.22 22:20:00 Pacific Daylight Time
# Embedded file name: toontown.estate.DistributedAnimatedStatuary
from pandac.PandaModules import NodePath
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.estate import DistributedStatuary
from toontown.estate import GardenGlobals
from direct.actor import Actor

class DistributedAnimatedStatuary(DistributedStatuary.DistributedStatuary):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimatedStatuary')

    def __init__(self, cr):
        self.notify.debug('constructing DistributedAnimatedStatuary')
        DistributedStatuary.DistributedStatuary.__init__(self, cr)

    def loadModel(self):
        self.rotateNode = self.plantPath.attachNewNode('rotate')
        self.model = Actor.Actor()
        animPath = self.modelPath + self.anims[1]
        self.model.loadModel(self.modelPath + self.anims[0])
        self.model.loadAnims(dict([[self.anims[1], animPath]]))
        colNode = self.model.find('**/+CollisionNode')
        if self.typeIndex == 234:
            colNode.setScale(0.5)
        if not colNode.isEmpty():
            score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballStatuary]
            if self.pinballScore:
                score = self.pinballScore[0]
                multiplier = self.pinballScore[1]
            scoreNodePath = NodePath('statuary-%d-%d' % (score, multiplier))
            colNode.setName('statuaryCol')
            scoreNodePath.reparentTo(colNode.getParent())
            colNode.reparentTo(scoreNodePath)
        self.model.setScale(self.worldScale)
        self.model.reparentTo(self.rotateNode)
        self.model.loop(self.anims[1])

    def setTypeIndex(self, typeIndex):
        DistributedStatuary.DistributedStatuary.setTypeIndex(self, typeIndex)
        self.anims = GardenGlobals.PlantAttributes[typeIndex]['anims']

    def setupShadow(self):
        if self.typeIndex == 234:
            pass
        else:
            DistributedStatuary.DistributedStatuary.setupShadow()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\estate\DistributedAnimatedStatuary.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:20:00 Pacific Daylight Time
