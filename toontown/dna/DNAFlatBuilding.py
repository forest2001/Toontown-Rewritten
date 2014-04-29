from DNANode import DNANode
from DNAFlatDoor import DNAFlatDoor
from DNAParser import *
import DNAUtil
from panda3d.core import *
import re

class DNAFlatBuilding(DNANode):
    TAG = 'flat_building'

    def __init__(self, id, width="0"):
        DNANode.__init__(self, id)

        self.id = id
        self.width = float(width)

    def _makeNode(self, storage, parent):
        return parent.attachNewNode(self.id)

    def _postGenerate(self, storage, np):
        height = np.getPythonTag('wall_height') or 0.0
        np.clearPythonTag('wall_height')

        # First, set up collisions. We need a (self.width, height)-sized square.
        barrierNode = storage.findNode('wall_camera_barrier')
        if not barrierNode:
            raise DNAError('No wall_camera_barrier in storage.')

        barrier = barrierNode.copyTo(np)
        barrier.setScale(self.width, 1, height)

        if 'safe_zone' not in str(np.getParent()):
            type = DNAUtil.getBuildingClassFromName(self.id)
            if type == 'tb':
                self.generateSuitGeometry(storage, np, height, barrier)

        # We need to set collisions on all of our knock knock doors:
        block = DNAUtil.getBlockFromName(self.name)
        if block is not None:
            for collisionNP in np.findAllMatches('**/door_*/+CollisionNode'):
                collisionNP.setName('KnockKnockDoorSphere_%d' % block)

        # Finally, flatten down:
        np.flattenStrong()

    def generateSuitGeometry(self, storage, np, height, barrier):
        node = np.getParent().attachNewNode('sb' + self.id[2:])
        node.setTransform(np.getTransform())

        barrier.copyTo(node)

        strIndex = str(abs(node.getPos().length()))
        if strIndex != '.':
            index = int(strIndex[1:2])
            wall = storage.findNode(storage.getCatalogCode('suit_wall', int(index)))
        else:
            wall = storage.findNode(storage.getCatalogCode('suit_wall', 0))

        if wall:
            wallNode = wall.copyTo(node)
            wallNode.setScale(self.width, 1, height)

            for door in DNAUtil.getChildrenOfType(self, DNAFlatDoor):
                door.generateSuitGeometry(storage, wallNode)

        node.flattenStrong()
        node.stash()

registerElement(DNAFlatBuilding)
