# 2013.08.22 22:14:46 Pacific Daylight Time
# Embedded file name: direct.showbase.ShowBase
__all__ = ['ShowBase', 'WindowControls']
from pandac.PandaModules import *
import __builtin__
__builtin__.config = getConfigShowbase()
from direct.directnotify.DirectNotifyGlobal import *
from MessengerGlobal import *
from BulletinBoardGlobal import *
from direct.task.TaskManagerGlobal import *
from JobManagerGlobal import *
from EventManagerGlobal import *
from PythonUtil import *
from direct.showbase import PythonUtil
from direct.interval import IntervalManager
from InputStateGlobal import inputState
from direct.showbase.BufferViewer import BufferViewer
from direct.task import Task
from direct.directutil import Verify
from direct.showbase import GarbageReport
import EventManager
import math, sys, os
import Loader
import time
import gc
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase import ExceptionVarDump
import DirectObject
import SfxPlayer
import OnScreenDebug
import AppRunnerGlobal
__builtin__.FADE_SORT_INDEX = 1000
__builtin__.NO_FADE_SORT_INDEX = 2000

class ShowBase(DirectObject.DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('ShowBase')

    def __init__(self, fStartDirect = True, windowType = None):
        __builtin__.__dev__ = config.GetBool('want-dev', 0)
        if not config.GetBool('log-stack-dump', 0):
            logStackDump = config.GetBool('client-log-stack-dump', 0)
            uploadStackDump = config.GetBool('upload-stack-dump', 0)
            if logStackDump or uploadStackDump:
                ExceptionVarDump.install(logStackDump, uploadStackDump)
            self.mainDir = ExecutionEnvironment.getEnvironmentVariable('MAIN_DIR')
            self.appRunner = AppRunnerGlobal.appRunner
            self.debugRunningMultiplier = 4
            self.config = config
            Verify.wantVerifyPdb = self.config.GetBool('want-verify-pdb', 0)
            if self.config.GetBool('disable-sticky-keys', 0):
                storeAccessibilityShortcutKeys()
                allowAccessibilityShortcutKeys(False)
            self.printEnvDebugInfo()
            vfs = VirtualFileSystem.getGlobalPtr()
            self.nextWindowIndex = 1
            self.__directStarted = False
            self.__deadInputs = 0
            self.sfxActive = self.config.GetBool('audio-sfx-active', 1)
            self.musicActive = self.config.GetBool('audio-music-active', 1)
            self.wantFog = self.config.GetBool('want-fog', 1)
            self.wantRender2dp = self.config.GetBool('want-render2dp', 1)
            self.screenshotExtension = self.config.GetString('screenshot-extension', 'jpg')
            self.musicManager = None
            self.musicManagerIsValid = None
            self.sfxManagerList = []
            self.sfxManagerIsValidList = []
            self.wantStats = self.config.GetBool('want-pstats', 0)
            self.exitFunc = None
            self.finalExitCallbacks = []
            Task.TaskManager.taskTimerVerbose = self.config.GetBool('task-timer-verbose', 0)
            Task.TaskManager.extendedExceptions = self.config.GetBool('extended-exceptions', 0)
            Task.TaskManager.pStatsTasks = self.config.GetBool('pstats-tasks', 0)
            taskMgr.resumeFunc = PStatClient.resumeAfterPause
            if self.config.GetBool('want-dev', 0):
                import profile, pstats
                profile.Profile.bias = float(self.config.GetString('profile-bias', '0'))

                def f8(x):
                    return ('%' + '8.%df' % base.config.GetInt('profile-decimals', 3)) % x

                pstats.f8 = f8
            self.__configAspectRatio = ConfigVariableDouble('aspect-ratio', 0).getValue()
            self.__oldAspectRatio = None
            self.windowType = windowType
            if self.windowType is None:
                self.windowType = self.config.GetString('window-type', 'onscreen')
            self.requireWindow = self.config.GetBool('require-window', 1)
            self.win = None
            self.frameRateMeter = None
            self.winList = []
            self.winControls = []
            self.mainWinMinimized = 0
            self.mainWinForeground = 0
            self.pipe = None
            self.pipeList = []
            self.mouse2cam = None
            self.buttonThrowers = None
            self.mouseWatcher = None
            self.mouseWatcherNode = None
            self.pointerWatcherNodes = None
            self.mouseInterface = None
            self.drive = None
            self.trackball = None
            self.texmem = None
            self.showVertices = None
            self.cam = None
            self.cam2d = None
            self.cam2dp = None
            self.camera = None
            self.camera2d = None
            self.camera2dp = None
            self.camList = []
            self.camNode = None
            self.camLens = None
            self.camFrustumVis = None
            try:
                self.clusterSyncFlag = clusterSyncFlag
            except NameError:
                self.clusterSyncFlag = self.config.GetBool('cluster-sync', 0)

            self.hidden = NodePath('hidden')
            self.graphicsEngine = GraphicsEngine.getGlobalPtr()
            self.setupRender()
            self.setupRender2d()
            self.setupDataGraph()
            if self.wantRender2dp:
                self.setupRender2dp()
            self.shadowTrav = 0
            self.cTrav = 0
            self.cTravStack = Stack()
            self.appTrav = 0
            self.dgTrav = DataGraphTraverser()
            self.recorder = None
            playbackSession = self.config.GetString('playback-session', '')
            recordSession = self.config.GetString('record-session', '')
            if playbackSession:
                self.recorder = RecorderController()
                self.recorder.beginPlayback(Filename.fromOsSpecific(playbackSession))
            elif recordSession:
                self.recorder = RecorderController()
                self.recorder.beginRecord(Filename.fromOsSpecific(recordSession))
            if self.recorder:
                import random
                seed = self.recorder.getRandomSeed()
                random.seed(seed)
            self.oldexitfunc = getattr(sys, 'exitfunc', None)
            sys.exitfunc = self.exitfunc
            if self.windowType != 'none':
                props = WindowProperties.getDefault()
                if self.config.GetBool('read-raw-mice', 0):
                    props.setRawMice(1)
                self.openDefaultWindow(startDirect=False, props=props)
            self.loader = Loader.Loader(self)
            self.graphicsEngine.setDefaultLoader(self.loader.loader)
            self.eventMgr = eventMgr
            self.messenger = messenger
            self.bboard = bulletinBoard
            self.taskMgr = taskMgr
            self.jobMgr = jobMgr
            self.particleMgr = None
            self.particleMgrEnabled = 0
            self.physicsMgr = None
            self.physicsMgrEnabled = 0
            self.physicsMgrAngular = 0
            self.createBaseAudioManagers()
            self.createStats()
            self.AppHasAudioFocus = 1
            globalClock = ClockObject.getGlobalClock()
            trueClock = TrueClock.getGlobalPtr()
            globalClock.setRealTime(trueClock.getShortTime())
            globalClock.tick()
            taskMgr.globalClock = globalClock
            affinityMask = self.config.GetInt('client-cpu-affinity-mask', -1)
            if affinityMask != -1:
                TrueClock.getGlobalPtr().setCpuAffinity(affinityMask)
            else:
                autoAffinity = self.config.GetBool('auto-single-cpu-affinity', 0)
                affinity = None
                if autoAffinity and 'clientIndex' in __builtin__.__dict__:
                    affinity = abs(int(__builtin__.clientIndex))
                else:
                    affinity = self.config.GetInt('client-cpu-affinity', -1)
                if affinity in (None, -1) and autoAffinity:
                    affinity = 0
                if affinity not in (None, -1):
                    TrueClock.getGlobalPtr().setCpuAffinity(1 << affinity % 32)
            __builtin__.base = self
            __builtin__.render2d = self.render2d
            __builtin__.aspect2d = self.aspect2d
            __builtin__.pixel2d = self.pixel2d
            __builtin__.render = self.render
            __builtin__.hidden = self.hidden
            __builtin__.camera = self.camera
            __builtin__.loader = self.loader
            __builtin__.taskMgr = self.taskMgr
            __builtin__.jobMgr = self.jobMgr
            __builtin__.eventMgr = self.eventMgr
            __builtin__.messenger = self.messenger
            __builtin__.bboard = self.bboard
            __builtin__.run = self.run
            __builtin__.ostream = Notify.out()
            __builtin__.directNotify = directNotify
            __builtin__.giveNotify = giveNotify
            __builtin__.globalClock = globalClock
            __builtin__.vfs = vfs
            __builtin__.cpMgr = ConfigPageManager.getGlobalPtr()
            __builtin__.cvMgr = ConfigVariableManager.getGlobalPtr()
            __builtin__.pandaSystem = PandaSystem.getGlobalPtr()
            __builtin__.wantUberdog = base.config.GetBool('want-uberdog', 1)
            __builtin__.onScreenDebug = OnScreenDebug.OnScreenDebug()
            if self.wantRender2dp:
                __builtin__.render2dp = self.render2dp
                __builtin__.aspect2dp = self.aspect2dp
                __builtin__.pixel2dp = self.pixel2dp
            ShowBase.notify.info('__dev__ == %s' % __dev__)
            PythonUtil.recordFunctorCreationStacks()
            if __dev__ or self.config.GetBool('want-e3-hacks', False):
                if self.config.GetBool('track-gui-items', True):
                    self.guiItems = {}
            self.accept('window-event', self.windowEvent)
            import Transitions
            self.transitions = Transitions.Transitions(self.loader)
            self.setupWindowControls()
            sleepTime = self.config.GetFloat('client-sleep', 0.0)
            self.clientSleep = 0.0
            self.setSleep(sleepTime)
            if base.config.GetBool('multi-sleep', 0):
                self.multiClientSleep = 1
            else:
                self.multiClientSleep = 0
            self.bufferViewer = BufferViewer()
            if self.wantRender2dp:
                self.bufferViewer.setRenderParent(self.render2dp)
            if self.windowType != 'none':
                if fStartDirect:
                    self.__doStartDirect()
                if self.config.GetBool('show-tex-mem', False):
                    (not self.texmem or self.texmem.cleanedUp) and self.toggleTexMem()
        taskMgr.finalInit()
        self.restart()
        return

    def pushCTrav(self, cTrav):
        self.cTravStack.push(self.cTrav)
        self.cTrav = cTrav

    def popCTrav(self):
        self.cTrav = self.cTravStack.pop()

    def getExitErrorCode(self):
        return 0

    def printEnvDebugInfo(self):
        if self.config.GetBool('want-env-debug-info', 0):
            print '\n\nEnvironment Debug Info {'
            print '* model path:'
            print getModelPath()
            print '* texture path:'
            print getTexturePath()
            print '* sound path:'
            print getSoundPath()
            print '}'

    def destroy(self):
        for cb in self.finalExitCallbacks:
            cb()

        if self.config.GetBool('disable-sticky-keys', 0):
            allowAccessibilityShortcutKeys(True)
        taskMgr.destroy()
        if getattr(self, 'musicManager', None):
            self.musicManager.shutdown()
            self.musicManager = None
            for sfxManager in self.sfxManagerList:
                sfxManager.shutdown()

            self.sfxManagerList = []
        if getattr(self, 'loader', None):
            self.loader.destroy()
            self.loader = None
        if getattr(self, 'graphicsEngine', None):
            self.graphicsEngine.removeAllWindows()
        try:
            self.direct.panel.destroy()
        except:
            pass

        if hasattr(self, 'win'):
            del self.win
            del self.winList
            del self.pipe
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.unmountAll()
        return

    def exitfunc(self):
        self.destroy()
        if self.oldexitfunc:
            self.oldexitfunc()

    def makeDefaultPipe(self, printPipeTypes = True):
        selection = GraphicsPipeSelection.getGlobalPtr()
        if printPipeTypes:
            selection.printPipeTypes()
        self.pipe = selection.makeDefaultPipe()
        if not self.pipe:
            self.notify.error('No graphics pipe is available!\nYour Config.prc file must name at least one valid panda display\nlibrary via load-display or aux-display.')
        self.notify.info('Default graphics pipe is %s (%s).' % (self.pipe.getType().getName(), self.pipe.getInterfaceName()))
        self.pipeList.append(self.pipe)

    def makeModulePipe(self, moduleName):
        selection = GraphicsPipeSelection.getGlobalPtr()
        return selection.makeModulePipe(moduleName)

    def makeAllPipes(self):
        shouldPrintPipes = 0
        selection = GraphicsPipeSelection.getGlobalPtr()
        selection.loadAuxModules()
        if self.pipe == None:
            self.makeDefaultPipe()
        numPipeTypes = selection.getNumPipeTypes()
        for i in range(numPipeTypes):
            pipeType = selection.getPipeType(i)
            already = 0
            for pipe in self.pipeList:
                if pipe.getType() == pipeType:
                    already = 1

            if not already:
                pipe = selection.makePipe(pipeType)
                if pipe:
                    self.notify.info('Got aux graphics pipe %s (%s).' % (pipe.getType().getName(), pipe.getInterfaceName()))
                    self.pipeList.append(pipe)
                else:
                    self.notify.info('Could not make graphics pipe %s.' % pipeType.getName())

        return

    def openWindow(self, props = None, pipe = None, gsg = None, type = None, name = None, size = None, aspectRatio = None, makeCamera = 1, keepCamera = 0, scene = None, stereo = None, rawmice = 0):
        if pipe == None:
            pipe = self.pipe
            if pipe == None:
                self.makeDefaultPipe()
                pipe = self.pipe
            if pipe == None:
                return
        if isinstance(gsg, GraphicsOutput):
            gsg = gsg.getGsg()
        if pipe.getType().getName().startswith('wdx'):
            gsg = None
        if type == None:
            type = self.windowType
        if props == None:
            props = WindowProperties.getDefault()
        if size != None:
            props = WindowProperties(props)
            props.setSize(size[0], size[1])
        if name == None:
            name = 'window%s' % self.nextWindowIndex
            self.nextWindowIndex += 1
        win = None
        fbprops = FrameBufferProperties.getDefault()
        flags = GraphicsPipe.BFFbPropsOptional
        if type == 'onscreen':
            flags = flags | GraphicsPipe.BFRequireWindow
        elif type == 'offscreen':
            flags = flags | GraphicsPipe.BFRefuseWindow
        if gsg:
            win = self.graphicsEngine.makeOutput(pipe, name, 0, fbprops, props, flags, gsg)
        else:
            win = self.graphicsEngine.makeOutput(pipe, name, 0, fbprops, props, flags)
        if win == None:
            return
        if hasattr(win, 'requestProperties'):
            win.requestProperties(props)
        mainWindow = False
        if self.win == None:
            mainWindow = True
            self.win = win
        self.winList.append(win)
        if keepCamera:
            self.makeCamera(win, scene=scene, aspectRatio=aspectRatio, stereo=stereo, useCamera=base.cam)
        elif makeCamera:
            self.makeCamera(win, scene=scene, aspectRatio=aspectRatio, stereo=stereo)
        messenger.send('open_window', [win, mainWindow])
        if mainWindow:
            messenger.send('open_main_window')
        return win

    def closeWindow(self, win, keepCamera = 0):
        numRegions = win.getNumDisplayRegions()
        for i in range(numRegions):
            dr = win.getDisplayRegion(i)
            if base.direct is not None:
                for drc in base.direct.drList:
                    if drc.cam == dr.getCamera():
                        base.direct.drList.displayRegionList.remove(drc)
                        break

            cam = NodePath(dr.getCamera())
            dr.setCamera(NodePath())
            if not cam.isEmpty() and cam.node().getNumDisplayRegions() == 0 and not keepCamera:
                if self.camList.count(cam) != 0:
                    self.camList.remove(cam)
                if cam == self.cam:
                    self.cam = None
                if cam == self.cam2d:
                    self.cam2d = None
                if cam == self.cam2dp:
                    self.cam2dp = None
                cam.removeNode()

        for winCtrl in self.winControls:
            if winCtrl.win == win:
                self.winControls.remove(winCtrl)
                break

        self.graphicsEngine.removeWindow(win)
        self.winList.remove(win)
        mainWindow = False
        if win == self.win:
            mainWindow = True
            self.win = None
            if self.frameRateMeter:
                self.frameRateMeter.clearWindow()
                self.frameRateMeter = None
        messenger.send('close_window', [win, mainWindow])
        if mainWindow:
            messenger.send('close_main_window')
        if not self.winList:
            base.graphicsEngine.renderFrame()
        return

    def openDefaultWindow(self, *args, **kw):
        startDirect = kw.get('startDirect', True)
        if 'startDirect' in kw:
            del kw['startDirect']
        if self.win:
            self.openMainWindow(*args, **kw)
            self.graphicsEngine.openWindows()
            return
        self.openMainWindow(*args, **kw)
        self.graphicsEngine.openWindows()
        if self.win != None and not self.isMainWindowOpen():
            self.notify.info('Window did not open, removing.')
            self.closeWindow(self.win)
        if self.win == None:
            self.makeAllPipes()
            try:
                self.pipeList.remove(self.pipe)
            except ValueError:
                pass

            while self.win == None and self.pipeList:
                self.pipe = self.pipeList[0]
                self.notify.info('Trying pipe type %s (%s)' % (self.pipe.getType(), self.pipe.getInterfaceName()))
                self.openMainWindow(*args, **kw)
                self.graphicsEngine.openWindows()
                if self.win != None and not self.isMainWindowOpen():
                    self.notify.info('Window did not open, removing.')
                    self.closeWindow(self.win)
                if self.win == None:
                    self.pipeList.remove(self.pipe)

        if self.win == None:
            self.notify.warning("Unable to open '%s' window." % self.windowType)
            if self.requireWindow:
                raise StandardError, 'Could not open window.'
        else:
            self.notify.info('Successfully opened window of type %s (%s)' % (self.win.getType(), self.win.getPipe().getInterfaceName()))
        self.mouseInterface = self.trackball
        self.useTrackball()
        if startDirect:
            self.__doStartDirect()
        return self.win != None

    def isMainWindowOpen(self):
        if self.win != None:
            return self.win.isValid()
        return 0

    def openMainWindow(self, *args, **kw):
        keepCamera = kw.get('keepCamera', 0)
        success = 1
        oldWin = self.win
        oldLens = self.camLens
        oldClearColorActive = None
        if self.win != None:
            oldClearColorActive = self.win.getClearColorActive()
            oldClearColor = VBase4(self.win.getClearColor())
            oldClearDepthActive = self.win.getClearDepthActive()
            oldClearDepth = self.win.getClearDepth()
            oldClearStencilActive = self.win.getClearStencilActive()
            oldClearStencil = self.win.getClearStencil()
            self.closeWindow(self.win, keepCamera=keepCamera)
        self.openWindow(*args, **kw)
        if self.win == None:
            self.win = oldWin
            self.winList.append(oldWin)
            success = 0
        if self.win != None:
            if isinstance(self.win, GraphicsWindow):
                self.setupMouse(self.win)
            self.makeCamera2d(self.win)
            self.makeCamera2dp(self.win)
            if oldLens != None:
                self.camNode.setLens(oldLens)
                self.camLens = oldLens
            if oldClearColorActive != None:
                self.win.setClearColorActive(oldClearColorActive)
                self.win.setClearColor(oldClearColor)
                self.win.setClearDepthActive(oldClearDepthActive)
                self.win.setClearDepth(oldClearDepth)
                self.win.setClearStencilActive(oldClearStencilActive)
                self.win.setClearStencil(oldClearStencil)
            flag = self.config.GetBool('show-frame-rate-meter', False)
            if self.appRunner is not None and self.appRunner.allowPythonDev:
                flag = True
            self.setFrameRateMeter(flag)
        return success

    def setSleep(self, amount):
        if self.clientSleep == amount:
            return
        self.clientSleep = amount
        if amount == 0.0:
            self.taskMgr.remove('clientSleep')
        else:
            self.taskMgr.remove('clientSleep')
            self.taskMgr.add(self.sleepCycleTask, 'clientSleep', priority=55)

    def sleepCycleTask(self, task):
        Thread.sleep(self.clientSleep)
        return Task.cont

    def setFrameRateMeter(self, flag):
        if flag:
            if not self.frameRateMeter:
                self.frameRateMeter = FrameRateMeter('frameRateMeter')
                self.frameRateMeter.setupWindow(self.win)
        elif self.frameRateMeter:
            self.frameRateMeter.clearWindow()
            self.frameRateMeter = None
        return

    def setupWindowControls(self, winCtrl = None):
        if winCtrl is None:
            winCtrl = WindowControls(self.win, mouseWatcher=self.mouseWatcher, cam=self.camera, camNode=self.camNode, cam2d=self.camera2d, mouseKeyboard=self.dataRoot.find('**/*'))
        self.winControls.append(winCtrl)
        return

    def setupRender(self):
        self.render = NodePath('render')
        self.render.setAttrib(RescaleNormalAttrib.makeDefault())
        self.render.setTwoSided(0)
        self.backfaceCullingEnabled = 1
        self.textureEnabled = 1
        self.wireframeEnabled = 0

    def setupRender2d(self):
        self.render2d = NodePath('render2d')
        self.render2d.setDepthTest(0)
        self.render2d.setDepthWrite(0)
        self.render2d.setMaterialOff(1)
        self.render2d.setTwoSided(1)
        aspectRatio = self.getAspectRatio()
        self.aspect2d = self.render2d.attachNewNode(PGTop('aspect2d'))
        self.aspect2d.setScale(1.0 / aspectRatio, 1.0, 1.0)
        self.a2dBackground = self.aspect2d.attachNewNode('a2dBackground')
        self.a2dTop = 1.0
        self.a2dBottom = -1.0
        self.a2dLeft = -aspectRatio
        self.a2dRight = aspectRatio
        self.a2dTopCenter = self.aspect2d.attachNewNode('a2dTopCenter')
        self.a2dTopCenterNs = self.aspect2d.attachNewNode('a2dTopCenterNS')
        self.a2dBottomCenter = self.aspect2d.attachNewNode('a2dBottomCenter')
        self.a2dBottomCenterNs = self.aspect2d.attachNewNode('a2dBottomCenterNS')
        self.a2dLeftCenter = self.aspect2d.attachNewNode('a2dLeftCenter')
        self.a2dLeftCenterNs = self.aspect2d.attachNewNode('a2dLeftCenterNS')
        self.a2dRightCenter = self.aspect2d.attachNewNode('a2dRightCenter')
        self.a2dRightCenterNs = self.aspect2d.attachNewNode('a2dRightCenterNS')
        self.a2dTopLeft = self.aspect2d.attachNewNode('a2dTopLeft')
        self.a2dTopLeftNs = self.aspect2d.attachNewNode('a2dTopLeftNS')
        self.a2dTopRight = self.aspect2d.attachNewNode('a2dTopRight')
        self.a2dTopRightNs = self.aspect2d.attachNewNode('a2dTopRightNS')
        self.a2dBottomLeft = self.aspect2d.attachNewNode('a2dBottomLeft')
        self.a2dBottomLeftNs = self.aspect2d.attachNewNode('a2dBottomLeftNS')
        self.a2dBottomRight = self.aspect2d.attachNewNode('a2dBottomRight')
        self.a2dBottomRightNs = self.aspect2d.attachNewNode('a2dBottomRightNS')
        self.a2dTopCenter.setPos(0, 0, self.a2dTop)
        self.a2dTopCenterNs.setPos(0, 0, self.a2dTop)
        self.a2dBottomCenter.setPos(0, 0, self.a2dBottom)
        self.a2dBottomCenterNs.setPos(0, 0, self.a2dBottom)
        self.a2dLeftCenter.setPos(self.a2dLeft, 0, 0)
        self.a2dLeftCenterNs.setPos(self.a2dLeft, 0, 0)
        self.a2dRightCenter.setPos(self.a2dRight, 0, 0)
        self.a2dRightCenterNs.setPos(self.a2dRight, 0, 0)
        self.a2dTopLeft.setPos(self.a2dLeft, 0, self.a2dTop)
        self.a2dTopLeftNs.setPos(self.a2dLeft, 0, self.a2dTop)
        self.a2dTopRight.setPos(self.a2dRight, 0, self.a2dTop)
        self.a2dTopRightNs.setPos(self.a2dRight, 0, self.a2dTop)
        self.a2dBottomLeft.setPos(self.a2dLeft, 0, self.a2dBottom)
        self.a2dBottomLeftNs.setPos(self.a2dLeft, 0, self.a2dBottom)
        self.a2dBottomRight.setPos(self.a2dRight, 0, self.a2dBottom)
        self.a2dBottomRightNs.setPos(self.a2dRight, 0, self.a2dBottom)
        xsize, ysize = self.getSize()
        self.pixel2d = self.render2d.attachNewNode(PGTop('pixel2d'))
        self.pixel2d.setPos(-1, 0, 1)
        if xsize > 0 and ysize > 0:
            self.pixel2d.setScale(2.0 / xsize, 1.0, 2.0 / ysize)

    def setupRender2dp(self):
        self.render2dp = NodePath('render2dp')
        dt = DepthTestAttrib.make(DepthTestAttrib.MNone)
        dw = DepthWriteAttrib.make(DepthWriteAttrib.MOff)
        self.render2dp.setDepthTest(0)
        self.render2dp.setDepthWrite(0)
        self.render2dp.setMaterialOff(1)
        self.render2dp.setTwoSided(1)
        aspectRatio = self.getAspectRatio()
        self.aspect2dp = self.render2dp.attachNewNode(PGTop('aspect2dp'))
        self.aspect2dp.node().setStartSort(16384)
        self.aspect2dp.setScale(1.0 / aspectRatio, 1.0, 1.0)
        self.a2dpTop = 1.0
        self.a2dpBottom = -1.0
        self.a2dpLeft = -aspectRatio
        self.a2dpRight = aspectRatio
        self.a2dpTopCenter = self.aspect2dp.attachNewNode('a2dpTopCenter')
        self.a2dpBottomCenter = self.aspect2dp.attachNewNode('a2dpBottomCenter')
        self.a2dpLeftCenter = self.aspect2dp.attachNewNode('a2dpLeftCenter')
        self.a2dpRightCenter = self.aspect2dp.attachNewNode('a2dpRightCenter')
        self.a2dpTopLeft = self.aspect2dp.attachNewNode('a2dpTopLeft')
        self.a2dpTopRight = self.aspect2dp.attachNewNode('a2dpTopRight')
        self.a2dpBottomLeft = self.aspect2dp.attachNewNode('a2dpBottomLeft')
        self.a2dpBottomRight = self.aspect2dp.attachNewNode('a2dpBottomRight')
        self.a2dpTopCenter.setPos(0, 0, self.a2dpTop)
        self.a2dpBottomCenter.setPos(0, 0, self.a2dpBottom)
        self.a2dpLeftCenter.setPos(self.a2dpLeft, 0, 0)
        self.a2dpRightCenter.setPos(self.a2dpRight, 0, 0)
        self.a2dpTopLeft.setPos(self.a2dpLeft, 0, self.a2dpTop)
        self.a2dpTopRight.setPos(self.a2dpRight, 0, self.a2dpTop)
        self.a2dpBottomLeft.setPos(self.a2dpLeft, 0, self.a2dpBottom)
        self.a2dpBottomRight.setPos(self.a2dpRight, 0, self.a2dpBottom)
        xsize, ysize = self.getSize()
        self.pixel2dp = self.render2dp.attachNewNode(PGTop('pixel2dp'))
        self.pixel2dp.node().setStartSort(16384)
        self.pixel2dp.setPos(-1, 0, 1)
        if xsize > 0 and ysize > 0:
            self.pixel2dp.setScale(2.0 / xsize, 1.0, 2.0 / ysize)

    def getAspectRatio(self, win = None):
        if self.__configAspectRatio:
            return self.__configAspectRatio
        aspectRatio = 1
        if win == None:
            win = self.win
        if win != None and win.hasSize():
            if win.getYSize() == 0 or win.getXSize() == 0:
                return 1
            aspectRatio = float(win.getXSize()) / float(win.getYSize())
        else:
            if win == None or not hasattr(win, 'getRequestedProperties'):
                props = WindowProperties.getDefault()
            else:
                props = win.getRequestedProperties()
                if not props.hasSize():
                    props = WindowProperties.getDefault()
            if props.hasSize():
                aspectRatio = float(props.getXSize()) / float(props.getYSize())
        return aspectRatio

    def getSize(self, win = None):
        if win == None:
            win = self.win
        if win != None and win.hasSize():
            return (win.getXSize(), win.getYSize())
        else:
            if win == None or not hasattr(win, 'getRequestedProperties'):
                props = WindowProperties.getDefault()
            else:
                props = win.getRequestedProperties()
                if not props.hasSize():
                    props = WindowProperties.getDefault()
            if props.hasSize():
                return (props.getXSize(), props.getYSize())
        return

    def makeCamera(self, win, sort = 0, scene = None, displayRegion = (0,
 1,
 0,
 1), stereo = None, aspectRatio = None, clearDepth = 0, clearColor = None, lens = None, camName = 'cam', mask = None, useCamera = None):
        if self.camera == None:
            self.camera = self.render.attachNewNode(ModelNode('camera'))
            self.camera.node().setPreserveTransform(ModelNode.PTLocal)
            __builtin__.camera = self.camera
        if useCamera:
            cam = useCamera
            camNode = useCamera.node()
            lens = camNode.getLens()
            cam.reparentTo(self.camera)
        else:
            camNode = Camera(camName)
            if lens == None:
                lens = PerspectiveLens()
                if aspectRatio == None:
                    aspectRatio = self.getAspectRatio(win)
                lens.setAspectRatio(aspectRatio)
            cam = self.camera.attachNewNode(camNode)
        if lens != None:
            camNode.setLens(lens)
        if scene != None:
            camNode.setScene(scene)
        if mask != None:
            if isinstance(mask, int):
                mask = BitMask32(mask)
            camNode.setCameraMask(mask)
        if self.cam == None:
            self.cam = cam
            self.camNode = camNode
            self.camLens = lens
        self.camList.append(cam)
        if stereo is not None:
            if stereo:
                dr = win.makeStereoDisplayRegion(*displayRegion)
            else:
                dr = win.makeMonoDisplayRegion(*displayRegion)
        else:
            dr = win.makeDisplayRegion(*displayRegion)
        dr.setSort(sort)
        if clearDepth:
            dr.setClearDepthActive(1)
        elif dr.isStereo():
            dr.getRightEye().setClearDepthActive(1)
        if clearColor:
            dr.setClearColorActive(1)
            dr.setClearColor(clearColor)
        dr.setCamera(cam)
        return cam

    def makeCamera2d(self, win, sort = 10, displayRegion = (0,
 1,
 0,
 1), coords = (-1,
 1,
 -1,
 1), lens = None, cameraName = None):
        dr = win.makeMonoDisplayRegion(*displayRegion)
        dr.setSort(sort)
        dr.setClearDepthActive(1)
        dr.setIncompleteRender(False)
        left, right, bottom, top = coords
        if cameraName:
            cam2dNode = Camera('cam2d_' + cameraName)
        else:
            cam2dNode = Camera('cam2d')
        if lens == None:
            lens = OrthographicLens()
            lens.setFilmSize(right - left, top - bottom)
            lens.setFilmOffset((right + left) * 0.5, (top + bottom) * 0.5)
            lens.setNearFar(-1000, 1000)
        cam2dNode.setLens(lens)
        if self.camera2d == None:
            self.camera2d = self.render2d.attachNewNode('camera2d')
        camera2d = self.camera2d.attachNewNode(cam2dNode)
        dr.setCamera(camera2d)
        if self.cam2d == None:
            self.cam2d = camera2d
        return camera2d

    def makeCamera2dp(self, win, sort = 20, displayRegion = (0,
 1,
 0,
 1), coords = (-1,
 1,
 -1,
 1), lens = None, cameraName = None):
        dr = win.makeMonoDisplayRegion(*displayRegion)
        dr.setSort(sort)
        if hasattr(dr, 'setIncompleteRender'):
            dr.setIncompleteRender(False)
        left, right, bottom, top = coords
        if cameraName:
            cam2dNode = Camera('cam2dp_' + cameraName)
        else:
            cam2dNode = Camera('cam2dp')
        if lens == None:
            lens = OrthographicLens()
            lens.setFilmSize(right - left, top - bottom)
            lens.setFilmOffset((right + left) * 0.5, (top + bottom) * 0.5)
            lens.setNearFar(-1000, 1000)
        cam2dNode.setLens(lens)
        if self.camera2dp == None:
            self.camera2dp = self.render2dp.attachNewNode('camera2dp')
        camera2dp = self.camera2dp.attachNewNode(cam2dNode)
        dr.setCamera(camera2dp)
        if self.cam2dp == None:
            self.cam2dp = camera2dp
        return camera2dp

    def setupDataGraph(self):
        self.dataRoot = NodePath('dataRoot')
        self.dataRootNode = self.dataRoot.node()
        self.dataUnused = NodePath('dataUnused')

    def setupMouse(self, win, fMultiWin = False):
        if not fMultiWin and self.buttonThrowers != None:
            for bt in self.buttonThrowers:
                mw = bt.getParent()
                mk = mw.getParent()
                bt.removeNode()
                mw.removeNode()
                mk.removeNode()

        bts, pws = self.setupMouseCB(win)
        if fMultiWin:
            return bts[0]
        self.buttonThrowers = bts[:]
        self.pointerWatcherNodes = pws[:]
        self.mouseWatcher = self.buttonThrowers[0].getParent()
        self.mouseWatcherNode = self.mouseWatcher.node()
        if self.recorder:
            mw = self.buttonThrowers[0].getParent()
            mouseRecorder = MouseRecorder('mouse')
            self.recorder.addRecorder('mouse', mouseRecorder.upcastToRecorderBase())
            np = mw.getParent().attachNewNode(mouseRecorder)
            mw.reparentTo(np)
        self.trackball = self.dataUnused.attachNewNode(Trackball('trackball'))
        self.drive = self.dataUnused.attachNewNode(DriveInterface('drive'))
        self.mouse2cam = self.dataUnused.attachNewNode(Transform2SG('mouse2cam'))
        self.mouse2cam.node().setNode(self.camera.node())
        mw = self.buttonThrowers[0].getParent()
        self.timeButtonThrower = mw.attachNewNode(ButtonThrower('timeButtons'))
        self.timeButtonThrower.node().setPrefix('time-')
        self.timeButtonThrower.node().setTimeFlag(1)
        self.aspect2d.node().setMouseWatcher(mw.node())
        self.aspect2dp.node().setMouseWatcher(mw.node())
        self.pixel2d.node().setMouseWatcher(mw.node())
        self.pixel2dp.node().setMouseWatcher(mw.node())
        mw.node().addRegion(PGMouseWatcherBackground())
        return

    def setupMouseCB(self, win):
        buttonThrowers = []
        pointerWatcherNodes = []
        for i in range(win.getNumInputDevices()):
            name = win.getInputDeviceName(i)
            mk = self.dataRoot.attachNewNode(MouseAndKeyboard(win, i, name))
            mw = mk.attachNewNode(MouseWatcher('watcher%s' % i))
            mb = mw.node().getModifierButtons()
            mb.addButton(KeyboardButton.shift())
            mb.addButton(KeyboardButton.control())
            mb.addButton(KeyboardButton.alt())
            mb.addButton(KeyboardButton.meta())
            mw.node().setModifierButtons(mb)
            bt = mw.attachNewNode(ButtonThrower('buttons%s' % i))
            if i != 0:
                bt.node().setPrefix('mousedev%s-' % i)
            mods = ModifierButtons()
            mods.addButton(KeyboardButton.shift())
            mods.addButton(KeyboardButton.control())
            mods.addButton(KeyboardButton.alt())
            mods.addButton(KeyboardButton.meta())
            bt.node().setModifierButtons(mods)
            buttonThrowers.append(bt)
            if win.hasPointer(i):
                pointerWatcherNodes.append(mw.node())

        return (buttonThrowers, pointerWatcherNodes)

    def enableSoftwareMousePointer(self):
        mouseViz = render2d.attachNewNode('mouseViz')
        lilsmiley = loader.loadModel('lilsmiley')
        lilsmiley.reparentTo(mouseViz)
        aspectRatio = self.getAspectRatio()
        height = self.win.getYSize()
        lilsmiley.setScale(32.0 / height / aspectRatio, 1.0, 32.0 / height)
        self.mouseWatcherNode.setGeometry(mouseViz.node())

    def getAlt(self):
        return self.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt())

    def getShift(self):
        return self.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.shift())

    def getControl(self):
        return self.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control())

    def getMeta(self):
        return self.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.meta())

    def addAngularIntegrator(self):
        if not self.physicsMgrAngular:
            self.physicsMgrAngular = 1
            integrator = AngularEulerIntegrator()
            self.physicsMgr.attachAngularIntegrator(integrator)

    def enableParticles(self):
        if not self.particleMgrEnabled:
            if not self.particleMgr:
                from direct.particles.ParticleManagerGlobal import particleMgr
                self.particleMgr = particleMgr
                self.particleMgr.setFrameStepping(1)
            if not self.physicsMgr:
                from PhysicsManagerGlobal import physicsMgr
                self.physicsMgr = physicsMgr
                integrator = LinearEulerIntegrator()
                self.physicsMgr.attachLinearIntegrator(integrator)
            self.particleMgrEnabled = 1
            self.physicsMgrEnabled = 1
            self.taskMgr.remove('manager-update')
            self.taskMgr.add(self.updateManagers, 'manager-update')

    def disableParticles(self):
        if self.particleMgrEnabled:
            self.particleMgrEnabled = 0
            self.physicsMgrEnabled = 0
            self.taskMgr.remove('manager-update')

    def toggleParticles(self):
        if self.particleMgrEnabled == 0:
            self.enableParticles()
        else:
            self.disableParticles()

    def isParticleMgrEnabled(self):
        return self.particleMgrEnabled

    def isPhysicsMgrEnabled(self):
        return self.physicsMgrEnabled

    def updateManagers(self, state):
        dt = globalClock.getDt()
        if self.particleMgrEnabled == 1:
            self.particleMgr.doParticles(dt)
        if self.physicsMgrEnabled == 1:
            self.physicsMgr.doPhysics(dt)
        return Task.cont

    def createStats(self, hostname = None, port = None):
        if not self.wantStats:
            return False
        if PStatClient.isConnected():
            PStatClient.disconnect()
        if hostname is None:
            hostname = ''
        if port is None:
            port = -1
        PStatClient.connect(hostname, port)
        return PStatClient.isConnected()

    def addSfxManager(self, extraSfxManager):
        self.sfxManagerList.append(extraSfxManager)
        if extraSfxManager != None:
            newSfxManagerIsValid = extraSfxManager.isValid()
            self.sfxManagerIsValidList.append(newSfxManagerIsValid)
            newSfxManagerIsValid and extraSfxManager.setActive(self.sfxActive)
        return

    def createBaseAudioManagers(self):
        self.sfxPlayer = SfxPlayer.SfxPlayer()
        sfxManager = AudioManager.createAudioManager()
        self.addSfxManager(sfxManager)
        self.musicManager = AudioManager.createAudioManager()
        if self.musicManager != None:
            self.musicManagerIsValid = self.musicManager.isValid()
            self.musicManagerIsValid and self.musicManager.setConcurrentSoundLimit(1)
            self.musicManager.setActive(self.musicActive)
        return

    def enableMusic(self, bEnableMusic):
        if self.AppHasAudioFocus and self.musicManagerIsValid:
            self.musicManager.setActive(bEnableMusic)
        self.musicActive = bEnableMusic
        if bEnableMusic:
            messenger.send('MusicEnabled')
            self.notify.debug('Enabling music')
        else:
            self.notify.debug('Disabling music')

    def SetAllSfxEnables(self, bEnabled):
        for i in range(len(self.sfxManagerList)):
            if self.sfxManagerIsValidList[i]:
                self.sfxManagerList[i].setActive(bEnabled)

    def enableSoundEffects(self, bEnableSoundEffects):
        if self.AppHasAudioFocus or bEnableSoundEffects == 0:
            self.SetAllSfxEnables(bEnableSoundEffects)
        self.sfxActive = bEnableSoundEffects
        if bEnableSoundEffects:
            self.notify.debug('Enabling sound effects')
        else:
            self.notify.debug('Disabling sound effects')

    def disableAllAudio(self):
        self.AppHasAudioFocus = 0
        self.SetAllSfxEnables(0)
        if self.musicManagerIsValid:
            self.musicManager.setActive(0)
        self.notify.debug('Disabling audio')

    def enableAllAudio(self):
        self.AppHasAudioFocus = 1
        self.SetAllSfxEnables(self.sfxActive)
        if self.musicManagerIsValid:
            self.musicManager.setActive(self.musicActive)
        self.notify.debug('Enabling audio')

    def loadSfx(self, name):
        return self.loader.loadSfx(name)

    def loadMusic(self, name):
        return self.loader.loadMusic(name)

    def playSfx(self, sfx, looping = 0, interrupt = 1, volume = None, time = 0.0, node = None, listener = None, cutoff = None):
        return self.sfxPlayer.playSfx(sfx, looping, interrupt, volume, time, node, listener, cutoff)

    def playMusic(self, music, looping = 0, interrupt = 1, volume = None, time = 0.0):
        if music:
            if volume != None:
                music.setVolume(volume)
            if interrupt or music.status() != AudioSound.PLAYING:
                music.setTime(time)
                music.setLoop(looping)
                music.play()
        return

    def __resetPrevTransform(self, state):
        PandaNode.resetAllPrevTransform()
        return Task.cont

    def __dataLoop(self, state):
        self.dgTrav.traverse(self.dataRootNode)
        return Task.cont

    def __ivalLoop(self, state):
        IntervalManager.ivalMgr.step()
        return Task.cont

    def initShadowTrav(self):
        if not self.shadowTrav:
            self.shadowTrav = CollisionTraverser('base.shadowTrav')
            self.shadowTrav.setRespectPrevTransform(False)

    def __shadowCollisionLoop(self, state):
        if self.shadowTrav:
            self.shadowTrav.traverse(self.render)
        return Task.cont

    def __collisionLoop(self, state):
        if self.cTrav:
            self.cTrav.traverse(self.render)
        if self.appTrav:
            self.appTrav.traverse(self.render)
        if self.shadowTrav:
            self.shadowTrav.traverse(self.render)
        messenger.send('collisionLoopFinished')
        return Task.cont

    def __audioLoop(self, state):
        if self.musicManager != None:
            self.musicManager.update()
        for x in self.sfxManagerList:
            x.update()

        return Task.cont

    def __igLoop(self, state):
        onScreenDebug.render()
        if self.recorder:
            self.recorder.recordFrame()
        self.graphicsEngine.renderFrame()
        if self.clusterSyncFlag:
            self.graphicsEngine.syncFrame()
        if self.multiClientSleep:
            time.sleep(0)
        onScreenDebug.clear()
        if self.recorder:
            self.recorder.playFrame()
        if self.mainWinMinimized:
            time.sleep(0.1)
        throwNewFrame()
        return Task.cont

    def __igLoopSync(self, state):
        onScreenDebug.render()
        if self.recorder:
            self.recorder.recordFrame()
        self.cluster.collectData()
        self.graphicsEngine.renderFrame()
        if self.clusterSyncFlag:
            self.graphicsEngine.syncFrame()
        if self.multiClientSleep:
            time.sleep(0)
        onScreenDebug.clear()
        if self.recorder:
            self.recorder.playFrame()
        if self.mainWinMinimized:
            time.sleep(0.1)
        self.graphicsEngine.readyFlip()
        self.cluster.waitForFlipCommand()
        self.graphicsEngine.flipFrame()
        throwNewFrame()
        return Task.cont

    def restart(self, clusterSync = False, cluster = None):
        self.shutdown()
        self.taskMgr.add(self.__resetPrevTransform, 'resetPrevTransform', priority=-51)
        self.taskMgr.add(self.__dataLoop, 'dataLoop', priority=-50)
        self.__deadInputs = 0
        self.taskMgr.add(self.__ivalLoop, 'ivalLoop', priority=20)
        self.taskMgr.add(self.__collisionLoop, 'collisionLoop', priority=30)
        self.cluster = cluster
        if not clusterSync or cluster == None:
            self.taskMgr.add(self.__igLoop, 'igLoop', priority=50)
        else:
            self.taskMgr.add(self.__igLoopSync, 'igLoop', priority=50)
        self.taskMgr.add(self.__audioLoop, 'audioLoop', priority=60)
        self.eventMgr.restart()
        return

    def shutdown(self):
        self.taskMgr.remove('audioLoop')
        self.taskMgr.remove('igLoop')
        self.taskMgr.remove('shadowCollisionLoop')
        self.taskMgr.remove('collisionLoop')
        self.taskMgr.remove('dataLoop')
        self.taskMgr.remove('resetPrevTransform')
        self.taskMgr.remove('ivalLoop')
        self.eventMgr.shutdown()

    def getBackgroundColor(self, win = None):
        if win == None:
            win = self.win
        return VBase4(win.getClearColor())

    def setBackgroundColor(self, r = None, g = None, b = None, a = 0.0, win = None):
        if g != None:
            color = VBase4(r, g, b, a)
        else:
            arg = r
            if isinstance(arg, VBase4):
                color = arg
            else:
                color = VBase4(arg[0], arg[1], arg[2], a)
        if win == None:
            win = self.win
        if win:
            win.setClearColor(color)
        return

    def toggleBackface(self):
        if self.backfaceCullingEnabled:
            self.backfaceCullingOff()
        else:
            self.backfaceCullingOn()

    def backfaceCullingOn(self):
        if not self.backfaceCullingEnabled:
            self.render.setTwoSided(0)
        self.backfaceCullingEnabled = 1

    def backfaceCullingOff(self):
        if self.backfaceCullingEnabled:
            self.render.setTwoSided(1)
        self.backfaceCullingEnabled = 0

    def toggleTexture(self):
        if self.textureEnabled:
            self.textureOff()
        else:
            self.textureOn()

    def textureOn(self):
        self.render.clearTexture()
        self.textureEnabled = 1

    def textureOff(self):
        self.render.setTextureOff(100)
        self.textureEnabled = 0

    def toggleWireframe(self):
        if self.wireframeEnabled:
            self.wireframeOff()
        else:
            self.wireframeOn()

    def wireframeOn(self):
        self.render.setRenderModeWireframe(100)
        self.render.setTwoSided(1)
        self.wireframeEnabled = 1

    def wireframeOff(self):
        self.render.clearRenderMode()
        render.setTwoSided(not self.backfaceCullingEnabled)
        self.wireframeEnabled = 0

    def disableMouse(self):
        if self.mouse2cam:
            self.mouse2cam.reparentTo(self.dataUnused)

    def enableMouse(self):
        if self.mouse2cam:
            self.mouse2cam.reparentTo(self.mouseInterface)

    def silenceInput(self):
        if not self.__deadInputs:
            self.__deadInputs = taskMgr.remove('dataLoop')

    def reviveInput(self):
        if self.__deadInputs:
            self.eventMgr.doEvents()
            self.dgTrav.traverse(base.dataRootNode)
            self.eventMgr.eventQueue.clear()
            self.taskMgr.add(self.__dataLoop, 'dataLoop', priority=-50)
            self.__deadInputs = 0

    def setMouseOnNode(self, newNode):
        if self.mouse2cam:
            self.mouse2cam.node().setNode(newNode)

    def changeMouseInterface(self, changeTo):
        self.mouseInterface.reparentTo(self.dataUnused)
        self.mouseInterface = changeTo
        self.mouseInterfaceNode = self.mouseInterface.node()
        self.mouseInterface.reparentTo(self.mouseWatcher)
        if self.mouse2cam:
            self.mouse2cam.reparentTo(self.mouseInterface)

    def useDrive(self):
        if self.drive:
            self.changeMouseInterface(self.drive)
            self.mouseInterfaceNode.reset()
            self.mouseInterfaceNode.setZ(4.0)

    def useTrackball(self):
        if self.trackball:
            self.changeMouseInterface(self.trackball)

    def toggleTexMem(self):
        if self.texmem and not self.texmem.cleanedUp:
            self.texmem.cleanup()
            self.texmem = None
            return
        from direct.showutil.TexMemWatcher import TexMemWatcher
        self.texmem = TexMemWatcher()
        return

    def toggleShowVertices(self):
        if self.showVertices:
            self.showVertices.node().setActive(0)
            dr = self.showVertices.node().getDisplayRegion(0)
            base.win.removeDisplayRegion(dr)
            self.showVertices.removeNode()
            self.showVertices = None
            return
        dr = base.win.makeDisplayRegion()
        dr.setSort(1000)
        cam = Camera('showVertices')
        cam.setLens(base.camLens)
        override = 100000
        t = NodePath('t')
        t.setColor(1, 0, 1, 0.02, override)
        t.setColorScale(1, 1, 1, 1, override)
        t.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha), override)
        t.setAttrib(RenderModeAttrib.make(RenderModeAttrib.MPoint, 10), override)
        t.setTwoSided(True, override)
        t.setBin('fixed', 0, override)
        t.setDepthTest(False, override)
        t.setDepthWrite(False, override)
        t.setLightOff(override)
        t.setShaderOff(override)
        t.setFogOff(override)
        t.setAttrib(AntialiasAttrib.make(AntialiasAttrib.MNone), override)
        t.setAttrib(RescaleNormalAttrib.make(RescaleNormalAttrib.MNone), override)
        t.setTextureOff(override)
        if self.config.GetBool('round-show-vertices', False):
            spot = PNMImage(256, 256, 1)
            spot.renderSpot((1, 1, 1, 1), (0, 0, 0, 0), 0.8, 1)
            tex = Texture('spot')
            tex.load(spot)
            tex.setFormat(tex.FAlpha)
            t.setTexture(tex, override)
            t.setAttrib(TexGenAttrib.make(TextureStage.getDefault(), TexGenAttrib.MPointSprite), override)
        cam.setInitialState(t.getState())
        cam.setCameraMask(~PandaNode.getOverallBit())
        self.showVertices = self.cam.attachNewNode(cam)
        dr.setCamera(self.showVertices)
        return

    def oobe(self):
        try:
            self.oobeMode
        except:
            self.oobeMode = 0
            self.oobeCamera = self.hidden.attachNewNode('oobeCamera')
            self.oobeCameraTrackball = self.oobeCamera.attachNewNode('oobeCameraTrackball')
            self.oobeLens = PerspectiveLens()
            self.oobeLens.setAspectRatio(self.getAspectRatio())
            self.oobeLens.setNearFar(0.1, 10000.0)
            self.oobeLens.setMinFov(40)
            self.oobeTrackball = self.dataUnused.attachNewNode(Trackball('oobeTrackball'), 1)
            self.oobe2cam = self.oobeTrackball.attachNewNode(Transform2SG('oobe2cam'))
            self.oobe2cam.node().setNode(self.oobeCameraTrackball.node())
            self.oobeVis = loader.loadModel('models/misc/camera', okMissing=True)
            if not self.oobeVis:
                self.oobeVis = NodePath('oobeVis')
            self.oobeVis.node().setFinal(1)
            self.oobeVis.setLightOff(1)
            self.oobeCullFrustum = None
            self.oobeCullFrustumVis = None
            self.accept('oobe-down', self.__oobeButton, extraArgs=[''])
            self.accept('oobe-repeat', self.__oobeButton, extraArgs=['-repeat'])
            self.accept('oobe-up', self.__oobeButton, extraArgs=['-up'])

        if self.oobeMode:
            if self.oobeCullFrustum != None:
                self.oobeCull()
            if self.oobeVis:
                self.oobeVis.reparentTo(self.hidden)
            self.mouseInterfaceNode.clearButton(KeyboardButton.control())
            self.oobeTrackball.detachNode()
            bt = self.buttonThrowers[0].node()
            bt.setSpecificFlag(1)
            bt.setButtonDownEvent('')
            bt.setButtonRepeatEvent('')
            bt.setButtonUpEvent('')
            self.cam.reparentTo(self.camera)
            self.camNode.setLens(self.camLens)
            self.oobeCamera.reparentTo(self.hidden)
            self.oobeMode = 0
            bboard.post('oobeEnabled', False)
        else:
            bboard.post('oobeEnabled', True)
            try:
                cameraParent = localAvatar
            except:
                cameraParent = self.camera.getParent()

            self.oobeCamera.reparentTo(cameraParent)
            self.oobeCamera.clearMat()
            self.mouseInterfaceNode.requireButton(KeyboardButton.control(), True)
            self.oobeTrackball.node().requireButton(KeyboardButton.control(), False)
            self.oobeTrackball.reparentTo(self.mouseWatcher)
            mat = Mat4.translateMat(0, -10, 3) * self.camera.getMat(cameraParent)
            mat.invertInPlace()
            self.oobeTrackball.node().setMat(mat)
            self.cam.reparentTo(self.oobeCameraTrackball)
            bt = self.buttonThrowers[0].node()
            bt.setSpecificFlag(0)
            bt.setButtonDownEvent('oobe-down')
            bt.setButtonRepeatEvent('oobe-repeat')
            bt.setButtonUpEvent('oobe-up')
            if self.oobeVis:
                self.oobeVis.reparentTo(self.camera)
            self.oobeMode = 1
        return

    def __oobeButton(self, suffix, button):
        if button.startswith('mouse'):
            return
        messenger.send(button + suffix)

    def oobeCull(self):
        try:
            if not self.oobeMode:
                self.oobe()
        except:
            self.oobe()

        if self.oobeCullFrustum == None:
            pnode = LensNode('oobeCull')
            pnode.setLens(self.camLens)
            self.oobeCullFrustum = self.camera.attachNewNode(pnode)
            geom = self.camLens.makeGeometry()
            if geom != None:
                gn = GeomNode('frustum')
                gn.addGeom(geom)
                self.oobeCullFrustumVis = self.oobeVis.attachNewNode(gn)
            for cam in base.camList:
                cam.node().setCullCenter(self.oobeCullFrustum)

        else:
            for cam in base.camList:
                cam.node().setCullCenter(NodePath())

            self.oobeCullFrustum.removeNode()
            self.oobeCullFrustum = None
            if self.oobeCullFrustumVis != None:
                self.oobeCullFrustumVis.removeNode()
                self.oobeCullFrustumVis = None
        return

    def showCameraFrustum(self):
        self.removeCameraFrustum()
        geom = self.camLens.makeGeometry()
        if geom != None:
            gn = GeomNode('frustum')
            gn.addGeom(geom)
            self.camFrustumVis = self.camera.attachNewNode(gn)
        return

    def removeCameraFrustum(self):
        if self.camFrustumVis:
            self.camFrustumVis.removeNode()

    def screenshot(self, namePrefix = 'screenshot', defaultFilename = 1, source = None, imageComment = ''):
        if source == None:
            source = self.win
        if defaultFilename:
            filename = GraphicsOutput.makeScreenshotFilename(namePrefix)
        else:
            filename = Filename(namePrefix)
        if isinstance(source, Texture):
            if source.getZSize() > 1:
                saved = source.write(filename, 0, 0, 1, 0)
            else:
                saved = source.write(filename)
        else:
            saved = source.saveScreenshot(filename, imageComment)
        if saved:
            messenger.send('screenshot', [filename])
            return filename
        return

    def saveCubeMap(self, namePrefix = 'cube_map_#.png', defaultFilename = 0, source = None, camera = None, size = 128, cameraMask = PandaNode.getAllCameraMask()):
        if source == None:
            source = base.win
        if camera == None:
            if hasattr(source, 'getCamera'):
                camera = source.getCamera()
            if camera == None:
                camera = base.camera
        if hasattr(source, 'getWindow'):
            source = source.getWindow()
        rig = NodePath(namePrefix)
        buffer = source.makeCubeMap(namePrefix, size, rig, cameraMask, 1)
        if buffer == None:
            raise StandardError, 'Could not make cube map.'
        lens = rig.find('**/+Camera').node().getLens()
        lens.setNearFar(base.camLens.getNear(), base.camLens.getFar())
        rig.reparentTo(camera)
        base.graphicsEngine.openWindows()
        base.graphicsEngine.renderFrame()
        tex = buffer.getTexture()
        saved = self.screenshot(namePrefix=namePrefix, defaultFilename=defaultFilename, source=tex)
        base.graphicsEngine.removeWindow(buffer)
        rig.removeNode()
        return saved

    def saveSphereMap(self, namePrefix = 'spheremap.png', defaultFilename = 0, source = None, camera = None, size = 256, cameraMask = PandaNode.getAllCameraMask(), numVertices = 1000):
        if source == None:
            source = base.win
        if camera == None:
            if hasattr(source, 'getCamera'):
                camera = source.getCamera()
            if camera == None:
                camera = base.camera
        if hasattr(source, 'getWindow'):
            source = source.getWindow()
        toSphere = source.makeTextureBuffer(namePrefix, size, size, Texture(), 1)
        rig = NodePath(namePrefix)
        buffer = toSphere.makeCubeMap(namePrefix, size, rig, cameraMask, 0)
        if buffer == None:
            base.graphicsEngine.removeWindow(toSphere)
            raise StandardError, 'Could not make cube map.'
        lens = rig.find('**/+Camera').node().getLens()
        lens.setNearFar(base.camLens.getNear(), base.camLens.getFar())
        dr = toSphere.makeMonoDisplayRegion()
        camNode = Camera('camNode')
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        camNode.setLens(lens)
        root = NodePath('buffer')
        cam = root.attachNewNode(camNode)
        dr.setCamera(cam)
        fm = FisheyeMaker('card')
        fm.setNumVertices(numVertices)
        fm.setSquareInscribed(1, 1.1)
        fm.setReflection(1)
        card = root.attachNewNode(fm.generate())
        card.setTexture(buffer.getTexture())
        rig.reparentTo(camera)
        base.graphicsEngine.openWindows()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        saved = self.screenshot(namePrefix=namePrefix, defaultFilename=defaultFilename, source=toSphere.getTexture())
        base.graphicsEngine.removeWindow(buffer)
        base.graphicsEngine.removeWindow(toSphere)
        rig.removeNode()
        return saved

    def movie(self, namePrefix = 'movie', duration = 1.0, fps = 30, format = 'png', sd = 4, source = None):
        globalClock.setMode(ClockObject.MNonRealTime)
        globalClock.setDt(1.0 / float(fps))
        t = taskMgr.add(self._movieTask, namePrefix + '_task')
        t.frameIndex = 0
        t.numFrames = int(duration * fps)
        t.source = source
        t.outputString = namePrefix + '_%0' + repr(sd) + 'd.' + format
        t.setUponDeath(lambda state: globalClock.setMode(ClockObject.MNormal))

    def _movieTask(self, state):
        if state.frameIndex != 0:
            frameName = state.outputString % state.frameIndex
            self.notify.info('Capturing frame: ' + frameName)
            self.screenshot(namePrefix=frameName, defaultFilename=0, source=state.source)
        state.frameIndex += 1
        if state.frameIndex > state.numFrames:
            return Task.done
        else:
            return Task.cont

    def windowEvent(self, win):
        if win == self.win:
            properties = win.getProperties()
            self.notify.info('Got window event: %s' % repr(properties))
            if not properties.getOpen():
                self.notify.info('User closed main window.')
                if __dev__ and config.GetBool('auto-garbage-logging', 0):
                    GarbageReport.b_checkForGarbageLeaks()
                self.userExit()
            if properties.getForeground() and not self.mainWinForeground:
                self.mainWinForeground = 1
            elif not properties.getForeground() and self.mainWinForeground:
                self.mainWinForeground = 0
                if __dev__ and config.GetBool('auto-garbage-logging', 0):
                    GarbageReport.b_checkForGarbageLeaks()
            if properties.getMinimized() and not self.mainWinMinimized:
                self.mainWinMinimized = 1
                messenger.send('PandaPaused')
            elif not properties.getMinimized() and self.mainWinMinimized:
                self.mainWinMinimized = 0
                messenger.send('PandaRestarted')
            if not self.__configAspectRatio:
                aspectRatio = self.getAspectRatio()
                if aspectRatio != self.__oldAspectRatio:
                    self.__oldAspectRatio = aspectRatio
                    self.camLens.setAspectRatio(aspectRatio)
                    if aspectRatio < 1:
                        self.aspect2d.setScale(1.0, 1.0, aspectRatio)
                        self.a2dTop = 1.0 / aspectRatio
                        self.a2dBottom = -1.0 / aspectRatio
                        self.a2dLeft = -1
                        self.a2dRight = 1.0
                        self.aspect2dp.setScale(1.0, 1.0, aspectRatio)
                        self.a2dpTop = 1.0 / aspectRatio
                        self.a2dpBottom = -1.0 / aspectRatio
                        self.a2dpLeft = -1
                        self.a2dpRight = 1.0
                    else:
                        self.aspect2d.setScale(1.0 / aspectRatio, 1.0, 1.0)
                        self.a2dTop = 1.0
                        self.a2dBottom = -1.0
                        self.a2dLeft = -aspectRatio
                        self.a2dRight = aspectRatio
                        self.aspect2dp.setScale(1.0 / aspectRatio, 1.0, 1.0)
                        self.a2dpTop = 1.0
                        self.a2dpBottom = -1.0
                        self.a2dpLeft = -aspectRatio
                        self.a2dpRight = aspectRatio
                    self.a2dTopCenter.setPos(0, 0, self.a2dTop)
                    self.a2dBottomCenter.setPos(0, 0, self.a2dBottom)
                    self.a2dLeftCenter.setPos(self.a2dLeft, 0, 0)
                    self.a2dRightCenter.setPos(self.a2dRight, 0, 0)
                    self.a2dTopLeft.setPos(self.a2dLeft, 0, self.a2dTop)
                    self.a2dTopRight.setPos(self.a2dRight, 0, self.a2dTop)
                    self.a2dBottomLeft.setPos(self.a2dLeft, 0, self.a2dBottom)
                    self.a2dBottomRight.setPos(self.a2dRight, 0, self.a2dBottom)
                    self.a2dTopCenterNs.setPos(0, 0, self.a2dTop)
                    self.a2dBottomCenterNs.setPos(0, 0, self.a2dBottom)
                    self.a2dLeftCenterNs.setPos(self.a2dLeft, 0, 0)
                    self.a2dRightCenterNs.setPos(self.a2dRight, 0, 0)
                    self.a2dTopLeftNs.setPos(self.a2dLeft, 0, self.a2dTop)
                    self.a2dTopRightNs.setPos(self.a2dRight, 0, self.a2dTop)
                    self.a2dBottomLeftNs.setPos(self.a2dLeft, 0, self.a2dBottom)
                    self.a2dBottomRightNs.setPos(self.a2dRight, 0, self.a2dBottom)
                    self.a2dpTopCenter.setPos(0, 0, self.a2dpTop)
                    self.a2dpBottomCenter.setPos(0, 0, self.a2dpBottom)
                    self.a2dpLeftCenter.setPos(self.a2dpLeft, 0, 0)
                    self.a2dpRightCenter.setPos(self.a2dpRight, 0, 0)
                    self.a2dpTopLeft.setPos(self.a2dpLeft, 0, self.a2dpTop)
                    self.a2dpTopRight.setPos(self.a2dpRight, 0, self.a2dpTop)
                    self.a2dpBottomLeft.setPos(self.a2dpLeft, 0, self.a2dpBottom)
                    self.a2dpBottomRight.setPos(self.a2dpRight, 0, self.a2dpBottom)
                    messenger.send('aspectRatioChanged')
            if win.getXSize() > 0 and win.getYSize() > 0:
                self.pixel2d.setScale(2.0 / win.getXSize(), 1.0, 2.0 / win.getYSize())
                self.pixel2dp.setScale(2.0 / win.getXSize(), 1.0, 2.0 / win.getYSize())

    def userExit(self):
        if self.exitFunc:
            self.exitFunc()
        self.notify.info('Exiting ShowBase.')
        self.finalizeExit()

    def finalizeExit(self):
        sys.exit()

    def startWx(self, fWantWx = 1):
        self.wantWx = fWantWx
        if self.wantWx:
            initAppForGui()
            from direct.showbase import WxGlobal
            taskMgr.remove('wxLoop')
            WxGlobal.spawnWxLoop()

    def startTk(self, fWantTk = 1):
        self.wantTk = fWantTk
        if self.wantTk:
            initAppForGui()
            from direct.showbase import TkGlobal
            taskMgr.remove('tkLoop')
            TkGlobal.spawnTkLoop()

    def startDirect(self, fWantDirect = 1, fWantTk = 1, fWantWx = 0):
        self.startTk(fWantTk)
        self.startWx(fWantWx)
        self.wantDirect = fWantDirect
        if self.wantDirect:
            from direct.directtools import DirectSession
            base.direct.enable()
        else:
            __builtin__.direct = self.direct = None
        return

    def getRepository(self):
        return None

    def getAxes(self):
        return loader.loadModel('models/misc/xyzAxis.bam')

    def __doStartDirect(self):
        if self.__directStarted:
            return
        self.__directStarted = False
        fTk = self.config.GetBool('want-tk', 0)
        fWx = self.config.GetBool('want-wx', 0)
        fDirect = self.config.GetBool('want-directtools', 0) or self.config.GetString('cluster-mode', '') != ''
        self.startDirect(fWantDirect=fDirect, fWantTk=fTk, fWantWx=fWx)

    def run(self):
        if self.appRunner is None or self.appRunner.dummy or self.appRunner.interactiveConsole and not self.appRunner.initialAppImport:
            self.taskMgr.run()
        return


class WindowControls():
    __module__ = __name__

    def __init__(self, win, cam = None, camNode = None, cam2d = None, mouseWatcher = None, mouseKeyboard = None, closeCmd = lambda : 0, grid = None):
        self.win = win
        self.camera = cam
        if camNode is None and cam is not None:
            camNode = cam.node()
        self.camNode = camNode
        self.camera2d = cam2d
        self.mouseWatcher = mouseWatcher
        self.mouseKeyboard = mouseKeyboard
        self.closeCommand = closeCmd
        self.grid = grid
        return

    def __str__(self):
        s = 'window = ' + str(self.win) + '\n'
        s += 'camera = ' + str(self.camera) + '\n'
        s += 'camNode = ' + str(self.camNode) + '\n'
        s += 'camera2d = ' + str(self.camera2d) + '\n'
        s += 'mouseWatcher = ' + str(self.mouseWatcher) + '\n'
        s += 'mouseAndKeyboard = ' + str(self.mouseKeyboard) + '\n'
        return s
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ShowBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:49 Pacific Daylight Time
