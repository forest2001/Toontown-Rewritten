# 2013.08.22 22:14:14 Pacific Daylight Time
# Embedded file name: direct.gui.DirectGuiBase
__all__ = ['DirectGuiBase', 'DirectGuiWidget']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from OnscreenText import *
from OnscreenGeom import *
from OnscreenImage import *
from direct.directtools.DirectUtil import ROUND_TO
from direct.showbase import DirectObject
from direct.task import Task
from direct.showbase import ShowBase
from direct.showbase.PythonUtil import recordCreationStackStr
from pandac.PandaModules import PStatCollector
import string, types
guiObjectCollector = PStatCollector('Client::GuiObjects')

class DirectGuiBase(DirectObject.DirectObject):
    __module__ = __name__

    def __init__(self):
        self.guiId = 'guiObject'
        self.postInitialiseFuncList = []
        self.fInit = 1
        self.__componentInfo = {}
        self.__componentAliases = {}

    def defineoptions(self, keywords, optionDefs, dynamicGroups = ()):
        if not hasattr(self, '_constructorKeywords'):
            tmp = {}
            for option, value in keywords.items():
                tmp[option] = [value, 0]

            self._constructorKeywords = tmp
            self._optionInfo = {}
        if not hasattr(self, '_dynamicGroups'):
            self._dynamicGroups = ()
        self._dynamicGroups = self._dynamicGroups + tuple(dynamicGroups)
        self.addoptions(optionDefs, keywords)

    def addoptions(self, optionDefs, optionkeywords):
        optionInfo = self._optionInfo
        optionInfo_has_key = optionInfo.has_key
        keywords = self._constructorKeywords
        keywords_has_key = keywords.has_key
        FUNCTION = DGG._OPT_FUNCTION
        for name, default, function in optionDefs:
            if '_' not in name:
                default = optionkeywords.get(name, default)
                if not optionInfo_has_key(name):
                    if keywords_has_key(name):
                        value = keywords[name][0]
                        optionInfo[name] = [default, value, function]
                        del keywords[name]
                    else:
                        optionInfo[name] = [default, default, function]
                elif optionInfo[name][FUNCTION] is None:
                    optionInfo[name][FUNCTION] = function
            elif not keywords_has_key(name):
                keywords[name] = [default, 0]

        return

    def initialiseoptions(self, myClass):
        if self.__class__ is myClass:
            FUNCTION = DGG._OPT_FUNCTION
            self.fInit = 1
            for info in self._optionInfo.values():
                func = info[FUNCTION]
                if func is not None and func is not DGG.INITOPT:
                    func()

            self.fInit = 0
            unusedOptions = []
            keywords = self._constructorKeywords
            for name in keywords.keys():
                used = keywords[name][1]
                if not used:
                    index = string.find(name, '_')
                    if index < 0 or name[:index] not in self._dynamicGroups:
                        unusedOptions.append(name)

            self._constructorKeywords = {}
            if len(unusedOptions) > 0:
                if len(unusedOptions) == 1:
                    text = 'Unknown option "'
                else:
                    text = 'Unknown options "'
                raise KeyError, text + string.join(unusedOptions, ', ') + '" for ' + myClass.__name__
            self.postInitialiseFunc()
        return

    def postInitialiseFunc(self):
        for func in self.postInitialiseFuncList:
            func()

    def isinitoption(self, option):
        return self._optionInfo[option][DGG._OPT_FUNCTION] is DGG.INITOPT

    def options(self):
        options = []
        if hasattr(self, '_optionInfo'):
            for option, info in self._optionInfo.items():
                isinit = info[DGG._OPT_FUNCTION] is DGG.INITOPT
                default = info[DGG._OPT_DEFAULT]
                options.append((option, default, isinit))

            options.sort()
        return options

    def configure(self, option = None, **kw):
        if len(kw) == 0:
            if option is None:
                rtn = {}
                for option, config in self._optionInfo.items():
                    rtn[option] = (option, config[DGG._OPT_DEFAULT], config[DGG._OPT_VALUE])

                return rtn
            else:
                config = self._optionInfo[option]
                return (option, config[DGG._OPT_DEFAULT], config[DGG._OPT_VALUE])
        optionInfo = self._optionInfo
        optionInfo_has_key = optionInfo.has_key
        componentInfo = self.__componentInfo
        componentInfo_has_key = componentInfo.has_key
        componentAliases = self.__componentAliases
        componentAliases_has_key = componentAliases.has_key
        VALUE = DGG._OPT_VALUE
        FUNCTION = DGG._OPT_FUNCTION
        directOptions = []
        indirectOptions = {}
        indirectOptions_has_key = indirectOptions.has_key
        for option, value in kw.items():
            if optionInfo_has_key(option):
                if optionInfo[option][FUNCTION] is DGG.INITOPT:
                    print 'Cannot configure initialisation option "' + option + '" for ' + self.__class__.__name__
                    break
                optionInfo[option][VALUE] = value
                directOptions.append(option)
            else:
                index = string.find(option, '_')
                if index >= 0:
                    component = option[:index]
                    componentOption = option[index + 1:]
                    if componentAliases_has_key(component):
                        component, subComponent = componentAliases[component]
                        if subComponent is not None:
                            componentOption = subComponent + '_' + componentOption
                        option = component + '_' + componentOption
                    if componentInfo_has_key(component):
                        componentConfigFuncs = [componentInfo[component][1]]
                    else:
                        componentConfigFuncs = []
                        for info in componentInfo.values():
                            if info[4] == component:
                                componentConfigFuncs.append(info[1])

                        if len(componentConfigFuncs) == 0 and component not in self._dynamicGroups:
                            raise KeyError, 'Unknown option "' + option + '" for ' + self.__class__.__name__
                    for componentConfigFunc in componentConfigFuncs:
                        if not indirectOptions_has_key(componentConfigFunc):
                            indirectOptions[componentConfigFunc] = {}
                        indirectOptions[componentConfigFunc][componentOption] = value

                else:
                    raise KeyError, 'Unknown option "' + option + '" for ' + self.__class__.__name__

        map(apply, indirectOptions.keys(), ((),) * len(indirectOptions), indirectOptions.values())
        for option in directOptions:
            info = optionInfo[option]
            func = info[DGG._OPT_FUNCTION]
            if func is not None:
                func()

        return

    def __setitem__(self, key, value):
        apply(self.configure, (), {key: value})

    def cget(self, option):
        if self._optionInfo.has_key(option):
            return self._optionInfo[option][DGG._OPT_VALUE]
        else:
            index = string.find(option, '_')
            if index >= 0:
                component = option[:index]
                componentOption = option[index + 1:]
                if self.__componentAliases.has_key(component):
                    component, subComponent = self.__componentAliases[component]
                    if subComponent is not None:
                        componentOption = subComponent + '_' + componentOption
                    option = component + '_' + componentOption
                if self.__componentInfo.has_key(component):
                    componentCget = self.__componentInfo[component][3]
                    return componentCget(componentOption)
                else:
                    for info in self.__componentInfo.values():
                        if info[4] == component:
                            componentCget = info[3]
                            return componentCget(componentOption)

        raise KeyError, 'Unknown option "' + option + '" for ' + self.__class__.__name__
        return

    __getitem__ = cget

    def createcomponent(self, componentName, componentAliases, componentGroup, widgetClass, *widgetArgs, **kw):
        if '_' in componentName:
            raise ValueError, 'Component name "%s" must not contain "_"' % componentName
        if hasattr(self, '_constructorKeywords'):
            keywords = self._constructorKeywords
        else:
            keywords = {}
        for alias, component in componentAliases:
            index = string.find(component, '_')
            if index < 0:
                self.__componentAliases[alias] = (component, None)
            else:
                mainComponent = component[:index]
                subComponent = component[index + 1:]
                self.__componentAliases[alias] = (mainComponent, subComponent)
            alias = alias + '_'
            aliasLen = len(alias)
            for option in keywords.keys():
                if len(option) > aliasLen and option[:aliasLen] == alias:
                    newkey = component + '_' + option[aliasLen:]
                    keywords[newkey] = keywords[option]
                    del keywords[option]

        componentPrefix = componentName + '_'
        nameLen = len(componentPrefix)
        for option in keywords.keys():
            index = string.find(option, '_')
            if index >= 0 and componentGroup == option[:index]:
                rest = option[index + 1:]
                kw[rest] = keywords[option][0]
                keywords[option][1] = 1

        for option in keywords.keys():
            if len(option) > nameLen and option[:nameLen] == componentPrefix:
                kw[option[nameLen:]] = keywords[option][0]
                del keywords[option]

        if widgetClass is None:
            return
        if len(widgetArgs) == 1 and type(widgetArgs[0]) == types.TupleType:
            widgetArgs = widgetArgs[0]
        widget = apply(widgetClass, widgetArgs, kw)
        componentClass = widget.__class__.__name__
        self.__componentInfo[componentName] = (widget,
         widget.configure,
         componentClass,
         widget.cget,
         componentGroup)
        return widget

    def component(self, name):
        index = string.find(name, '_')
        if index < 0:
            component = name
            remainingComponents = None
        else:
            component = name[:index]
            remainingComponents = name[index + 1:]
        if self.__componentAliases.has_key(component):
            component, subComponent = self.__componentAliases[component]
            if subComponent is not None:
                if remainingComponents is None:
                    remainingComponents = subComponent
                else:
                    remainingComponents = subComponent + '_' + remainingComponents
        widget = self.__componentInfo[component][0]
        if remainingComponents is None:
            return widget
        else:
            return widget.component(remainingComponents)
        return

    def components(self):
        names = self.__componentInfo.keys()
        names.sort()
        return names

    def hascomponent(self, component):
        return self.__componentInfo.has_key(component)

    def destroycomponent(self, name):
        self.__componentInfo[name][0].destroy()
        del self.__componentInfo[name]

    def destroy(self):
        self.ignoreAll()
        del self._optionInfo
        del self.__componentInfo
        del self.postInitialiseFuncList

    def bind(self, event, command, extraArgs = []):
        gEvent = event + self.guiId
        if base.config.GetBool('debug-directgui-msgs', False):
            from direct.showbase.PythonUtil import StackTrace
            print gEvent
            print StackTrace()
        self.accept(gEvent, command, extraArgs=extraArgs)

    def unbind(self, event):
        gEvent = event + self.guiId
        self.ignore(gEvent)


