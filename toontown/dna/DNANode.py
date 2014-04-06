from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *

class DNANode(DNAGroup):
    TAG = 'node'

registerElement(DNANode)
