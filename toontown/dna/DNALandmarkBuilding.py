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
        return DNANode._DNANode__getAttribute(self, DNATitle, 'title', '')

    def setupSuitBuildingOrigin(self, nodePathA, nodePathB):
        if self.id[0:2] == 'tb' and self.id[2].isdigit() and self.id.find(':') != -1:
            name = self.id
            name = 's' + name[1:]
            node = nodePathB.find('**/*suit_building_origin')
            if node.isEmpty():
                #TODO: dna logging
                #print 'DNALandmarkBuilding ' + name + ' did not find **/*suit_building_origin'
                node = nodePathA.attachNewNode(self.name)
                node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
            else:
                node.wrtReparentTo(nodePathA, 0)
                node.setName(name)
            node.hide()

    def _makeNode(self, storage, parent):
        node = storage.findNode(self.code)
        if node is None:
            #TODO: dna logging
            #raise DNAError('DNALandmarkBuilding uses unknown code %s' % self.code)
            pass
        self.node = node.copyTo(parent)
        self.node.setName(self.id)
        self.node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())

        self.setupSuitBuildingOrigin(self.node, self.node)
        gr = SceneGraphReducer()
        gr.flatten(self.node.getNode(0), 0)
        return self.node

    def _storeData(self, data):
        block = data.getBlock(DNAUtil.getBlock(self.name))
        block.title = self.getTitle()
        block.buildingType = self.type
        block.zone = self.getVisGroup().getZone()

registerElement(DNALandmarkBuilding)
