from panda3d.core import *
import math

class DNATypesetter:
    # DNATypesetter is for signs: it takes the baseline parameters and a series
    # of texts to produce a NodePath which contains the already-typeset geometry.
    def __init__(self, baseline, dnaStorage):
        self.baseline = baseline
        self.dnaStorage = dnaStorage

    def generate(self, texts):
        root = NodePath('typesetter')

        x = 0.0
        for i,text in enumerate(texts):
            tn = TextNode('text')
            tn.setText(text)
            font = self.dnaStorage.findFont(self.baseline.code)
            if font is None:
                font = TextProperties.getDefaultFont()
                3/0
            tn.setFont(font)

            # If this is the first glyph, and we've got the 'b' flag, we need
            # to make it 'b'igger.
            if i==0 and 'b' in self.baseline.flags:
                tn.setTextScale(1.5)

            np = root.attachNewNode(tn)
            np.setDepthWrite(0)
            if i&1:
                np.setPos(x+self.baseline.stumble, 0, self.baseline.stomp)
                np.setR(-self.baseline.wiggle)
            else:
                np.setPos(x-self.baseline.stumble, 0, -self.baseline.stomp)
                np.setR(self.baseline.wiggle)
            x += tn.getWidth() + self.baseline.kern

        # Center...
        for child in root.getChildren():
            child.setX(child.getX()-x/2)

        # Is there a width+height on the baseline? If so, we have to curve:
        if self.baseline.width != 0.0 and self.baseline.height != 0.0:
            ellipse = DNAEllipseFormatter(self.baseline)
            ellipse.process(root)

        # Generate all TextNodes to GeomNodes, then flatten:
        for np in root.findAllMatches('**/+TextNode'):
            tn = np.node().generate()
            np2 = np.getParent().attachNewNode(tn)
            np2.setTransform(np.getTransform())
            np.removeNode()
        root.flattenStrong()

        # If and only if there is any text, we should have exactly one child:
        if root.getNumChildren():
            return root.getChild(0)
        else:
            return None

class DNAEllipseFormatter:
    # This class curves the text if a width/height is specified.
    def __init__(self, baseline):
        self.baseline = baseline

        # It's /2 because the height/width is specified as "diameter" while
        # elliptical calculations are done with radius axes.
        self.a = self.baseline.width/2.
        self.b = self.baseline.height/2.

    def arc(self, x):
        # TODO: This function needs to calculate the inverse arc length along
        # the ellipse so it can map x to theta. Currently, this assumes that
        # the region is completely circular.
        return x/self.b

    def process(self, np):
        for node in np.getChildren():
            theta = self.arc(node.getX())
            deviation = node.getY()

            # Apply indent:
            theta += self.baseline.indent * math.pi/180

            x, y = math.sin(theta)*self.a, (math.cos(theta)-1)*self.b
            radius = math.sqrt(x*x + y*y)
            if radius > 0.0:
                x *= (radius+deviation)/radius
                y *= (radius+deviation)/radius

            node.setPos(x, 0, y)
            node.setR(node, theta * 180/math.pi)
