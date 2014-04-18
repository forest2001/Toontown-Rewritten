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
    elif fade == 'hide':
        for node in elements:
            node.setColorScale(1, 1, 1, 0)

class Shockley:
    def __init__(self, preload=False):
        self.sceneRoot = None
        self.preload = preload

    def load(self):
        self.sceneRoot = NodePath('Shockley')
        base.setBackgroundColor(0, 0, 0, 1)

        self.title = OnscreenText(text='Shockley ', pos=(0.6, 0.15, 0.0), scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=TextNode.ACenter)
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
            Wait(3),
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
    def __init__(self, name, description, image, side = 'left', number = 1, name2 = None, description2 = None, image2 = None, special = None):
        self.sceneRoot = None
        self.twoSlides = None
        self.toonName = name
        self.toonDescription = description
        self.toonImage = image
        self.side = side
        self.special = special # For special types of slides, like the final one
        if number > 1:
            self.toon2Name = name2
            self.toon2Description = description2
            self.toon2Image = image2
            self.twoSlides = True

    def load(self):
        self.sceneRoot = NodePath(self.toonName.replace(' ', '').replace('',''))
        base.setBackgroundColor(0, 0, 0, 1)

        if self.twoSlides:
            if self.side == 'left':
                # Left Top
                titlePos = (0.1, 0.5, 0.0)
                descriptionPos = (0.2, 0.4, 0.0)
                imagePos = (-0.55, 0.0, 0.4)
                textAlignment = TextNode.ALeft
                # Right Bottom
                title2Pos = (-0.1, -0.35, 0.0)
                description2Pos = (-0.1, -0.45, 0.0)
                image2Pos = (0.55, 0.0, -0.4)
                text2Alignment = TextNode.ARight
            else:
                # Right Top
                titlePos = (-0.1, 0.5, 0.0)
                descriptionPos = (-0.1, 0.4, 0.0)
                imagePos = (0.55, 0.0, 0.4)
                textAlignment = TextNode.ARight
                # Left Bottom
                title2Pos = (0.1, -0.35, 0.0)
                description2Pos = (0.25, -0.45, 0.0)
                image2Pos = (-0.55, 0.0, -0.4)
                text2Alignment = TextNode.ALeft
        elif self.side == 'left':
            # Left Middle
            titlePos = (0.1, 0.15, 0.0)
            descriptionPos = (0.2, 0.05, 0.0)
            imagePos = (-0.5, 0.0, 0.0)
            textAlignment = TextNode.ALeft
        else: 
            # Right Middle
            titlePos = (-0.1, 0.1, 0.0)
            descriptionPos = (-0.11, 0.0, 0.0)
            imagePos = (0.5, 0.0, 0.0)
            textAlignment = TextNode.ARight

        self.title = OnscreenText(text=self.toonName, pos=titlePos, scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=textAlignment)
        self.description = OnscreenText(text=self.toonDescription, pos=descriptionPos, scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=textAlignment)
        self.image = OnscreenImage(image='phase_4/maps/news/%s' % self.toonImage, pos=imagePos, scale=(0.5, 0.30, 0.30))
        self.elements = [self.title, self.description, self.image]
        
        if self.twoSlides:
            self.title2 = OnscreenText(text=self.toon2Name, pos=title2Pos, scale=(0.15), fg=(1, 1, 1, 1), font=ToontownGlobals.getSignFont(), align=text2Alignment)
            self.description2 = OnscreenText(text=self.toon2Description, pos=description2Pos, scale=(0.06), fg=(1, 1, 1, 1), font=ToontownGlobals.getMinnieFont(), align=text2Alignment)
            self.image2 = OnscreenImage(image='phase_4/maps/news/%s' % self.toon2Image, pos=image2Pos, scale=(0.5, 0.30, 0.30))
            self.elements.extend([self.title2, self.description2, self.image2])

        for node in self.elements:
            node.setTransparency(1)
            node.setColorScale(1, 1, 1, 0)

    def makeInterval(self):
        if self.special == 'final':
            # Hide the last slide, rather than fade out
            return Sequence(
                ParentInterval(self.sceneRoot, render),
                Func(doFade, 'in', self.elements),
                Wait(3),
                Func(doFade, 'hide', self.elements),
                ParentInterval(self.sceneRoot, hidden)
                )
        else:
            # Just a normal slide
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

CreditsScenes = [
                # Developers
                Shockley(),
                Credits('Sir Max', 'Team Lead\nCommunity Manager\nDeveloper', '10-29-13_cannon.jpg', 'left'),
                Credits('McQuack', 'Expert of Explosives\nDeveloper', '14-3-17_dontworryhesurvived.jpg', 'right', 2, 'Hawkheart', 'Fish Bingo Controller\nDeveloper', '11-11-13_bingo.jpg'),
                Credits('Fat McStink', 'Ultimate Party King\nServer Administraitor\nDeveloper', '11-8-13_pieornot.jpg', 'right'),
                Credits('Hamlet', 'Astron Team\nDeveloper', 'hamlet.jpg', 'left', 2, 'Muddy Paws', 'Expert Cake Baker\nMac Support\nDeveloper', 'muddy-paws.jpg'),
                Credits('Goshi', 'Self-proclaimed Police\nSupport Manager\nModerator', '14-4-1_itsabirthdefect-nothingsilly.jpg', 'right', 2, 'J.C.', 'Moral Support\nModerator', '11-2-13_whatdoesjcsay.jpg'),

                # Artists
                Credits('Capt. Sandy', '\n\nLead Art Director\nGraphic Designer\nConcept Artist', 'capt_sandy.jpg', 'left', 2, 'Boo Boo', 'Novice Painter\nTexture Artist', '03-4-19_kickedthebucket.jpg'),
                Credits('Slate', 'Texture Artist', '12-6-13_slate.jpg', 'right', 2, 'June', 'Texture Artist', 'roxys_joyful_uber.jpg'),

                # Too Many Secrets
                Credits('Too Many\nSecrets', '\n\nMany Secret Things\nDeveloper', 'toomanysecrets.jpg', 'left'),

                # Modelers
                Credits('Roger Dog', 'Roger Dog\n3D Modeler\nAnimator', '11-21-13_hiimrogerdog.jpg', 'left', 2, 'Flippy Cheezer', 'The Speedway Master\n3D Modeler\nCharacter Rigger', 'flippy_cheezer.jpg'),
                Credits('Scooter', 'Puzzle Piecer\nARG Organizer', '11-16-13_whatisthis.jpg', 'left', 2, 'Joshsora', 'Infinite Chatterbox\nFormer 3D Modeler', '12-21-13_theworldendedtodaylastyear.jpg'),

                # Composers
                Credits('Cool Peaches', 'Lead Composer\nElection Composer', 'flippy_cheezer.jpg', 'right', 2, 'Jethred', 'Theme Song Composer', 'flippy_cheezer.jpg'),

                # Special Thanks to:
                Credits('Disney Online', 'The owners and creators\nof Toontown.', '11-20-13_donald.jpg', 'left', 2, 'VR Studio', 'For developing Toontown Online.', '11-15-13_grey.jpg'),
                Credits('Jaymo', 'For his continued efforts\nto bring Toontown back.', '14-1-22_ohmanohmanOHMAN.jpg', 'left'),
                ]
