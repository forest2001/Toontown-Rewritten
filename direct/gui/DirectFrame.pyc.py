# 2013.08.22 22:14:14 Pacific Daylight Time
# Embedded file name: direct.gui.DirectFrame
__all__ = ['DirectFrame']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectGuiBase import *
from OnscreenImage import OnscreenImage
from OnscreenGeom import OnscreenGeom
import string, types

class DirectFrame(DirectGuiWidget):
    __module__ = __name__
    DefDynGroups = ('text', 'geom', 'image')

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGItem, None),
         ('numStates', 1, None),
         ('state', self.inactiveInitState, None),
         ('image', None, self.setImage),
         ('geom', None, self.setGeom),
         ('text', None, self.setText),
         ('textMayChange', 1, None))
        self.defineoptions(kw, optiondefs, dynamicGroups=DirectFrame.DefDynGroups)
        DirectGuiWidget.__init__(self, parent)
        self.initialiseoptions(DirectFrame)
        return

    def destroy(self):
        DirectGuiWidget.destroy(self)

    def setText(self):
        if self['text'] == None:
            textList = (None,) * self['numStates']
        elif isinstance(self['text'], types.StringTypes):
            textList = (self['text'],) * self['numStates']
        else:
            textList = self['text']
        for i in range(self['numStates']):
            component = 'text' + repr(i)
            try:
                text = textList[i]
            except IndexError:
                text = textList[-1]

            if self.hascomponent(component):
                if text == None:
                    self.destroycomponent(component)
                else:
                    self[component + '_text'] = text
            elif text == None:
                return
            else:
                from OnscreenText import OnscreenText
                self.createcomponent(component, (), 'text', OnscreenText, (), parent=self.stateNodePath[i], text=text, scale=1, mayChange=self['textMayChange'], sort=DGG.TEXT_SORT_INDEX)

        return

    def setGeom(self):
        geom = self['geom']
        if geom == None:
            geomList = (None,) * self['numStates']
        elif isinstance(geom, NodePath) or isinstance(geom, types.StringTypes):
            geomList = (geom,) * self['numStates']
        else:
            geomList = geom
        for i in range(self['numStates']):
            component = 'geom' + repr(i)
            try:
                geom = geomList[i]
            except IndexError:
                geom = geomList[-1]

            if self.hascomponent(component):
                if geom == None:
                    self.destroycomponent(component)
                else:
                    self[component + '_geom'] = geom
            elif geom == None:
                return
            else:
                self.createcomponent(component, (), 'geom', OnscreenGeom, (), parent=self.stateNodePath[i], geom=geom, scale=1, sort=DGG.GEOM_SORT_INDEX)

        return

    def setImage(self):
        arg = self['image']
        if arg == None:
            imageList = (None,) * self['numStates']
        elif isinstance(arg, NodePath) or isinstance(arg, Texture) or isinstance(arg, types.StringTypes):
            imageList = (arg,) * self['numStates']
        elif len(arg) == 2 and isinstance(arg[0], types.StringTypes) and isinstance(arg[1], types.StringTypes):
            imageList = (arg,) * self['numStates']
        else:
            imageList = arg
        for i in range(self['numStates']):
            component = 'image' + repr(i)
            try:
                image = imageList[i]
            except IndexError:
                image = imageList[-1]

            if self.hascomponent(component):
                if image == None:
                    self.destroycomponent(component)
                else:
                    self[component + '_image'] = image
            elif image == None:
                return
            else:
                self.createcomponent(component, (), 'image', OnscreenImage, (), parent=self.stateNodePath[i], image=image, scale=1, sort=DGG.IMAGE_SORT_INDEX)

        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectFrame.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:14 Pacific Daylight Time
