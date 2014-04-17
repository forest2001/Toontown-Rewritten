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

# Developers
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
            Wait(3.5),
            Func(doFade, 'out', self.elements),
            Wait(0.5),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()

class Credits:
    def __init__(self, name, description, image, side = 'Left'):
        self.sceneRoot = None
        self.toonName = name
        self.toonDescription = description
        self.toonImage = image
        self.side = side

    def load(self):
        self.sceneRoot = NodePath(self.toonName.replace(' ', '').replace('',''))
        base.setBackgroundColor(0, 0, 0, 1)

        titlePos = None
        descriptionPos = None
        imagePos = None
        textAlignment = None
        if self.side == 'Left':
            titlePos = (0.6, 0.15, 0.0)
            descriptionPos = (0.25, 0.05, 0.0)
            imagePos = (-0.5, 0.0, 0.0)
            textAlignment = TextNode.ALeft
        else:
            titlePos = (-0.6, 0.1, 0.0)
            descriptionPos = (-0.1, 0.0, 0.0)
            imagePos = (0.5, 1, 0.0)
            textAlignment = TextNode.ARight

        self.title = OnscreenText(text=self.toonName, pos=titlePos, scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text=self.toonDescription, pos=descriptionPos, scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=textAlignment)
        self.image = OnscreenImage(image='phase_4/maps/news/%s' % self.toonImage, pos=imagePos, scale=(0.5, 0.30, 0.30))

        self.elements = [self.title, self.description, self.image]
        for node in self.elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        return Sequence(
            ParentInterval(self.sceneRoot, render),
            Func(doFade, 'in', self.elements),
            Wait(3.5),
            Func(doFade, 'out', self.elements),
            Wait(0.5),
            ParentInterval(self.sceneRoot, hidden)
            )

    def unload(self):
        self.sceneRoot.removeNode()
        self.title.removeNode()
        self.description.removeNode()
        self.image.removeNode()
        self.elements = None
        self.toonName = None
        self.toonDescription = None
        self.toonImage = None
        self.side = None
