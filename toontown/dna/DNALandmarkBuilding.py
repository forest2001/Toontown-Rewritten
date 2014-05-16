from DNANode import DNANode
from DNAParser import *
from DNATitle import DNATitle
import DNAUtil
from DNAVisGroup import DNAVisGroup
from panda3d.core import *

class DNALandmarkBuilding(DNANode):
    TAG = 'landmark_building'

    def __init__(self, id, code, type=None):
        DNANode.__init__(self, id)

        self.id = id
        self.code = code
        self.type = type

    def getTitle(self):
        return self._getAttribute(DNATitle, 'title', '')

    def setupSuitBuildingOrigin(self, nodePath):
        building = DNAUtil.getBuildingClassFromName(self.id)
        if building != 'tb':
            return

        name = 'sb' + self.id[2:]

        node = nodePath.find('**/*suit_building_origin')
        if node.isEmpty():
            #TODO: dna logging
            #print 'DNALandmarkBuilding ' + name + ' did not find **/*suit_building_origin'
            node = nodePath.attachNewNode(ModelNode(self.name))
        else:
            node.wrtReparentTo(nodePath)
            node.setName(name)

        node.node().setPreserveTransform(ModelNode.PTNet)
        node.hide()

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            #TODO: dna logging
            #raise DNAError('DNALandmarkBuilding uses unknown code %s' % self.code)
            pass
        np = node.copyTo(parent)
        np.setName(self.id)

        self.setupSuitBuildingOrigin(np)

        return np

    def _postGenerate(self, storage, np):
        np.flattenStrong()

    def _storeData(self, data):
        block = data.getBlock(DNAUtil.getBlockFromName(self.id))
        block.title = self.getTitle()
        block.buildingType = self.type
        block.zone = self.getVisGroup().getZone()
        block.node = self

registerElement(DNALandmarkBuilding)
