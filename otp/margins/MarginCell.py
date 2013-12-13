from pandac.PandaModules import *

class MarginCell(NodePath):
    def __init__(self, manager):
        NodePath.__init__(self, 'cell')

        self.manager = manager

        self.content = None
        self.available = False

        self.debugSquare = None
        self.debugMode = False

        self.setDebug(base.config.GetBool('want-cell-debug', False))

    def setAvailable(self, available):
        if not available and self.hasContent():
            self.setContent(None)

        self.available = available

        self.updateDebug()

    def setContent(self, content):
        if self.content:
            self.content._assignedCell = None
            self.contentNP.removeNode()

        if content:
            content._assignedCell = self
            content._lastCell = self
            self.contentNP = self.attachNewNode(content)

        self.content = content

        self.updateDebug()

    def hasContent(self):
        return self.content is not None

    def getContent(self):
        return self.content

    def isAvailable(self):
        return self.available

    def isFree(self):
        return self.isAvailable() and not self.hasContent()

    def setDebugColor(self, color):
        if not self.debugSquare:
            cm = CardMaker('debugSquare')
            cm.setFrameFullscreenQuad()
            self.debugSquare = self.attachNewNode(cm.generate())
            self.debugSquare.setTransparency(1)
            self.debugSquare.setY(1)

        self.debugSquare.setColor(color)

    def updateDebug(self):
        if not self.debugMode: return

        if self.hasContent():
            self.setDebugColor(VBase4(0.0, 0.8, 0.0, 0.5))
        elif self.isAvailable():
            self.setDebugColor(VBase4(0.0, 0.0, 0.8, 0.5))
        else:
            self.setDebugColor(VBase4(0.8, 0.0, 0.0, 0.5))

    def setDebug(self, status):
        if bool(status) == self.debugMode:
            return

        self.debugMode = status

        if self.debugMode:
            self.updateDebug()
        elif self.debugSquare:
            self.debugSquare.removeNode()
            self.debugSquare = None