def toggleGuiGridSnap():
    DirectGuiWidget.snapToGrid = 1 - DirectGuiWidget.snapToGrid


def setGuiGridSpacing(spacing):
    DirectGuiWidget.gridSpacing = spacing


if config.GetBool('record-gui-creation-stack', 0):
    DirectGuiBase = recordCreationStackStr(DirectGuiBase)

class DirectGuiWidget(DirectGuiBase, NodePath):
    __module__ = __name__
    snapToGrid = 0
    gridSpacing = 0.05
    guiEdit = config.GetBool('direct-gui-edit', 0)
    if guiEdit:
        inactiveInitState = DGG.NORMAL
    else:
        inactiveInitState = DGG.DISABLED
    guiDict = {}

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGItem, None),
         ('numStates', 1, None),
         ('invertedFrames', (), None),
         ('sortOrder', 0, None),
         ('state', DGG.NORMAL, self.setState),
         ('relief', DGG.FLAT, self.setRelief),
         ('borderWidth', (0.1, 0.1), self.setBorderWidth),
         ('borderUvWidth', (0.1, 0.1), self.setBorderUvWidth),
         ('frameSize', None, self.setFrameSize),
         ('frameColor', (0.8,
           0.8,
           0.8,
           1), self.setFrameColor),
         ('frameTexture', None, self.setFrameTexture),
         ('frameVisibleScale', (1, 1), self.setFrameVisibleScale),
         ('pad', (0, 0), self.resetFrameSize),
         ('guiId', None, DGG.INITOPT),
         ('pos', None, DGG.INITOPT),
         ('hpr', None, DGG.INITOPT),
         ('scale', None, DGG.INITOPT),
         ('color', None, DGG.INITOPT),
         ('suppressMouse', 1, DGG.INITOPT),
         ('suppressKeys', 0, DGG.INITOPT),
         ('enableEdit', 1, DGG.INITOPT))
        self.defineoptions(kw, optiondefs)
        DirectGuiBase.__init__(self)
        NodePath.__init__(self)
        self.guiItem = self['pgFunc']('')
        if self['guiId']:
            self.guiItem.setId(self['guiId'])
        self.guiId = self.guiItem.getId()
        if __dev__:
            guiObjectCollector.addLevel(1)
            guiObjectCollector.flushLevel()
            if hasattr(base, 'guiItems'):
                if self.guiId in base.guiItems:
                    base.notify.warning('duplicate guiId: %s (%s stomping %s)' % (self.guiId, self, base.guiItems[self.guiId]))
                base.guiItems[self.guiId] = self
                if hasattr(base, 'printGuiCreates'):
                    printStack()
        if parent == None:
            parent = aspect2d
        self.assign(parent.attachNewNode(self.guiItem, self['sortOrder']))
        if self['pos']:
            pos = self['pos']
            if isinstance(pos, VBase3):
                self.setPos(pos)
            else:
                apply(self.setPos, pos)
        if self['hpr']:
            hpr = self['hpr']
            if isinstance(hpr, VBase3):
                self.setHpr(hpr)
            else:
                apply(self.setHpr, hpr)
        if self['scale']:
            scale = self['scale']
            if not isinstance(scale, VBase3):
                if not type(scale) == types.IntType:
                    if type(scale) == types.FloatType:
                        self.setScale(scale)
                    else:
                        apply(self.setScale, scale)
                if self['color']:
                    color = self['color']
                    if isinstance(color, VBase4):
                        self.setColor(color)
                    else:
                        apply(self.setColor, color)
                self.setName('%s-%s' % (self.__class__.__name__, self.guiId))
                self.stateNodePath = []
                for i in range(self['numStates']):
                    self.stateNodePath.append(NodePath(self.guiItem.getStateDef(i)))

                self.frameStyle = []
                for i in range(self['numStates']):
                    self.frameStyle.append(PGFrameStyle())

                self.ll = Point3(0)
                self.ur = Point3(0)
                if self['enableEdit']:
                    self.guiEdit and self.enableEdit()
                suppressFlags = 0
                self['suppressMouse'] and suppressFlags |= MouseWatcherRegion.SFMouseButton
                suppressFlags |= MouseWatcherRegion.SFMousePosition
            self['suppressKeys'] and suppressFlags |= MouseWatcherRegion.SFOtherButton
        self.guiItem.setSuppressFlags(suppressFlags)
        self.guiDict[self.guiId] = self
        self.postInitialiseFuncList.append(self.frameInitialiseFunc)
        self.initialiseoptions(DirectGuiWidget)
        return None

    def frameInitialiseFunc(self):
        self.updateFrameStyle()
        if not self['frameSize']:
            self.resetFrameSize()

    def enableEdit(self):
        self.bind(DGG.B2PRESS, self.editStart)
        self.bind(DGG.B2RELEASE, self.editStop)
        self.bind(DGG.PRINT, self.printConfig)

    def disableEdit(self):
        self.unbind(DGG.B2PRESS)
        self.unbind(DGG.B2RELEASE)
        self.unbind(DGG.PRINT)

    def editStart(self, event):
        taskMgr.remove('guiEditTask')
        vWidget2render2d = self.getPos(render2d)
        vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
        editVec = Vec3(vWidget2render2d - vMouse2render2d)
        if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
            t = taskMgr.add(self.guiScaleTask, 'guiEditTask')
            t.refPos = vWidget2render2d
            t.editVecLen = editVec.length()
            t.initScale = self.getScale()
        else:
            t = taskMgr.add(self.guiDragTask, 'guiEditTask')
            t.editVec = editVec

    def guiScaleTask(self, state):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newEditVecLen = Vec3(state.refPos - vMouse2render2d).length()
            self.setScale(state.initScale * (newEditVecLen / state.editVecLen))
        return Task.cont

    def guiDragTask(self, state):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d + state.editVec
            self.setPos(render2d, newPos)
            if DirectGuiWidget.snapToGrid:
                newPos = self.getPos()
                newPos.set(ROUND_TO(newPos[0], DirectGuiWidget.gridSpacing), ROUND_TO(newPos[1], DirectGuiWidget.gridSpacing), ROUND_TO(newPos[2], DirectGuiWidget.gridSpacing))
                self.setPos(newPos)
        return Task.cont

    def editStop(self, event):
        taskMgr.remove('guiEditTask')

    def setState(self):
        if type(self['state']) == type(0):
            self.guiItem.setActive(self['state'])
        elif self['state'] == DGG.NORMAL or self['state'] == 'normal':
            self.guiItem.setActive(1)
        else:
            self.guiItem.setActive(0)

    def resetFrameSize(self):
        if not self.fInit:
            self.setFrameSize(fClearFrame=1)

    def setFrameSize(self, fClearFrame = 0):
        frameType = self.getFrameType()
        if self['frameSize']:
            self.bounds = self['frameSize']
            bw = (0, 0)
        else:
            if fClearFrame and frameType != PGFrameStyle.TNone:
                self.frameStyle[0].setType(PGFrameStyle.TNone)
                self.guiItem.setFrameStyle(0, self.frameStyle[0])
                self.guiItem.getStateDef(0)
            self.getBounds()
            if frameType != PGFrameStyle.TNone:
                self.frameStyle[0].setType(frameType)
                self.guiItem.setFrameStyle(0, self.frameStyle[0])
            if frameType != PGFrameStyle.TNone and frameType != PGFrameStyle.TFlat:
                bw = self['borderWidth']
            else:
                bw = (0, 0)
        self.guiItem.setFrame(self.bounds[0] - bw[0], self.bounds[1] + bw[0], self.bounds[2] - bw[1], self.bounds[3] + bw[1])

    def getBounds(self, state = 0):
        self.stateNodePath[state].calcTightBounds(self.ll, self.ur)
        self.bounds = [self.ll[0] - self['pad'][0],
         self.ur[0] + self['pad'][0],
         self.ll[2] - self['pad'][1],
         self.ur[2] + self['pad'][1]]
        return self.bounds

    def getWidth(self):
        return self.bounds[1] - self.bounds[0]

    def getHeight(self):
        return self.bounds[3] - self.bounds[2]

    def getCenter(self):
        x = self.bounds[0] + (self.bounds[1] - self.bounds[0]) / 2.0
        y = self.bounds[2] + (self.bounds[3] - self.bounds[2]) / 2.0
        return (x, y)

    def getFrameType(self, state = 0):
        return self.frameStyle[state].getType()

    def updateFrameStyle(self):
        if not self.fInit:
            for i in range(self['numStates']):
                self.guiItem.setFrameStyle(i, self.frameStyle[i])

    def setRelief(self, fSetStyle = 1):
        relief = self['relief']
        if relief == None:
            relief = PGFrameStyle.TNone
        elif isinstance(relief, types.StringTypes):
            relief = DGG.FrameStyleDict[relief]
        if relief == DGG.RAISED:
            for i in range(self['numStates']):
                if i in self['invertedFrames']:
                    self.frameStyle[1].setType(DGG.SUNKEN)
                else:
                    self.frameStyle[i].setType(DGG.RAISED)

        elif relief == DGG.SUNKEN:
            for i in range(self['numStates']):
                if i in self['invertedFrames']:
                    self.frameStyle[1].setType(DGG.RAISED)
                else:
                    self.frameStyle[i].setType(DGG.SUNKEN)

        else:
            for i in range(self['numStates']):
                self.frameStyle[i].setType(relief)

        self.updateFrameStyle()
        return

    def setFrameColor(self):
        colors = self['frameColor']
        if type(colors[0]) == types.IntType or type(colors[0]) == types.FloatType:
            colors = (colors,)
        for i in range(self['numStates']):
            if i >= len(colors):
                color = colors[-1]
            else:
                color = colors[i]
            self.frameStyle[i].setColor(color[0], color[1], color[2], color[3])

        self.updateFrameStyle()

    def setFrameTexture(self):
        textures = self['frameTexture']
        if textures == None or isinstance(textures, Texture) or isinstance(textures, types.StringTypes):
            textures = (textures,) * self['numStates']
        for i in range(self['numStates']):
            if i >= len(textures):
                texture = textures[-1]
            else:
                texture = textures[i]
            if isinstance(texture, types.StringTypes):
                texture = loader.loadTexture(texture)
            if texture:
                self.frameStyle[i].setTexture(texture)
            else:
                self.frameStyle[i].clearTexture()

        self.updateFrameStyle()
        return

    def setFrameVisibleScale(self):
        scale = self['frameVisibleScale']
        for i in range(self['numStates']):
            self.frameStyle[i].setVisibleScale(scale[0], scale[1])

        self.updateFrameStyle()

    def setBorderWidth(self):
        width = self['borderWidth']
        for i in range(self['numStates']):
            self.frameStyle[i].setWidth(width[0], width[1])

        self.updateFrameStyle()

    def setBorderUvWidth(self):
        uvWidth = self['borderUvWidth']
        for i in range(self['numStates']):
            self.frameStyle[i].setUvWidth(uvWidth[0], uvWidth[1])

        self.updateFrameStyle()

    def destroy(self):
        if hasattr(self, 'frameStyle'):
            if __dev__:
                guiObjectCollector.subLevel(1)
                guiObjectCollector.flushLevel()
                if hasattr(base, 'guiItems'):
                    if self.guiId in base.guiItems:
                        del base.guiItems[self.guiId]
                    else:
                        base.notify.warning('DirectGuiWidget.destroy(): gui item %s not in base.guiItems' % self.guiId)
            for child in self.getChildren():
                childGui = self.guiDict.get(child.getName())
                if childGui:
                    childGui.destroy()
                else:
                    parts = child.getName().split('-')
                    simpleChildGui = self.guiDict.get(parts[-1])
                    if simpleChildGui:
                        simpleChildGui.destroy()

            del self.guiDict[self.guiId]
            del self.frameStyle
            self.removeNode()
            for nodePath in self.stateNodePath:
                nodePath.removeNode()

            del self.stateNodePath
            del self.guiItem
            DirectGuiBase.destroy(self)

    def printConfig(self, indent = 0):
        space = ' ' * indent
        print space + self.guiId, '-', self.__class__.__name__
        print space + 'Pos:   ' + self.getPos().pPrintValues()
        print space + 'Scale: ' + self.getScale().pPrintValues()
        for child in self.getChildren():
            messenger.send(DGG.PRINT + child.getName(), [indent + 2])

    def copyOptions(self, other):
        for key, value in other._optionInfo.items():
            self[key] = value[1]

    def taskName(self, idString):
        return idString + '-' + str(self.guiId)

    def uniqueName(self, idString):
        return idString + '-' + str(self.guiId)

    def setProp(self, propString, value):
        self[propString] = value
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectGuiBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:16 Pacific Daylight Time
