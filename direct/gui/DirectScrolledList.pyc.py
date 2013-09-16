# 2013.08.22 22:14:18 Pacific Daylight Time
# Embedded file name: direct.gui.DirectScrolledList
__all__ = ['DirectScrolledListItem', 'DirectScrolledList']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from direct.directnotify import DirectNotifyGlobal
from direct.task.Task import Task
from DirectFrame import *
from DirectButton import *
import string, types

class DirectScrolledListItem(DirectButton):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DirectScrolledListItem')

    def __init__(self, parent = None, **kw):
        self.parent = parent
        if kw.has_key('command'):
            self.nextCommand = kw.get('command')
            del kw['command']
        if kw.has_key('extraArgs'):
            self.nextCommandExtraArgs = kw.get('extraArgs')
            del kw['extraArgs']
        optiondefs = (('parent', self.parent, None), ('command', self.select, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self)
        self.initialiseoptions(DirectScrolledListItem)
        return

    def select(self):
        apply(self.nextCommand, self.nextCommandExtraArgs)
        self.parent.selectListItem(self)


class DirectScrolledList(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DirectScrolledList')

    def __init__(self, parent = None, **kw):
        self.index = 0
        self.forceHeight = None
        if kw.has_key('items'):
            for item in kw['items']:
                if type(item) != type(''):
                    break
            else:
                kw['items'] = kw['items'][:]

        self.nextItemID = 10
        optiondefs = (('items', [], None),
         ('itemsAlign', TextNode.ACenter, DGG.INITOPT),
         ('itemsWordwrap', None, DGG.INITOPT),
         ('command', None, None),
         ('extraArgs', [], None),
         ('itemMakeFunction', None, None),
         ('itemMakeExtraArgs', [], None),
         ('numItemsVisible', 1, self.setNumItemsVisible),
         ('scrollSpeed', 8, self.setScrollSpeed),
         ('forceHeight', None, self.setForceHeight),
         ('incButtonCallback', None, self.setIncButtonCallback),
         ('decButtonCallback', None, self.setDecButtonCallback))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.incButton = self.createcomponent('incButton', (), None, DirectButton, (self,))
        self.incButton.bind(DGG.B1PRESS, self.__incButtonDown)
        self.incButton.bind(DGG.B1RELEASE, self.__buttonUp)
        self.decButton = self.createcomponent('decButton', (), None, DirectButton, (self,))
        self.decButton.bind(DGG.B1PRESS, self.__decButtonDown)
        self.decButton.bind(DGG.B1RELEASE, self.__buttonUp)
        self.itemFrame = self.createcomponent('itemFrame', (), None, DirectFrame, (self,))
        for item in self['items']:
            if item.__class__.__name__ != 'str':
                item.reparentTo(self.itemFrame)

        self.initialiseoptions(DirectScrolledList)
        self.recordMaxHeight()
        self.scrollTo(0)
        return

    def setForceHeight(self):
        self.forceHeight = self['forceHeight']

    def recordMaxHeight(self):
        if self.forceHeight is not None:
            self.maxHeight = self.forceHeight
        else:
            self.maxHeight = 0.0
            for item in self['items']:
                if item.__class__.__name__ != 'str':
                    self.maxHeight = max(self.maxHeight, item.getHeight())

        return

    def setScrollSpeed(self):
        self.scrollSpeed = self['scrollSpeed']
        if self.scrollSpeed <= 0:
            self.scrollSpeed = 1

    def setNumItemsVisible(self):
        self.numItemsVisible = self['numItemsVisible']

    def destroy(self):
        taskMgr.remove(self.taskName('scroll'))
        if hasattr(self, 'currentSelected'):
            del self.currentSelected
        if self.incButtonCallback:
            self.incButtonCallback = None
        if self.decButtonCallback:
            self.decButtonCallback = None
        self.incButton.destroy()
        self.decButton.destroy()
        DirectFrame.destroy(self)
        return

    def selectListItem(self, item):
        if hasattr(self, 'currentSelected'):
            self.currentSelected['state'] = DGG.NORMAL
        item['state'] = DGG.DISABLED
        self.currentSelected = item

    def scrollBy(self, delta):
        return self.scrollTo(self.index + delta)

    def getItemIndexForItemID(self, itemID):
        if len(self['items']) == 0:
            return 0
        if type(self['items'][0]) != types.InstanceType:
            self.notify.warning('getItemIndexForItemID: cant find itemID for non-class list items!')
            return 0
        for i in range(len(self['items'])):
            if self['items'][i].itemID == itemID:
                return i

        self.notify.warning('getItemIndexForItemID: item not found!')
        return 0

    def scrollToItemID(self, itemID, centered = 0):
        self.scrollTo(self.getItemIndexForItemID(itemID), centered)

    def scrollTo(self, index, centered = 0):
        try:
            self['numItemsVisible']
        except:
            self.notify.info('crash 27633 fixed!')
            return

        numItemsVisible = self['numItemsVisible']
        numItemsTotal = len(self['items'])
        if centered:
            self.index = index - numItemsVisible / 2
        else:
            self.index = index
        if len(self['items']) <= numItemsVisible:
            self.incButton['state'] = DGG.DISABLED
            self.decButton['state'] = DGG.DISABLED
            self.index = 0
            ret = 0
        elif self.index <= 0:
            self.index = 0
            self.decButton['state'] = DGG.DISABLED
            self.incButton['state'] = DGG.NORMAL
            ret = 0
        elif self.index >= numItemsTotal - numItemsVisible:
            self.index = numItemsTotal - numItemsVisible
            self.incButton['state'] = DGG.DISABLED
            self.decButton['state'] = DGG.NORMAL
            ret = 0
        else:
            if self.incButton['state'] == DGG.DISABLED or self.decButton['state'] == DGG.DISABLED:
                self.__buttonUp(0)
            self.incButton['state'] = DGG.NORMAL
            self.decButton['state'] = DGG.NORMAL
            ret = 1
        for item in self['items']:
            if item.__class__.__name__ != 'str':
                item.hide()

        upperRange = min(numItemsTotal, numItemsVisible)
        for i in range(self.index, self.index + upperRange):
            item = self['items'][i]
            if item.__class__.__name__ == 'str':
                if self['itemMakeFunction']:
                    item = apply(self['itemMakeFunction'], (item, i, self['itemMakeExtraArgs']))
                else:
                    item = DirectFrame(text=item, text_align=self['itemsAlign'], text_wordwrap=self['itemsWordwrap'], relief=None)
                self['items'][i] = item
                item.reparentTo(self.itemFrame)
                self.recordMaxHeight()
            item.show()
            item.setPos(0, 0, -(i - self.index) * self.maxHeight)

        if self['command']:
            apply(self['command'], self['extraArgs'])
        return ret

    def makeAllItems(self):
        for i in range(len(self['items'])):
            item = self['items'][i]
            if item.__class__.__name__ == 'str':
                if self['itemMakeFunction']:
                    item = apply(self['itemMakeFunction'], (item, i, self['itemMakeExtraArgs']))
                else:
                    item = DirectFrame(text=item, text_align=self['itemsAlign'], text_wordwrap=self['itemsWordwrap'], relief=None)
                self['items'][i] = item
                item.reparentTo(self.itemFrame)

        self.recordMaxHeight()
        return

    def __scrollByTask(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        else:
            ret = self.scrollBy(task.delta)
            task.prevTime = task.time
            if ret:
                return Task.cont
            else:
                return Task.done

    def __incButtonDown(self, event):
        task = Task(self.__scrollByTask)
        task.setDelay(1.0 / self.scrollSpeed)
        task.prevTime = 0.0
        task.delta = 1
        taskName = self.taskName('scroll')
        taskMgr.add(task, taskName)
        self.scrollBy(task.delta)
        messenger.send('wakeup')
        if self.incButtonCallback:
            self.incButtonCallback()

    def __decButtonDown(self, event):
        task = Task(self.__scrollByTask)
        task.setDelay(1.0 / self.scrollSpeed)
        task.prevTime = 0.0
        task.delta = -1
        taskName = self.taskName('scroll')
        taskMgr.add(task, taskName)
        self.scrollBy(task.delta)
        messenger.send('wakeup')
        if self.decButtonCallback:
            self.decButtonCallback()

    def __buttonUp(self, event):
        taskName = self.taskName('scroll')
        taskMgr.remove(taskName)

    def addItem(self, item, refresh = 1):
        if type(item) == types.InstanceType:
            item.itemID = self.nextItemID
            self.nextItemID += 1
        self['items'].append(item)
        if type(item) != type(''):
            item.reparentTo(self.itemFrame)
        if refresh:
            self.refresh()
        if type(item) == types.InstanceType:
            return item.itemID

    def removeItem(self, item, refresh = 1):
        if item in self['items']:
            if hasattr(self, 'currentSelected') and self.currentSelected is item:
                del self.currentSelected
            self['items'].remove(item)
            if type(item) != type(''):
                item.reparentTo(hidden)
            self.refresh()
            return 1
        else:
            return 0

    def removeAndDestroyItem(self, item, refresh = 1):
        if item in self['items']:
            if hasattr(self, 'currentSelected') and self.currentSelected is item:
                del self.currentSelected
            if hasattr(item, 'destroy') and hasattr(item.destroy, '__call__'):
                item.destroy()
            self['items'].remove(item)
            if type(item) != type(''):
                item.reparentTo(hidden)
            self.refresh()
            return 1
        else:
            return 0

    def removeAllItems(self, refresh = 1):
        retval = 0
        while len(self['items']):
            item = self['items'][0]
            if hasattr(self, 'currentSelected') and self.currentSelected is item:
                del self.currentSelected
            self['items'].remove(item)
            if type(item) != type(''):
                item.removeNode()
            retval = 1

        if refresh:
            self.refresh()
        return retval

    def removeAndDestroyAllItems(self, refresh = 1):
        retval = 0
        while len(self['items']):
            item = self['items'][0]
            if hasattr(self, 'currentSelected') and self.currentSelected is item:
                del self.currentSelected
            if hasattr(item, 'destroy') and hasattr(item.destroy, '__call__'):
                item.destroy()
            self['items'].remove(item)
            if type(item) != type(''):
                item.removeNode()
            retval = 1

        if refresh:
            self.refresh()
        return retval

    def refresh(self):
        self.recordMaxHeight()
        self.scrollTo(self.index)

    def getSelectedIndex(self):
        return self.index

    def getSelectedText(self):
        if self['items'][self.index].__class__.__name__ == 'str':
            return self['items'][self.index]
        else:
            return self['items'][self.index]['text']

    def setIncButtonCallback(self):
        self.incButtonCallback = self['incButtonCallback']

    def setDecButtonCallback(self):
        self.decButtonCallback = self['decButtonCallback']
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectScrolledList.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:18 Pacific Daylight Time
