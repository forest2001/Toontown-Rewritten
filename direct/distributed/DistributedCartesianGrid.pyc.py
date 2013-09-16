# 2013.08.22 22:14:02 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedCartesianGrid
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedNode import DistributedNode
from direct.task import Task
from direct.gui import DirectGuiGlobals
from direct.showbase.EventGroup import EventGroup
from direct.showbase.PythonUtil import report
from direct.distributed.GridParent import GridParent
from CartesianGridBase import CartesianGridBase
GRID_Z_OFFSET = 0.0

class DistributedCartesianGrid(DistributedNode, CartesianGridBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedCartesianGrid')
    notify.setDebug(0)
    VisualizeGrid = config.GetBool('visualize-cartesian-grid', 0)
    RuleSeparator = ':'

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        self.visAvatar = None
        self.gridVisContext = None
        self._onOffState = False
        return

    def generate(self):
        DistributedNode.generate(self)

    def disable(self):
        DistributedNode.disable(self)
        self.stopProcessVisibility()

    def delete(self):
        DistributedNode.delete(self)
        taskMgr.remove(self.taskName('processVisibility'))

    def isGridParent(self):
        return 1

    def setCellWidth(self, width):
        self.cellWidth = width

    def setParentingRules(self, style, rule):
        rules = rule.split(self.RuleSeparator)
        self.style = style
        self.startingZone = int(rules[0])
        self.gridSize = int(rules[1])
        self.viewingRadius = int(rules[2])
        cx = self.cellWidth * self.gridSize / 2.0
        self.centerPos = Vec3(cx, cx, 0)

    def getCenterPos(self):
        return self.centerPos

    def handleChildArrive(self, child, zoneId):
        DistributedNode.handleChildArrive(self, child, zoneId)
        if zoneId >= self.startingZone:
            if not child.gridParent:
                child.gridParent = GridParent(child)
            child.gridParent.setGridParent(self, zoneId)
        elif child.gridParent:
            child.gridParent.delete()
            child.gridParent = None
        return

    def handleChildArriveZone(self, child, zoneId):
        DistributedNode.handleChildArrive(self, child, zoneId)
        if zoneId >= self.startingZone:
            if not child.gridParent:
                child.gridParent = GridParent(child)
            child.gridParent.setGridParent(self, zoneId)
        elif child.gridParent:
            child.gridParent.delete()
            child.gridParent = None
        return

    def handleChildLeave(self, child, zoneId):
        if child.gridParent:
            child.gridParent.delete()
            child.gridParent = None
        return

    @report(types=['deltaStamp', 'avLocation', 'args'], dConfigParam=['connector', 'shipboard'])
    def startProcessVisibility(self, avatar):
        if not self._onOffState:
            return
        if self.cr.noNewInterests():
            self.notify.warning('startProcessVisibility(%s): tried to open a new interest during logout' % self.doId)
            return
        taskMgr.remove(self.taskName('processVisibility'))
        self.acceptOnce(self.cr.StopVisibilityEvent, self.stopProcessVisibility)
        self.visAvatar = avatar
        self.visZone = None
        self.visDirty = True
        taskMgr.add(self.processVisibility, self.taskName('processVisibility'))
        self.processVisibility(0)
        return

    @report(types=['deltaStamp', 'avLocation', 'args'], dConfigParam=['connector', 'shipboard'])
    def stopProcessVisibility(self, clearAll = False, event = None):
        self.ignore(self.cr.StopVisibilityEvent)
        taskMgr.remove(self.taskName('processVisibility'))
        if event is not None:
            eventGroup = EventGroup('DistCartesianGrid.stopProcessVis', doneEvent=event)
        if self.gridVisContext is not None:
            if event is not None:
                removeEvent = eventGroup.newEvent('%s.removeInterest' % self.doId)
            else:
                removeEvent = None
            self.cr.removeInterest(self.gridVisContext, removeEvent)
            self.gridVisContext = None
        elif event is not None:
            messenger.send(event)
        self.visAvatar = None
        self.visZone = None
        if clearAll:
            if event is not None:
                parentEvent = eventGroup.newEvent('%s.parent.removeInterest' % self.doId)
            else:
                parentEvent = None
            if hasattr(self.cr.doId2do[self.parentId], 'worldGrid'):
                self.cr.doId2do[self.parentId].worldGrid.stopProcessVisibility(event=parentEvent)
        return

    def processVisibility(self, task):
        if self.visAvatar == None:
            return Task.done
        if self.visAvatar.isDisabled():
            self.visAvatar = None
            return Task.done
        if self.visAvatar.gameFSM.state == 'Cutscene':
            return Task.cont
        pos = self.visAvatar.getPos(self)
        dx = self.cellWidth * self.gridSize * 0.5
        x = pos[0] + dx
        y = pos[1] + dx
        col = x // self.cellWidth
        row = y // self.cellWidth
        if row < 0 or col < 0 or row > self.gridSize or col > self.gridSize:
            if self.gridVisContext:
                self.cr.removeInterest(self.gridVisContext)
                self.visZone = None
                self.gridVisContext = None
            return Task.cont
        zoneId = int(self.startingZone + (row * self.gridSize + col))
        if zoneId == self.visZone:
            if self.visDirty:
                messenger.send(self.uniqueName('visibility'))
                self.visDirty = False
            return Task.cont
        else:
            self.visZone = zoneId
            if not self.gridVisContext:
                self.gridVisContext = self.cr.addInterest(self.getDoId(), self.visZone, self.uniqueName('visibility'), event=self.uniqueName('visibility'))
            else:
                event = None
                if self.visDirty:
                    event = self.uniqueName('visibility')
                self.cr.alterInterest(self.gridVisContext, self.getDoId(), self.visZone, event=event)
                parentId = self.visAvatar.parentId
                oldZoneId = self.visAvatar.zoneId
                if parentId == self.doId:
                    messenger.send('avatarZoneChanged', [self.visAvatar, self.doId, zoneId])
            self.visDirty = False
            return Task.cont
        return

    def addObjectToGrid(self, av):
        pos = av.getPos(self)
        zoneId = self.getZoneFromXYZ(pos)
        messenger.send('avatarZoneChanged', [av, self.doId, zoneId])

    def removeObjectFromGrid(self, av):
        if av.getParent().compareTo(self) == 0:
            av.detachNode()

    def handleAvatarZoneChange(self, av, zoneId):
        if not self.isValidZone(zoneId):
            return
        av.b_setLocation(self.doId, zoneId)

    def turnOff(self):
        self._onOffState = False
        self.stopProcessVisibility()

    def turnOn(self, av = None):
        self._onOffState = True
        if av:
            self.startProcessVisibility(av)

    def setWorldContext(self, worldContext):
        pass

    def clearWorldContext(self, event = None):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedCartesianGrid.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:02 Pacific Daylight Time
