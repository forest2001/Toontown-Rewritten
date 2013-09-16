# 2013.08.22 22:14:17 Pacific Daylight Time
# Embedded file name: direct.gui.DirectRadioButton
__all__ = ['DirectRadioButton']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectButton import *
from DirectLabel import *

class DirectRadioButton(DirectButton):
    __module__ = __name__

    def __init__(self, parent = None, **kw):
        self.colors = None
        optiondefs = (('indicatorValue', 0, self.setIndicatorValue),
         ('variable', [], None),
         ('value', [], None),
         ('others', [], None),
         ('boxBorder', 0, None),
         ('boxPlacement', 'left', None),
         ('boxGeom', None, None),
         ('boxGeomColor', None, None),
         ('boxGeomScale', 1.0, None),
         ('boxImage', loader.loadModel('models/gui/radio_button_gui'), None),
         ('boxImageScale', 1.0, None),
         ('boxImageColor', VBase4(1, 1, 1, 1), None),
         ('boxRelief', None, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.indicator = self.createcomponent('indicator', (), None, DirectLabel, (self,), numStates=2, image=self['boxImage'], image_scale=self['boxImageScale'], image_color=self['boxImageColor'], geom=self['boxGeom'], geom_scale=self['boxGeomScale'], geom_color=self['boxGeomColor'], state='disabled', text=('X', 'X'), relief=self['boxRelief'])
        self.initialiseoptions(DirectRadioButton)
        if self['boxGeom'] == None:
            self.indicator['text'] = (' ', '*')
            self.indicator['text_pos'] = (0, -0.5)
        else:
            self.indicator['text'] = (' ', ' ')
        if self['boxGeomColor'] != None and self['boxGeom'] != None:
            self.colors = [VBase4(1, 1, 1, 0), self['boxGeomColor']]
            self.component('indicator')['geom_color'] = VBase4(1, 1, 1, 0)
        needToCheck = True
        if len(self['value']) == len(self['variable']) != 0:
            for i in range(len(self['value'])):
                if self['variable'][i] != self['value'][i]:
                    needToCheck = False
                    break

        if needToCheck:
            self.check()
        return

    def resetFrameSize(self):
        self.setFrameSize(fClearFrame=1)

    def setFrameSize(self, fClearFrame = 0):
        if self['frameSize']:
            self.bounds = self['frameSize']
            frameType = self.frameStyle[0].getType()
            ibw = self.indicator['borderWidth']
        else:
            frameType = self.frameStyle[0].getType()
            if fClearFrame and frameType != PGFrameStyle.TNone:
                self.frameStyle[0].setType(PGFrameStyle.TNone)
                self.guiItem.setFrameStyle(0, self.frameStyle[0])
                self.guiItem.getStateDef(0)
            self.getBounds()
            if frameType != PGFrameStyle.TNone:
                self.frameStyle[0].setType(frameType)
                self.guiItem.setFrameStyle(0, self.frameStyle[0])
            ibw = self.indicator['borderWidth']
            indicatorWidth = self.indicator.getWidth() + 2 * ibw[0]
            indicatorHeight = self.indicator.getHeight() + 2 * ibw[1]
            diff = indicatorHeight + 2 * self['boxBorder'] - (self.bounds[3] - self.bounds[2])
            if diff > 0:
                if self['boxPlacement'] == 'left':
                    self.bounds[0] += -(indicatorWidth + 2 * self['boxBorder'])
                    self.bounds[3] += diff / 2
                    self.bounds[2] -= diff / 2
                elif self['boxPlacement'] == 'below':
                    self.bounds[2] += -(indicatorHeight + 2 * self['boxBorder'])
                elif self['boxPlacement'] == 'right':
                    self.bounds[1] += indicatorWidth + 2 * self['boxBorder']
                    self.bounds[3] += diff / 2
                    self.bounds[2] -= diff / 2
                else:
                    self.bounds[3] += indicatorHeight + 2 * self['boxBorder']
            elif self['boxPlacement'] == 'left':
                self.bounds[0] += -(indicatorWidth + 2 * self['boxBorder'])
            elif self['boxPlacement'] == 'below':
                self.bounds[2] += -(indicatorHeight + 2 * self['boxBorder'])
            elif self['boxPlacement'] == 'right':
                self.bounds[1] += indicatorWidth + 2 * self['boxBorder']
            else:
                self.bounds[3] += indicatorHeight + 2 * self['boxBorder']
        if frameType != PGFrameStyle.TNone and frameType != PGFrameStyle.TFlat:
            bw = self['borderWidth']
        else:
            bw = (0, 0)
        self.guiItem.setFrame(self.bounds[0] - bw[0], self.bounds[1] + bw[0], self.bounds[2] - bw[1], self.bounds[3] + bw[1])
        if not self.indicator['pos']:
            bbounds = self.bounds
            lbounds = self.indicator.bounds
            newpos = [0, 0, 0]
            if self['boxPlacement'] == 'left':
                newpos[0] += bbounds[0] - lbounds[0] + self['boxBorder'] + ibw[0]
                dropValue = (bbounds[3] - bbounds[2] - lbounds[3] + lbounds[2]) / 2 + self['boxBorder']
                newpos[2] += bbounds[3] - lbounds[3] + self['boxBorder'] - dropValue
            elif self['boxPlacement'] == 'right':
                newpos[0] += bbounds[1] - lbounds[1] - self['boxBorder'] - ibw[0]
                dropValue = (bbounds[3] - bbounds[2] - lbounds[3] + lbounds[2]) / 2 + self['boxBorder']
                newpos[2] += bbounds[3] - lbounds[3] + self['boxBorder'] - dropValue
            elif self['boxPlacement'] == 'above':
                newpos[2] += bbounds[3] - lbounds[3] - self['boxBorder'] - ibw[1]
            else:
                newpos[2] += bbounds[2] - lbounds[2] + self['boxBorder'] + ibw[1]
            self.indicator.setPos(newpos[0], newpos[1], newpos[2])

    def commandFunc(self, event):
        if len(self['value']) == len(self['variable']) != 0:
            for i in range(len(self['value'])):
                self['variable'][i] = self['value'][i]

        self.check()

    def check(self):
        self['indicatorValue'] = 1
        self.setIndicatorValue()
        for other in self['others']:
            if other != self:
                other.uncheck()

        if self['command']:
            apply(self['command'], self['extraArgs'])

    def setOthers(self, others):
        self['others'] = others

    def uncheck(self):
        self['indicatorValue'] = 0
        if self.colors != None:
            self.component('indicator')['geom_color'] = self.colors[self['indicatorValue']]
        return

    def setIndicatorValue(self):
        self.component('indicator').guiItem.setState(self['indicatorValue'])
        if self.colors != None:
            self.component('indicator')['geom_color'] = self.colors[self['indicatorValue']]
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectRadioButton.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:17 Pacific Daylight Time
