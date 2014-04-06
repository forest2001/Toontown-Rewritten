from DNASceneElement import DNASceneElement
from DNAParser import *
from panda3d.core import *

class DNASceneRoot(DNASceneElement):
    TAG = 'scene'
    PARENTS = [None]

    def __init__(self, zone=None):
        DNASceneElement.__init__(self)

        self.zone = zone

    def generate(self, storage):
        """
        Generate the scenegraph for this scene using the nodes, textures, and
        fonts stored within the provided DNAStorage object.
        """

        scene = NodePath('scene')
        for child in self._children:
            child._generate(storage, scene)
        return scene.node()

registerElement(DNASceneRoot)
