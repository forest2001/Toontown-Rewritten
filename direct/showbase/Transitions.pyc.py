# 2013.08.22 22:14:49 Pacific Daylight Time
# Embedded file name: direct.showbase.Transitions
__all__ = ['Transitions']
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
from direct.interval.LerpInterval import LerpColorScaleInterval, LerpColorInterval, LerpScaleInterval, LerpPosInterval
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.FunctionInterval import Func

class Transitions():
    __module__ = __name__
    IrisModelName = 'models/misc/iris'
    FadeModelName = 'models/misc/fade'

    def __init__(self, loader, model = None, scale = 3.0, pos = Vec3(0, 0, 0)):
        self.transitionIval = None
        self.letterboxIval = None
        self.iris = None
        self.fade = None
        self.letterbox = None
        self.fadeModel = model
        self.imagePos = pos
        if model:
            self.alphaOff = Vec4(1, 1, 1, 0)
            self.alphaOn = Vec4(1, 1, 1, 1)
            model.setTransparency(1)
            self.lerpFunc = LerpColorScaleInterval
        else:
            self.alphaOff = Vec4(0, 0, 0, 0)
            self.alphaOn = Vec4(0, 0, 0, 1)
            self.lerpFunc = LerpColorInterval
        self.irisTaskName = 'irisTask'
        self.fadeTaskName = 'fadeTask'
        self.letterboxTaskName = 'letterboxTask'
        return

    def __del__(self):
        if self.fadeModel:
            self.fadeModel.removeNode()
            self.fadeModel = None
        return

    def setFadeModel(self, model, scale = 1.0):
        self.fadeModel = model
        self.alphaOn = Vec4(1, 1, 1, 1)
        if self.fade:
            del self.fade
            self.fade = None
            self.loadFade()
        return

    def loadFade(self):
        if not self.fadeModel:
            self.fadeModel = loader.loadModel(self.FadeModelName)
        if self.fade == None:
            self.fade = DirectFrame(parent=hidden, guiId='fade', relief=None, image=self.fadeModel, image_scale=(4, 2, 2), state=DGG.NORMAL)
            self.fade.setBin('unsorted', 0)
            self.fade.setColor(0, 0, 0, 0)
        return

    def getFadeInIval(self, t = 0.5, finishIval = None):
        self.loadFade()
        transitionIval = Sequence(Func(self.fade.reparentTo, aspect2d, FADE_SORT_INDEX), Func(self.fade.showThrough), self.lerpFunc(self.fade, t, self.alphaOff), Func(self.fade.detachNode), name=self.fadeTaskName)
        if finishIval:
            transitionIval.append(finishIval)
        return transitionIval

    def getFadeOutIval(self, t = 0.5, finishIval = None):
        self.noTransitions()
        self.loadFade()
        transitionIval = Sequence(Func(self.fade.reparentTo, aspect2d, FADE_SORT_INDEX), Func(self.fade.showThrough), self.lerpFunc(self.fade, t, self.alphaOn), name=self.fadeTaskName)
        if finishIval:
            transitionIval.append(finishIval)
        return transitionIval

    def fadeIn(self, t = 0.5, finishIval = None):
        gsg = base.win.getGsg()
        if gsg:
            base.graphicsEngine.renderFrame()
            render.prepareScene(gsg)
            render2d.prepareScene(gsg)
        if t == 0:
            self.noTransitions()
            self.loadFade()
            self.fade.detachNode()
        else:
            self.transitionIval = self.getFadeInIval(t, finishIval)
            self.transitionIval.start()

    def fadeOut(self, t = 0.5, finishIval = None):
        if t == 0:
            self.noTransitions()
            self.loadFade()
            self.fade.reparentTo(aspect2d, FADE_SORT_INDEX)
            self.fade.setColor(self.alphaOn)
        elif base.config.GetBool('no-loading-screen', 0):
            if finishIval:
                self.transitionIval = finishIval
                self.transitionIval.start()
        else:
            self.transitionIval = self.getFadeOutIval(t, finishIval)
            self.transitionIval.start()

    def fadeOutActive(self):
        return self.fade and self.fade.getColor()[3] > 0

    def fadeScreen(self, alpha = 0.5):
        self.noTransitions()
        self.loadFade()
        self.fade.reparentTo(aspect2d, FADE_SORT_INDEX)
        self.fade.setColor(self.alphaOn[0], self.alphaOn[1], self.alphaOn[2], alpha)

    def fadeScreenColor(self, color):
        self.noTransitions()
        self.loadFade()
        self.fade.reparentTo(aspect2d, FADE_SORT_INDEX)
        self.fade.setColor(color)

    def noFade(self):
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None
        if self.fade:
            self.fade.setColor(self.alphaOff)
            self.fade.detachNode()
        return

    def setFadeColor(self, r, g, b):
        self.alphaOn.set(r, g, b, 1)
        self.alphaOff.set(r, g, b, 0)

    def loadIris(self):
        if self.iris == None:
            self.iris = loader.loadModel(self.IrisModelName)
            self.iris.setPos(0, 0, 0)
        return

    def irisIn(self, t = 0.5, finishIval = None):
        self.noTransitions()
        self.loadIris()
        if t == 0:
            self.iris.detachNode()
        else:
            self.iris.reparentTo(aspect2d, FADE_SORT_INDEX)
            self.transitionIval = Sequence(LerpScaleInterval(self.iris, t, scale=0.18, startScale=0.01), Func(self.iris.detachNode), name=self.irisTaskName)
            if finishIval:
                self.transitionIval.append(finishIval)
            self.transitionIval.start()

    def irisOut(self, t = 0.5, finishIval = None):
        self.noTransitions()
        self.loadIris()
        self.loadFade()
        if t == 0:
            self.iris.detachNode()
            self.fadeOut(0)
        else:
            self.iris.reparentTo(aspect2d, FADE_SORT_INDEX)
            self.transitionIval = Sequence(LerpScaleInterval(self.iris, t, scale=0.01, startScale=0.18), Func(self.iris.detachNode), Func(self.fadeOut, 0), name=self.irisTaskName)
            if finishIval:
                self.transitionIval.append(finishIval)
            self.transitionIval.start()

    def noIris(self):
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None
        if self.iris != None:
            self.iris.detachNode()
        self.noFade()
        return

    def noTransitions(self):
        self.noFade()
        self.noIris()

    def loadLetterbox(self):
        if not self.letterbox:
            self.letterbox = NodePath('letterbox')
            self.letterbox.setTransparency(1)
            self.letterbox.setBin('unsorted', 0)
            button = loader.loadModel('models/gui/toplevel_gui', okMissing=True)
            barImage = None
            if button:
                barImage = button.find('**/generic_button')
            self.letterboxTop = DirectFrame(parent=self.letterbox, guiId='letterboxTop', relief=DGG.FLAT, state=DGG.NORMAL, frameColor=(0, 0, 0, 1), borderWidth=(0, 0), frameSize=(-1, 1, 0, 0.2), pos=(0, 0, 0.8), image=barImage, image_scale=(2.25, 1, 0.5), image_pos=(0, 0, 0.1), image_color=(0.3, 0.3, 0.3, 1), sortOrder=0)
            self.letterboxBottom = DirectFrame(parent=self.letterbox, guiId='letterboxBottom', relief=DGG.FLAT, state=DGG.NORMAL, frameColor=(0, 0, 0, 1), borderWidth=(0, 0), frameSize=(-1, 1, 0, 0.2), pos=(0, 0, -1), image=barImage, image_scale=(2.25, 1, 0.5), image_pos=(0, 0, 0.1), image_color=(0.3, 0.3, 0.3, 1), sortOrder=0)
            self.letterboxTop.setBin('sorted', 0)
            self.letterboxBottom.setBin('sorted', 0)
            self.letterbox.reparentTo(render2d, -1)
            self.letterboxOff(0)
        return

    def noLetterbox(self):
        if self.letterboxIval:
            self.letterboxIval.pause()
            self.letterboxIval = None
        if self.letterbox:
            self.letterbox.stash()
        return

    def letterboxOn(self, t = 0.25, finishIval = None):
        self.noLetterbox()
        self.loadLetterbox()
        self.letterbox.unstash()
        if t == 0:
            self.letterboxBottom.setPos(0, 0, -1)
            self.letterboxTop.setPos(0, 0, 0.8)
        else:
            self.letterboxIval = Sequence(Parallel(LerpPosInterval(self.letterboxBottom, t, pos=Vec3(0, 0, -1)), LerpPosInterval(self.letterboxTop, t, pos=Vec3(0, 0, 0.8))), name=self.letterboxTaskName)
            if finishIval:
                self.letterboxIval.append(finishIval)
            self.letterboxIval.start()

    def letterboxOff(self, t = 0.25, finishIval = None):
        self.noLetterbox()
        self.loadLetterbox()
        self.letterbox.unstash()
        if t == 0:
            self.letterbox.stash()
        else:
            self.letterboxIval = Sequence(Parallel(LerpPosInterval(self.letterboxBottom, t, pos=Vec3(0, 0, -1.2)), LerpPosInterval(self.letterboxTop, t, pos=Vec3(0, 0, 1))), Func(self.letterbox.stash), Func(messenger.send, 'letterboxOff'), name=self.letterboxTaskName)
            if finishIval:
                self.letterboxIval.append(finishIval)
            self.letterboxIval.start()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\Transitions.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:50 Pacific Daylight Time
