from DNAAnimProp import DNAAnimProp
from DNAParser import *
from panda3d.core import *

class DNAInteractiveProp(DNAAnimProp):
    TAG = 'interactive_prop'

    def __init__(self, name, code, anim, cell_id='0'):
        DNAAnimProp.__init__(self, name, code, anim)

        self.cell_id = int(cell_id)

    def _makeNode(self, parent, storage):
        node = DNAAnimProp._makeNode(self, parent, storage)

        node.setTag('DNACellIndex', str(self.cell_id))

        return node

registerElement(DNAInteractiveProp)
