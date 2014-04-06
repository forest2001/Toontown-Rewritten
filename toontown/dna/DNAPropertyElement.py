from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNAPropertyElement(DNASceneElement):
    PARENTS = ['prop', 'anim_prop', 'interactive_prop', 'node', 'flat_building',
               'landmark_building', 'door', 'flat_door', 'wall', 'windows',
               'cornice', 'sign', 'baseline', 'street']

    def _makeNode(self, storage, parent):
        # We don't return a node, because this is a property.
        self._apply(parent)

    def _apply(self, parent):
        pass # Overridden by subclass.
