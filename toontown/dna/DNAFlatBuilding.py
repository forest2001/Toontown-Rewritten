from DNANode import DNANode
from DNAParser import *
from panda3d.core import *
import re

class DNAFlatBuilding(DNANode):
    TAG = 'flat_building'

    INDEX_REGEX = re.compile('tb([0-9]+):')

    def __init__(self, id, width="0"):
        DNANode.__init__(self, id)

        self.id = id
        self.width = float(width)

    def _makeNode(self, storage, parent):
        return parent.attachNewNode(self.id)

    def _postGenerate(self, storage, np):
        height = np.getPythonTag('wall_height') or 0.0
        np.clearPythonTag('wall_height')
        
        node = np.attachNewNode(self.id)
        
        internalNode = np.attachNewNode(self.id + '-internal')
        internalNode.setScale(self.getScale())

        # First, set up collisions. We need a (self.width, height)-sized square.
        barrierNode = storage.findNode('wall_camera_barrier')
        if not barrierNode:
            raise DNAError('No wall_camera_barrier in storage.')

        barrier = barrierNode.copyTo(internalNode, 0)
        barrier.setScale(self.width, 1, height)

        internalNode.flattenStrong()

        # We need to set collisions on all of our knock knock doors:
        match = self.INDEX_REGEX.match(self.name)
        if match:
            index = int(match.group(1))
            for collisionNP in np.findAllMatches('**/door_*/+CollisionNode'):
                collisionNP.setName('KnockKnockDoorSphere_%d' % index)

        wallCollection = internalNode.findAllMatches('wall*')
        wallHolder = node.attachNewNode('wall_holder')
        wallDecal = node.attachNewNode('wall_decal')
        windowCollection = internalNode.findAllMatches('**/window*')
        doorCollection = internalNode.findAllMatches('**/door*')
        corniceCollection = internalNode.findAllMatches('**/cornice*_d')
        
        wallCollection.reparentTo(wallHolder)
        windowCollection.reparentTo(wallDecal)
        doorCollection.reparentTo(wallDecal)
        corniceCollection.reparentTo(wallDecal)

        for i in range(wallHolder.getNumChildren()):
            iNode = wallHolder.getChild(i)
            iNode.clearTag('DNACode')
            iNode.clearTag('DNARoot')

        wallHolder.flattenStrong()
        wallDecal.flattenStrong()

        holderChild0 = wallHolder.getChild(0)
        wallDecal.getChildren().reparentTo(holderChild0)
        holderChild0.reparentTo(internalNode)
        holderChild0.setEffect(DecalEffect.make())

        wallHolder.removeNode()
        wallDecal.removeNode()

registerElement(DNAFlatBuilding)
