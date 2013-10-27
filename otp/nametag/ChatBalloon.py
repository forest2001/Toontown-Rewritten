from pandac.PandaModules import *

class ChatBalloon:
    TEXT_SHIFT = (0.1, 0, 1.1)
    TEXT_SHIFT_PROP = 0.08
    NATIVE_WIDTH = 10.0
    BUBBLE_PADDING = 0.3
    BUBBLE_PADDING_PROP = 0.05

    def __init__(self, model):
        self.model = model
        self.wordWrap = 15.0

    def generate(self, text, font, textColor=(0,0,0,1), balloonColor=(1,1,1,1)):
        root = NodePath('balloon')

        # Add balloon geometry:
        balloon = self.model.copyTo(root)
        top = balloon.find('**/top')
        middle = balloon.find('**/middle')
        bottom = balloon.find('**/bottom')

        balloon.setColor(balloonColor)
        if balloonColor[3] < 1.0:
            balloon.setTransparency(1)

        # Render the text into a TextNode, using the font:
        t = root.attachNewNode(TextNode('text'))
        t.node().setFont(font)
        t.node().setWordwrap(self.wordWrap)
        t.node().setText(text)
        t.node().setTextColor(textColor)

        width, height = t.node().getWidth(), t.node().getHeight()

        t.setDepthOffset(1)
        t.setPos(self.TEXT_SHIFT)
        t.setX(t, self.TEXT_SHIFT_PROP*width)
        t.setZ(t, height)

        # Set the balloon's size:
        width *= 1+self.BUBBLE_PADDING_PROP
        width += self.BUBBLE_PADDING
        balloon.setSx(width/self.NATIVE_WIDTH)
        middle.setSz(height)
        top.setZ(top, height-1)

        root.flattenStrong()
        return root
