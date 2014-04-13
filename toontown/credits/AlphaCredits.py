from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from toontown.toonbase import ToontownGlobals

class Shockley:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('Shockley')
        base.setBackgroundColor(0, 0, 0, 1)

        self.title = OnscreenText(text='Shockley', pos=(0.6, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Lead Developer\nNetwork Administraitor\nAstron Team', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/11-17-13_garden.jpg', pos=(-0.5, -1, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            # This fades in during the election's WrapUp state to prevent jittering when loading this first scene.
            Wait(3),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 0)), self.description.colorScaleInterval(0.5, (1, 1, 1, 0)), self.image.colorScaleInterval(0.5, (1, 1, 1, 0))),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()

class SirMax:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('SirMax')

        self.title = OnscreenText(text='Sir Max', pos=(0.55, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Team Lead\nCommunity Manager\nDeveloper', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/10-29-13_cannon.jpg', pos=(-0.5, -1, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 1)), self.description.colorScaleInterval(0.5, (1, 1, 1, 1)), self.image.colorScaleInterval(0.5, (1, 1, 1, 1))),
            Wait(3),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 0)), self.description.colorScaleInterval(0.5, (1, 1, 1, 0)), self.image.colorScaleInterval(0.5, (1, 1, 1, 0))),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()

class FatMcStink:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('FatMcStink')

        self.title = OnscreenText(text='Fat McStink', pos=(-0.6, 0.1, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Server Administraitor\nWeb Backend Development\nDeveloper', pos=(-0.1, 0.0, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ARight)
        self.image = OnscreenImage(image='phase_4/maps/news/11-8-13_pieornot.jpg', pos=(0.5, 1, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 1)), self.description.colorScaleInterval(0.5, (1, 1, 1, 1)), self.image.colorScaleInterval(0.5, (1, 1, 1, 1))),
            Wait(3),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 0)), self.description.colorScaleInterval(0.5, (1, 1, 1, 0)), self.image.colorScaleInterval(0.5, (1, 1, 1, 0))),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()

class McQuack:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('McQuack')

        self.title = OnscreenText(text='McQuack', pos=(0.55, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Expert of Explosives\nDeveloper\nAstron Team', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/12-28-13-hiatus.jpg', pos=(-0.5, -1, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 1)), self.description.colorScaleInterval(0.5, (1, 1, 1, 1)), self.image.colorScaleInterval(0.5, (1, 1, 1, 1))),
            Wait(3),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 0)), self.description.colorScaleInterval(0.5, (1, 1, 1, 0)), self.image.colorScaleInterval(0.5, (1, 1, 1, 0))),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()
        
class Hawkheart:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('Hawkheart')

        self.title = OnscreenText(text='Hawkheart', pos=(0.65, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Fish Bingo Controller\nDeveloper', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/11-11-13_bingo.jpg', pos=(-0.5, -1, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 1)), self.description.colorScaleInterval(0.5, (1, 1, 1, 1)), self.image.colorScaleInterval(0.5, (1, 1, 1, 1))),
            Wait(3),
            Parallel(self.title.colorScaleInterval(0.5, (1, 1, 1, 0)), self.description.colorScaleInterval(0.5, (1, 1, 1, 0)), self.image.colorScaleInterval(0.5, (1, 1, 1, 0))),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()

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