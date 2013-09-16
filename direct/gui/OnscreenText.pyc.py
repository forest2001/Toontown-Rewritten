# 2013.08.22 22:14:19 Pacific Daylight Time
# Embedded file name: direct.gui.OnscreenText
__all__ = ['OnscreenText',
 'Plain',
 'ScreenTitle',
 'ScreenPrompt',
 'NameConfirm',
 'BlackOnWhite']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from direct.showbase.DirectObject import DirectObject
import string, types
Plain = 1
ScreenTitle = 2
ScreenPrompt = 3
NameConfirm = 4
BlackOnWhite = 5

class OnscreenText(DirectObject, NodePath):
    __module__ = __name__

    def __init__(self, text = '', style = Plain, pos = (0, 0), roll = 0, scale = None, fg = None, bg = None, shadow = None, shadowOffset = (0.04, 0.04), frame = None, align = None, wordwrap = None, drawOrder = None, decal = 0, font = None, parent = None, sort = 0, mayChange = True):
        if parent == None:
            parent = aspect2d
        textNode = TextNode('')
        self.textNode = textNode
        NodePath.__init__(self)
        if style == Plain:
            if not scale:
                scale = 0.07
                if not fg:
                    fg = (0, 0, 0, 1)
                    if not bg:
                        bg = (0, 0, 0, 0)
                        if not shadow:
                            shadow = (0, 0, 0, 0)
                            if not frame:
                                frame = (0, 0, 0, 0)
                                if align == None:
                                    align = TextNode.ACenter
                            elif style == ScreenTitle:
                                if not scale:
                                    scale = 0.15
                                    fg = fg or (1, 0.2, 0.2, 1)
                                    bg = bg or (0, 0, 0, 0)
                                    shadow = shadow or (0, 0, 0, 1)
                                    frame = frame or (0, 0, 0, 0)
                                    align = align == None and TextNode.ACenter
                            elif style == ScreenPrompt:
                                if not scale:
                                    scale = 0.1
                                    fg = fg or (1, 1, 0, 1)
                                    bg = bg or (0, 0, 0, 0)
                                    shadow = shadow or (0, 0, 0, 1)
                                    frame = frame or (0, 0, 0, 0)
                                    align = align == None and TextNode.ACenter
                            elif style == NameConfirm:
                                if not scale:
                                    scale = 0.1
                                    fg = fg or (0, 1, 0, 1)
                                    bg = bg or (0, 0, 0, 0)
                                    shadow = shadow or (0, 0, 0, 0)
                                    frame = frame or (0, 0, 0, 0)
                                    align = align == None and TextNode.ACenter
                            elif style == BlackOnWhite:
                                if not scale:
                                    scale = 0.1
                                    fg = fg or (0, 0, 0, 1)
                                    bg = bg or (1, 1, 1, 1)
                                    shadow = shadow or (0, 0, 0, 0)
                                    frame = frame or (0, 0, 0, 0)
                                    align = align == None and TextNode.ACenter
                            else:
                                raise ValueError
                            if not isinstance(scale, types.TupleType):
                                scale = (scale, scale)
                            self.scale = scale
                            self.pos = pos
                            self.roll = roll
                            self.wordwrap = wordwrap
                            if decal:
                                textNode.setCardDecal(1)
                            if font == None:
                                font = DGG.getDefaultFont()
                            textNode.setFont(font)
                            textNode.setTextColor(fg[0], fg[1], fg[2], fg[3])
                            textNode.setAlign(align)
                            if wordwrap:
                                textNode.setWordwrap(wordwrap)
                            if bg[3] != 0:
                                textNode.setCardColor(bg[0], bg[1], bg[2], bg[3])
                                textNode.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
                            shadow[3] != 0 and textNode.setShadowColor(shadow[0], shadow[1], shadow[2], shadow[3])
                            textNode.setShadow(*shadowOffset)
                        frame[3] != 0 and textNode.setFrameColor(frame[0], frame[1], frame[2], frame[3])
                        textNode.setFrameAsMargin(0.1, 0.1, 0.1, 0.1)
                    self.updateTransformMat()
                    drawOrder != None and textNode.setBin('fixed')
                    textNode.setDrawOrder(drawOrder)
                self.setText(text)
                self.mayChange = text or 1
            else:
                self.mayChange = mayChange
            self.textNode = self.mayChange or textNode.generate()
        self.isClean = 0
        self.assign(parent.attachNewNode(self.textNode, sort))
        return

    def cleanup(self):
        self.textNode = None
        if self.isClean == 0:
            self.isClean = 1
            self.removeNode()
        return

    def destroy(self):
        self.cleanup()

    def freeze(self):
        pass

    def thaw(self):
        pass

    def setDecal(self, decal):
        self.textNode.setCardDecal(decal)

    def getDecal(self):
        return self.textNode.getCardDecal()

    def setFont(self, font):
        self.textNode.setFont(font)

    def getFont(self):
        return self.textNode.getFont()

    def clearText(self):
        self.textNode.clearText()

    def setText(self, text):
        self.unicodeText = isinstance(text, types.UnicodeType)
        if self.unicodeText:
            self.textNode.setWtext(text)
        else:
            self.textNode.setText(text)

    def appendText(self, text):
        if isinstance(text, types.UnicodeType):
            self.unicodeText = 1
        if self.unicodeText:
            self.textNode.appendWtext(text)
        else:
            self.textNode.appendText(text)

    def getText(self):
        if self.unicodeText:
            return self.textNode.getWtext()
        else:
            return self.textNode.getText()

    def setX(self, x):
        self.setPos(x, self.pos[1])

    def setY(self, y):
        self.setPos(self.pos[0], y)

    def setPos(self, x, y):
        self.pos = (x, y)
        self.updateTransformMat()

    def getPos(self):
        return self.pos

    def setRoll(self, roll):
        self.roll = roll
        self.updateTransformMat()

    def getRoll(self):
        return self.roll

    def setScale(self, sx, sy = None):
        if sy == None:
            if isinstance(sx, types.TupleType):
                self.scale = sx
            else:
                self.scale = (sx, sx)
        else:
            self.scale = (sx, sy)
        self.updateTransformMat()
        return

    def updateTransformMat(self):
        mat = Mat4.scaleMat(self.scale[0], 1, self.scale[1]) * Mat4.rotateMat(self.roll, Vec3(0, -1, 0)) * Mat4.translateMat(self.pos[0], 0, self.pos[1])
        self.textNode.setTransform(mat)

    def getScale(self):
        return self.scale

    def setWordwrap(self, wordwrap):
        self.wordwrap = wordwrap
        if wordwrap:
            self.textNode.setWordwrap(wordwrap)
        else:
            self.textNode.clearWordwrap()

    def getWordwrap(self):
        return self.wordwrap

    def setFg(self, fg):
        self.textNode.setTextColor(fg[0], fg[1], fg[2], fg[3])

    def setBg(self, bg):
        if bg[3] != 0:
            self.textNode.setCardColor(bg[0], bg[1], bg[2], bg[3])
            self.textNode.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
        else:
            self.textNode.clearCard()

    def setShadow(self, shadow):
        if shadow[3] != 0:
            self.textNode.setShadowColor(shadow[0], shadow[1], shadow[2], shadow[3])
            self.textNode.setShadow(0.04, 0.04)
        else:
            self.textNode.clearShadow()

    def setFrame(self, frame):
        if frame[3] != 0:
            self.textNode.setFrameColor(frame[0], frame[1], frame[2], frame[3])
            self.textNode.setFrameAsMargin(0.1, 0.1, 0.1, 0.1)
        else:
            self.textNode.clearFrame()

    def configure(self, option = None, **kw):
        if not self.mayChange:
            print 'OnscreenText.configure: mayChange == 0'
            return
        for option, value in kw.items():
            try:
                setter = eval('self.set' + string.upper(option[0]) + option[1:])
                if setter == self.setPos:
                    setter(value[0], value[1])
                else:
                    setter(value)
            except AttributeError:
                print 'OnscreenText.configure: invalid option:', option

    def __setitem__(self, key, value):
        apply(self.configure, (), {key: value})

    def cget(self, option):
        getter = eval('self.get' + string.upper(option[0]) + option[1:])
        return getter()

    def setAlign(self, align):
        self.textNode.setAlign(align)

    __getitem__ = cget
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\OnscreenText.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:20 Pacific Daylight Time
