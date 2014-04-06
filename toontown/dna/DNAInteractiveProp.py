from DNAProp import DNAProp
from DNAParser import *
from panda3d.core import *

class DNAInteractiveProp(DNAProp):
    TAG = 'interactive_prop'

    def __init__(self, name, code, anim, cell_id='0'):
        DNAProp.__init__(self, name, code)

        self.anim = anim
        self.cell_id = int(cell_id)


registerElement(DNAInteractiveProp)
