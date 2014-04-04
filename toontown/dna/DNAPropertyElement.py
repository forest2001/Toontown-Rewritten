from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAPropertyElement(DNASceneElement):
    PARENTS = ['prop', 'node', 'flat_building', 'landmark_building', 'door',
               'wall', 'windows', 'cornice', 'sign', 'baseline']

    def _makeNode(self, storage, parent):
        # We don't return a node, because this is a property.
        self._apply(parent)

    def _apply(self, parent):
        pass # Overridden by subclass.
