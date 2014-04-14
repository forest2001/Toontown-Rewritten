from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from toontown.toonbase import ToontownGlobals

def doFade(fade, elements):
    if fade == 'in':
        for node in elements:
            Sequence(node.colorScaleInterval(0.5, (1, 1, 1, 1))).start()
    elif fade == 'out':
        for node in elements:
            Sequence(node.colorScaleInterval(0.5, (1, 1, 1, 0))).start()

class Shockley:
    def __init__(self):
        self.sceneRoot = None

    def load(self):
        self.sceneRoot = NodePath('Shockley')
        base.setBackgroundColor(0, 0, 0, 1)

        self.title = OnscreenText(text='Shockley', pos=(0.6, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Lead Developer\nNetwork Technician\nGame Systems Engineer', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/11-17-13_garden.jpg', pos=(-0.5, 0.0, 0.0), scale=(0.5, 0.30, 0.30))

        self.elements = [self.title, self.description, self.image]
        for node in self.elements:
            node.setTransparency(1)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            # This fades in during the election's WrapUp state to prevent jittering when loading this first scene.
            Wait(3),
            Func(doFade, 'out', self.elements),
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

        self.title = OnscreenText(text='Sir Max', pos=(0.45, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Team Lead\nCommunity Manager\nWriter\nDeveloper', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/10-29-13_cannon.jpg', pos=(-0.5, 0.0, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Func(doFade, 'in', self.elements),
            Wait(3),
            Func(doFade, 'out', self.elements),
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

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Func(doFade, 'in', self.elements),
            Wait(3),
            Func(doFade, 'out', self.elements),
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

        self.title = OnscreenText(text='McQuack', pos=(-0.6, 0.1, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Expert of Explosives\nDeveloper\nAstron Team', pos=(-0.1, 0.0, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/12-28-13-hiatus.jpg', pos=(0.5, 1, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Func(doFade, 'in', self.elements),
            Wait(3),
            Func(doFade, 'out', self.elements),
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
        self.image = OnscreenImage(image='phase_4/maps/news/11-11-13_bingo.jpg', pos=(-0.5, 0.0, 0.0), scale=(0.5, 0.30, 0.30))

        elements = [self.title, self.description, self.image]
        for node in elements:
            node.setTransparency(1)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Func(doFade, 'in', self.elements),
            Wait(3),
            Func(doFade, 'out', self.elements),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()