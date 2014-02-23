from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import *
from toontown.toon import NPCToons

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

class FlippyScene:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('scene1')
        tn = TextNode('text')
        tn.setText('Flippy')
        tn.setAlign(tn.ACenter)
        self.tnnp = self.sceneRoot.attachNewNode(tn)
        self.tnnp.setPos(20, 30, 2)

        self.flippy = NPCToons.createLocalNPC(2001)
        self.flippy.reparentTo(self.sceneRoot)
        self.flippy.setPos(0, 10, -5)
        self.flippy.setH(180)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Func(self.flippy.setChatAbsolute, 'UNITE!', CFSpeech|CFTimeout),
            Parallel(ActorInterval(self.flippy, 'victory', playRate=0.75, startFrame=0, endFrame=9), self.tnnp.posHprInterval(0.5, (5, 25, 3), (0, 0, 10))),
            self.tnnp.posHprInterval(2, (4, 26, 3), (5, 0, 30)),
            Parallel(ActorInterval(self.flippy, 'victory', playRate=0.75, startFrame=9, endFrame=0), self.tnnp.posHprInterval(0.5, (0, 30, 15), (0, 0, -30))),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()