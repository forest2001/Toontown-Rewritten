from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

class TestScene1:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('scene1')
        tn = TextNode('text')
        tn.setText('Hello world!')
        tn.setAlign(tn.ACenter)
        self.tnnp = self.sceneRoot.attachNewNode(tn)
        self.tnnp.setPos(0, 5, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            self.tnnp.hprInterval(10, (0, 0, 360)),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()

class TestScene2:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('scene1')
        tn = TextNode('text')
        tn.setText('Scene #2!')
        self.tnnp = self.sceneRoot.attachNewNode(tn)
        self.tnnp.setPos(10, 5, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            self.tnnp.posInterval(10, (-10, 5, 0)),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
