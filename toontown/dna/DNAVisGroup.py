from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *

class DNAVisGroup(DNAGroup):
    TAG = 'visgroup'

    def __init__(self, zone, vis=''):
        DNAGroup.__init__(self, zone)

        self.zone = zone
        self.vis = vis.split()

    def getZone(self):
        pos = self.zone.find(':')
        if pos != -1:
            return int(self.zone[:pos])
        else:
            return int(self.zone)

    def getVisibleZones(self):
        return map(int, self.vis)

    def _storeData(self, data):
        # Store the VisGroup's existence into the DNASceneData:
        data.visgroups.append(self)

    def getVisGroup(self):
        return self

registerElement(DNAVisGroup)
