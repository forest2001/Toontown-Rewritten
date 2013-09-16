# 2013.08.22 22:14:13 Pacific Daylight Time
# Embedded file name: direct.gui.DirectEntry
__all__ = ['DirectEntry']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *
from OnscreenText import OnscreenText
import string, types
import encodings.utf_8
from direct.showbase.DirectObject import DirectObject
ENTRY_FOCUS_STATE = PGEntry.SFocus
ENTRY_NO_FOCUS_STATE = PGEntry.SNoFocus
ENTRY_INACTIVE_STATE = PGEntry.SInactive

class DirectEntry(DirectFrame):
    __module__ = __name__
    directWtext = ConfigVariableBool('direct-wtext', 1)
    AllowCapNamePrefixes = ('Al', 'Ap', 'Ben', 'De', 'Del', 'Della', 'Delle', 'Der', 'Di', 'Du', 'El', 'Fitz', 'La', 'Las', 'Le', 'Les', 'Lo', 'Los', 'Mac', 'St', 'Te', 'Ten', 'Van', 'Von')
    ForceCapNamePrefixes = ("D'", 'DeLa', "Dell'", "L'", "M'", 'Mc', "O'")

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGEntry, None),
         ('numStates', 3, None),
         ('state', DGG.NORMAL, None),
         ('entryFont', None, DGG.INITOPT),
         ('width', 10, self.setup),
         ('numLines', 1, self.setup),
         ('focus', 0, self.setFocus),
         ('cursorKeys', 1, self.setCursorKeysActive),
         ('obscured', 0, self.setObscureMode),
         ('backgroundFocus', 0, self.setBackgroundFocus),
         ('initialText', '', DGG.INITOPT),
         ('command', None, None),
         ('extraArgs', [], None),
         ('failedCommand', None, None),
         ('failedExtraArgs', [], None),
         ('focusInCommand', None, None),
         ('focusInExtraArgs', [], None),
         ('focusOutCommand', None, None),
         ('focusOutExtraArgs', [], None),
         ('rolloverSound', DGG.getDefaultRolloverSound(), self.setRolloverSound),
         ('clickSound', DGG.getDefaultClickSound(), self.setClickSound),
         ('autoCapitalize', 0, self.autoCapitalizeFunc),
         ('autoCapitalizeAllowPrefixes', DirectEntry.AllowCapNamePrefixes, None),
         ('autoCapitalizeForcePrefixes', DirectEntry.ForceCapNamePrefixes, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        if self['entryFont'] == None:
            font = DGG.getDefaultFont()
        else:
            font = self['entryFont']
        self.onscreenText = self.createcomponent('text', (), None, OnscreenText, (), parent=hidden, text='', align=TextNode.ALeft, font=font, scale=1, mayChange=1)
        self.onscreenText.removeNode()
        self.bind(DGG.ACCEPT, self.commandFunc)
        self.bind(DGG.ACCEPTFAILED, self.failedCommandFunc)
        self.accept(self.guiItem.getFocusInEvent(), self.focusInCommandFunc)
        self.accept(self.guiItem.getFocusOutEvent(), self.focusOutCommandFunc)
        self._autoCapListener = DirectObject()
        self.initialiseoptions(DirectEntry)
        if not hasattr(self, 'autoCapitalizeAllowPrefixes'):
            self.autoCapitalizeAllowPrefixes = DirectEntry.AllowCapNamePrefixes
        if not hasattr(self, 'autoCapitalizeForcePrefixes'):
            self.autoCapitalizeForcePrefixes = DirectEntry.ForceCapNamePrefixes
        for i in range(self['numStates']):
            self.guiItem.setTextDef(i, self.onscreenText.textNode)

        self.setup()
        self.unicodeText = 0
        if self['initialText']:
            self.enterText(self['initialText'])
        return None

    def destroy(self):
        self.ignoreAll()
        self._autoCapListener.ignoreAll()
        DirectFrame.destroy(self)

    def setup(self):
        self.guiItem.setupMinimal(self['width'], self['numLines'])

    def setFocus(self):
        PGEntry.setFocus(self.guiItem, self['focus'])

    def setCursorKeysActive(self):
        PGEntry.setCursorKeysActive(self.guiItem, self['cursorKeys'])

    def setObscureMode(self):
        PGEntry.setObscureMode(self.guiItem, self['obscured'])

    def setBackgroundFocus(self):
        PGEntry.setBackgroundFocus(self.guiItem, self['backgroundFocus'])

    def setRolloverSound(self):
        rolloverSound = self['rolloverSound']
        if rolloverSound:
            self.guiItem.setSound(DGG.ENTER + self.guiId, rolloverSound)
        else:
            self.guiItem.clearSound(DGG.ENTER + self.guiId)

    def setClickSound(self):
        clickSound = self['clickSound']
        if clickSound:
            self.guiItem.setSound(DGG.ACCEPT + self.guiId, clickSound)
        else:
            self.guiItem.clearSound(DGG.ACCEPT + self.guiId)

    def commandFunc(self, event):
        if self['command']:
            apply(self['command'], [self.get()] + self['extraArgs'])

    def failedCommandFunc(self, event):
        if self['failedCommand']:
            apply(self['failedCommand'], [self.get()] + self['failedExtraArgs'])

    def autoCapitalizeFunc(self):
        if self['autoCapitalize']:
            self._autoCapListener.accept(self.guiItem.getTypeEvent(), self._handleTyping)
            self._autoCapListener.accept(self.guiItem.getEraseEvent(), self._handleErasing)
        else:
            self._autoCapListener.ignore(self.guiItem.getTypeEvent())
            self._autoCapListener.ignore(self.guiItem.getEraseEvent())

    def focusInCommandFunc(self):
        if self['focusInCommand']:
            apply(self['focusInCommand'], self['focusInExtraArgs'])
        if self['autoCapitalize']:
            self.accept(self.guiItem.getTypeEvent(), self._handleTyping)
            self.accept(self.guiItem.getEraseEvent(), self._handleErasing)

    def _handleTyping(self, guiEvent):
        self._autoCapitalize()

    def _handleErasing(self, guiEvent):
        self._autoCapitalize()

    def _autoCapitalize(self):
        name = self.get().decode('utf-8')
        capName = ''
        wordSoFar = ''
        wasNonWordChar = True
        for i in xrange(len(name)):
            character = name[i]
            if string.lower(character) == string.upper(character) and character != "'":
                wordSoFar = ''
                wasNonWordChar = True
            else:
                capitalize = False
                if wasNonWordChar:
                    capitalize = True
                elif character == string.upper(character) and len(self.autoCapitalizeAllowPrefixes) and wordSoFar in self.autoCapitalizeAllowPrefixes:
                    capitalize = True
                elif len(self.autoCapitalizeForcePrefixes) and wordSoFar in self.autoCapitalizeForcePrefixes:
                    capitalize = True
                if capitalize:
                    character = string.upper(character)
                else:
                    character = string.lower(character)
                wordSoFar += character
                wasNonWordChar = False
            capName += character

        self.enterText(capName.encode('utf-8'))

    def focusOutCommandFunc(self):
        if self['focusOutCommand']:
            apply(self['focusOutCommand'], self['focusOutExtraArgs'])
        if self['autoCapitalize']:
            self.ignore(self.guiItem.getTypeEvent())
            self.ignore(self.guiItem.getEraseEvent())

    def set(self, text):
        self.unicodeText = isinstance(text, types.UnicodeType)
        if self.unicodeText:
            self.guiItem.setWtext(text)
        else:
            self.guiItem.setText(text)

    def get(self, plain = False):
        if not self.unicodeText:
            wantWide = self.guiItem.isWtext()
            if not self.directWtext.getValue():
                wantWide = False
            if plain:
                return wantWide and self.guiItem.getPlainWtext()
            else:
                return self.guiItem.getPlainText()
        elif wantWide:
            return self.guiItem.getWtext()
        else:
            return self.guiItem.getText()

    def setCursorPosition(self, pos):
        if pos < 0:
            self.guiItem.setCursorPosition(self.guiItem.getNumCharacters() + pos)
        else:
            self.guiItem.setCursorPosition(pos)

    def enterText(self, text):
        self.set(text)
        self.setCursorPosition(self.guiItem.getNumCharacters())

    def getFont(self):
        return self.onscreenText.getFont()

    def getBounds(self, state = 0):
        tn = self.onscreenText.textNode
        mat = tn.getTransform()
        align = tn.getAlign()
        lineHeight = tn.getLineHeight()
        numLines = self['numLines']
        width = self['width']
        if align == TextNode.ALeft:
            left = 0.0
            right = width
        elif align == TextNode.ACenter:
            left = -width / 2.0
            right = width / 2.0
        elif align == TextNode.ARight:
            left = -width
            right = 0.0
        bottom = -0.3 * lineHeight - lineHeight * (numLines - 1)
        top = lineHeight
        self.ll.set(left, 0.0, bottom)
        self.ur.set(right, 0.0, top)
        self.ll = mat.xformPoint(self.ll)
        self.ur = mat.xformPoint(self.ur)
        pad = self['pad']
        borderWidth = self['borderWidth']
        self.bounds = [self.ll[0] - pad[0] - borderWidth[0],
         self.ur[0] + pad[0] + borderWidth[0],
         self.ll[2] - pad[1] - borderWidth[1],
         self.ur[2] + pad[1] + borderWidth[1]]
        return self.bounds
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectEntry.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:14 Pacific Daylight Time
