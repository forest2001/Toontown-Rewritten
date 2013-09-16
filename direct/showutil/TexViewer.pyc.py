# 2013.08.22 22:14:52 Pacific Daylight Time
# Embedded file name: direct.showutil.TexViewer
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class TexViewer(DirectObject):
    __module__ = __name__

    def __init__(self, tex):
        self.tex = tex
        self.cleanedUp = False
        self.root = aspect2d.attachNewNode('texViewer')
        self.root.setBin('gui-popup', 10000)
        cards = self.root.attachNewNode('cards')
        cm = CardMaker('left')
        l, r, b, t = (-1,
         -0.1,
         0,
         0.9)
        cm.setFrame(l, r, b, t)
        left = cards.attachNewNode(cm.generate())
        left.setTexture(self.tex)
        left.setTransparency(TransparencyAttrib.MAlpha)
        ls = LineSegs('frame')
        ls.setColor(0, 0, 0, 1)
        ls.moveTo(l, 0, b)
        ls.drawTo(r, 0, b)
        ls.drawTo(r, 0, t)
        ls.drawTo(l, 0, t)
        ls.drawTo(l, 0, b)
        cards.attachNewNode(ls.create())
        if self.tex.hasSimpleRamImage():
            self.t2 = Texture('simple')
            self.t2.setup2dTexture(self.tex.getSimpleXSize(), self.tex.getSimpleYSize(), Texture.TUnsignedByte, Texture.FRgba8)
            self.t2.setRamImage(self.tex.getSimpleRamImage())
            self.t2.setMagfilter(Texture.FTNearest)
            cm = CardMaker('right')
            l, r, b, t = (0.1, 1, 0, 0.9)
            cm.setFrame(l, r, b, t)
            right = cards.attachNewNode(cm.generate())
            right.setTexture(self.t2)
            right.setTransparency(TransparencyAttrib.MAlpha)
            ls = LineSegs('frame')
            ls.setColor(0, 0, 0, 1)
            ls.moveTo(l, 0, b)
            ls.drawTo(r, 0, b)
            ls.drawTo(r, 0, t)
            ls.drawTo(l, 0, t)
            ls.drawTo(l, 0, b)
            cards.attachNewNode(ls.create())
        if self.tex.getXSize() > self.tex.getYSize():
            cards.setScale(1, 1, float(self.tex.getYSize()) / self.tex.getXSize())
        else:
            cards.setScale(float(self.tex.getXSize()) / self.tex.getYSize(), 1, 1)
        tn = TextNode('label')
        tn.setShadow(0.1, 0.1)
        tn.setText(self.tex.getName())
        tn.setAlign(tn.ACenter)
        tnp = self.root.attachNewNode(tn)
        tnp.setScale(0.1)
        tnp.setPos(0, 0, -tn.getHeight() * 0.1)

    def cleanup(self):
        if not self.cleanedUp:
            self.root.removeNode()
            self.cleanedUp = True
            self.tex = None
            self.t2 = None
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showutil\TexViewer.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:52 Pacific Daylight Time
