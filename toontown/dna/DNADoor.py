from DNANode import DNANode
from DNAParser import *
import DNAUtil
from panda3d.core import *

class DNADoor(DNANode):
    TAG = 'door'
    PARENTS = ['landmark_building']

    def __init__(self, code):
        DNANode.__init__(self, 'door')

        self.code = code

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0,0,0), (0,0,0), (1,1,1))
        doorNodePath.setColor(color, 0)
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')
        doorFlat = doorNodePath.find('door_*_flat')
        leftHole.wrtReparentTo(doorFlat, 0)
        rightHole.wrtReparentTo(doorFlat, 0)
        doorFlat.setEffect(DecalEffect.make())
        rightDoor.wrtReparentTo(parentNode, 0)
        leftDoor.wrtReparentTo(parentNode, 0)

        rightDoor.setColor(color, 0)
        leftDoor.setColor(color, 0)
        leftHole.setColor((0,0,0,1), 0)
        rightHole.setColor((0,0,0,1), 0)

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2,2,2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + block)

        store = NodePath('door-%s' % block)
        store.setPosHprScale(doorNodePath, (0,0,0), (0,0,0), (1,1,1))

        return store

    def _makeNode(self, storage, parent):
        frontNode = parent.find('**/*building*_front')
        if frontNode.isEmpty():
            frontNode = parent.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        node = storage.findNode(self.code)
        if node is None:
            #raise DNAError('DNADoor code ' + self.code + ' not found in DNAStorage')
            #TODO: error message here
            pass
        doorNode = node.copyTo(frontNode, 0)
        self.setupDoor(doorNode, parent, parent.find('**/*door_origin'), storage,
          DNAUtil.getBlockFromName(parent.getName()), self.getColor())
        return doorNode

    def _storeData(self, data):
        block = data.getBlock(DNAUtil.getBlockFromName(self.parent.name))
        block.doorName = 'door-%s' % block.index

registerElement(DNADoor)
