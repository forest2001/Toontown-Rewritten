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
    def __init__(self, preload=False):
        self.sceneRoot = None
        self.preload = preload

    def load(self):
        self.sceneRoot = NodePath('Shockley')
        base.setBackgroundColor(0, 0, 0, 1)

        self.title = OnscreenText(text='Shockley', pos=(0.6, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
        self.description = OnscreenText(text='Lead Developer\nNetwork Technician\nGame Systems Engineer', pos=(0.25, 0.05, 0.0), scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=TextNode.ALeft)
        self.image = OnscreenImage(image='phase_4/maps/news/11-17-13_garden.jpg', pos=(-0.5, 0.0, 0.0), scale=(0.5, 0.30, 0.30))

        self.elements = [self.title, self.description, self.image]
        for node in self.elements:
            node.setTransparency(1)
            if self.preload:
                node.setColorScale(1, 1, 1, 0)

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
    def __init__(self, name, description, image, side = 'left'):
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
        if self.side == 'left':
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

class Survivor:
    def __init__(self, toonName):
        self.toonName = toonName
        print('Saved toon name is: %s' % self.toonName)

AlphaCreditsScenes = [
                # Developers
                Shockley(),
                Credits('Sir Max', 'Team Lead\nCommunity Manager\nWriter\nDeveloper', '10-29-13_cannon.jpg', 'left'),
                Credits('Fat McStink', 'Server Administraitor\nWeb Backend Development\nDeveloper', '11-8-13_pieornot.jpg', 'right'),
                Credits('McQuack', 'Expert of Explosives\nDeveloper\nAstron Team', '12-28-13-hiatus.jpg', 'right'),
                Credits('Hawkheart', 'Fish Bingo Controller\nDeveloper', '11-11-13_bingo.jpg', 'left'),
                Credits('Hamlet', 'Astron Team\nDeveloper', 'hamlet.jpg', 'left'),
                Credits('Muddy Paws', 'Expert Cake Maker\nDeveloper\nMac Team', 'muddy-paws.jpg', 'right'),
                Credits('Goshi', 'Support Manager\nModerator', '14-4-1_itsabirthdefect-nothingsilly.jpg', 'right'),
                Credits('Too Many Secrets', 'Many Secret Things\nDeveloper', 'toomanysecrets.jpg', 'left'),

                # Artists
                Credits('Capt. Sandy', 'Lead Graphic Designer\nConcept Artist\nSite Designer\nArtist', 'capt_sandy.jpg', 'left'),
                Credits('Slate Blue\nRabbit', '\n\nTexture Artist', 'slate.jpg', 'right'),
                Credits('Roxy\'s Joyful\nUber', '\n\nTexture Artist', 'roxys_joyful_uber.jpg', 'right'),
                Credits('Roger Dog', '3D Modeler\nArtist', 'roger_dog.jpg', 'left'),
                Credits('Flippy Cheezer', '3D Modeler\nArtist', 'flippy_cheezer.jpg', 'left'),
                Credits('Boo Boo', 'Novice Construction Painter\nTexture Artist', '03-4-19_kickedthebucket.jpg', 'right'),
                ]
