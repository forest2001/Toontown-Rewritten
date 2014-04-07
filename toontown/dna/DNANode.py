from DNAGroup import DNAGroup
from DNAParser import *
from panda3d.core import *
# For the get* helpers:
from DNAPos import DNAPos
from DNAHpr import DNAHpr
from DNAColor import DNAColor
from DNAScale import DNAScale

class DNANode(DNAGroup):
    TAG = 'node'

    def __getAttribute(self, type, member, default):
        children = self.findChildren(type)
        if not children:
            return default
        else:
            return getattr(children[0], member)

    def getPos(self):
        return self.__getAttribute(DNAPos, 'pos', (0.0, 0.0, 0.0))

    def getHpr(self):
        return self.__getAttribute(DNAHpr, 'hpr', (0.0, 0.0, 0.0))

    def getScale(self):
        return self.__getAttribute(DNAScale, 'scale', (1.0, 1.0, 1.0))

    def getColor(self):
        return self.__getAttribute(DNAColor, 'color', (1.0, 1.0, 1.0, 1.0))

registerElement(DNANode)
