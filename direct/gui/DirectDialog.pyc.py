# 2013.08.22 22:14:13 Pacific Daylight Time
# Embedded file name: direct.gui.DirectDialog
__all__ = ['findDialog',
 'cleanupDialog',
 'DirectDialog',
 'OkDialog',
 'OkCancelDialog',
 'YesNoDialog',
 'YesNoCancelDialog',
 'RetryCancelDialog']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *
from DirectButton import *
import types

def findDialog(uniqueName):
    if DirectDialog.AllDialogs.has_key(uniqueName):
        return DirectDialog.AllDialogs[uniqueName]
    return None


def cleanupDialog(uniqueName):
    if DirectDialog.AllDialogs.has_key(uniqueName):
        DirectDialog.AllDialogs[uniqueName].cleanup()


class DirectDialog(DirectFrame):
    __module__ = __name__
    AllDialogs = {}
    PanelIndex = 0

    def __init__(self, parent = None, **kw):
        optiondefs = (('dialogName', 'DirectDialog_' + repr(DirectDialog.PanelIndex), DGG.INITOPT),
         ('pos', (0, 0.1, 0), None),
         ('pad', (0.1, 0.1), None),
         ('text', '', None),
         ('text_align', TextNode.ALeft, None),
         ('text_scale', 0.06, None),
         ('image', DGG.getDefaultDialogGeom(), None),
         ('relief', None, None),
         ('buttonTextList', [], DGG.INITOPT),
         ('buttonGeomList', [], DGG.INITOPT),
         ('buttonImageList', [], DGG.INITOPT),
         ('buttonValueList', [], DGG.INITOPT),
         ('buttonHotKeyList', [], DGG.INITOPT),
         ('button_borderWidth', (0.01, 0.01), None),
         ('button_pad', (0.01, 0.01), None),
         ('button_relief', DGG.RAISED, None),
         ('button_text_scale', 0.06, None),
         ('buttonSize', None, DGG.INITOPT),
         ('topPad', 0.06, DGG.INITOPT),
         ('midPad', 0.12, DGG.INITOPT),
         ('sidePad', 0.0, DGG.INITOPT),
         ('buttonPadSF', 1.1, DGG.INITOPT),
         ('fadeScreen', 0, None),
         ('command', None, None),
         ('extraArgs', [], None),
         ('sortOrder', NO_FADE_SORT_INDEX, None))
        self.defineoptions(kw, optiondefs, dynamicGroups=('button',))
        DirectFrame.__init__(self, parent)
        cleanupDialog(self['dialogName'])
        DirectDialog.AllDialogs[self['dialogName']] = self
        DirectDialog.PanelIndex += 1
        self.numButtons = max(len(self['buttonTextList']), len(self['buttonGeomList']), len(self['buttonImageList']), len(self['buttonValueList']))
        self.buttonList = []
        index = 0
        for i in range(self.numButtons):
            name = 'Button' + repr(i)
            try:
                text = self['buttonTextList'][i]
            except IndexError:
                text = None

            try:
                geom = self['buttonGeomList'][i]
            except IndexError:
                geom = None

            try:
                image = self['buttonImageList'][i]
            except IndexError:
                image = None

            try:
                value = self['buttonValueList'][i]
            except IndexError:
                value = i
                self['buttonValueList'].append(i)

            try:
                hotKey = self['buttonHotKeyList'][i]
            except IndexError:
                hotKey = None

            button = self.createcomponent(name, (), 'button', DirectButton, (self,), text=text, geom=geom, image=image, suppressKeys=self['suppressKeys'], frameSize=self['buttonSize'], command=lambda s = self, v = value: s.buttonCommand(v))
            self.buttonList.append(button)

        self.postInitialiseFuncList.append(self.configureDialog)
        self.initialiseoptions(DirectDialog)
        return None

    def configureDialog(self):
        bindList = zip(self.buttonList, self['buttonHotKeyList'], self['buttonValueList'])
        for button, hotKey, value in bindList:
            if type(hotKey) == types.ListType or type(hotKey) == types.TupleType:
                for key in hotKey:
                    button.bind('press-' + key + '-', self.buttonCommand, extraArgs=[value])
                    self.bind('press-' + key + '-', self.buttonCommand, extraArgs=[value])

            else:
                button.bind('press-' + hotKey + '-', self.buttonCommand, extraArgs=[value])
                self.bind('press-' + hotKey + '-', self.buttonCommand, extraArgs=[value])

        pad = self['pad']
        if self.hascomponent('image0'):
            image = self.component('image0')
        else:
            image = None
        if image:
            image.reparentTo(hidden)
        bounds = self.stateNodePath[0].getTightBounds()
        if image:
            image.reparentTo(self.stateNodePath[0])
        l = bounds[0][0]
        r = bounds[1][0]
        b = bounds[0][2]
        t = bounds[1][2]
        xOffset = -(l + r) * 0.5
        zOffset = -(b + t) * 0.5
        l += xOffset
        r += xOffset
        b += zOffset
        t += zOffset
        if self['text']:
            self['text_pos'] = (self['text_pos'][0] + xOffset, self['text_pos'][1] + zOffset)
        if self['geom']:
            self['geom_pos'] = Point3(self['geom_pos'][0] + xOffset, self['geom_pos'][1], self['geom_pos'][2] + zOffset)
        if self.numButtons != 0:
            bpad = self['button_pad']
            if self['buttonSize']:
                buttonSize = self['buttonSize']
                bl = buttonSize[0]
                br = buttonSize[1]
                bb = buttonSize[2]
                bt = buttonSize[3]
            else:
                bl = br = bb = bt = 0
                for button in self.buttonList:
                    bounds = button.stateNodePath[0].getTightBounds()
                    bl = min(bl, bounds[0][0])
                    br = max(br, bounds[1][0])
                    bb = min(bb, bounds[0][2])
                    bt = max(bt, bounds[1][2])

                bl -= bpad[0]
                br += bpad[0]
                bb -= bpad[1]
                bt += bpad[1]
                for button in self.buttonList:
                    button['frameSize'] = (bl,
                     br,
                     bb,
                     bt)

            scale = self['button_scale']
            if isinstance(scale, Vec3) or type(scale) == types.ListType or type(scale) == types.TupleType:
                sx = scale[0]
                sz = scale[2]
            elif type(scale) == types.IntType or type(scale) == types.FloatType:
                sx = sz = scale
            else:
                sx = sz = 1
            bl *= sx
            br *= sx
            bb *= sz
            bt *= sz
            bHeight = bt - bb
            bWidth = br - bl
            bSpacing = self['buttonPadSF'] * bWidth
            bPos = -bSpacing * (self.numButtons - 1) * 0.5
            index = 0
            for button in self.buttonList:
                button.setPos(bPos + index * bSpacing, 0, b - self['midPad'] - bpad[1] - bt)
                index += 1

            bMax = bPos + bSpacing * (self.numButtons - 1)
        else:
            bpad = 0
            bl = br = bb = bt = 0
            bPos = 0
            bMax = 0
            bpad = (0, 0)
            bHeight = bWidth = 0
        l = min(bPos + bl, l) - pad[0]
        r = max(bMax + br, r) + pad[0]
        sidePad = self['sidePad']
        l -= sidePad
        r += sidePad
        b = min(b - self['midPad'] - bpad[1] - bHeight - bpad[1], b) - pad[1]
        t = t + self['topPad'] + pad[1]
        self['image_scale'] = (r - l, 1, t - b)
        self['image_pos'] = ((l + r) * 0.5, 0.0, (b + t) * 0.5)
        self.resetFrameSize()
        return

    def show(self):
        if self['fadeScreen']:
            base.transitions.fadeScreen(self['fadeScreen'])
            self.setBin('gui-popup', 0)
        NodePath.show(self)

    def hide(self):
        if self['fadeScreen']:
            base.transitions.noTransitions()
        NodePath.hide(self)

    def buttonCommand(self, value, event = None):
        if self['command']:
            self['command'](value, *self['extraArgs'])

    def setMessage(self, message):
        self['text'] = message
        self.configureDialog()

    def cleanup(self):
        uniqueName = self['dialogName']
        if DirectDialog.AllDialogs.has_key(uniqueName):
            del DirectDialog.AllDialogs[uniqueName]
        self.destroy()

    def destroy(self):
        if self['fadeScreen']:
            base.transitions.noTransitions()
        for button in self.buttonList:
            button.destroy()

        DirectFrame.destroy(self)


class OkDialog(DirectDialog):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('buttonTextList', ['OK'], DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_OK], DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(OkDialog)


class OkCancelDialog(DirectDialog):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('buttonTextList', ['OK', 'Cancel'], DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_OK, DGG.DIALOG_CANCEL], DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(OkCancelDialog)


class YesNoDialog(DirectDialog):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('buttonTextList', ['Yes', 'No'], DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_YES, DGG.DIALOG_NO], DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(YesNoDialog)


class YesNoCancelDialog(DirectDialog):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('buttonTextList', ['Yes', 'No', 'Cancel'], DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_YES, DGG.DIALOG_NO, DGG.DIALOG_CANCEL], DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(YesNoCancelDialog)


class RetryCancelDialog(DirectDialog):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        optiondefs = (('buttonTextList', ['Retry', 'Cancel'], DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_RETRY, DGG.DIALOG_CANCEL], DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(RetryCancelDialog)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectDialog.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:13 Pacific Daylight Time
