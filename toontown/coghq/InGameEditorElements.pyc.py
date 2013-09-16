# 2013.08.22 22:19:06 Pacific Daylight Time
# Embedded file name: toontown.coghq.InGameEditorElements
from direct.showbase import DirectObject

class InGameEditorElement(DirectObject.DirectObject):
    __module__ = __name__
    elementId = 0

    def __init__(self, children = []):
        self.elementId = InGameEditorElement.elementId
        InGameEditorElement.elementId += 1
        self.setChildren(children)
        self.feName = self.getTypeName()

    def getName(self):
        return self.feName

    def setNewName(self, newName):
        self.feName = newName

    def getTypeName(self):
        return 'Level Element'

    def id(self):
        return self.elementId

    def getChildren(self):
        return self.children

    def setChildren(self, children):
        self.children = list(children)

    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, child):
        self.children.remove(child)

    def getNumChildren(self):
        return len(self.children)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\InGameEditorElements.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:06 Pacific Daylight Time
