# 2013.08.22 22:18:34 Pacific Daylight Time
# Embedded file name: toontown.coghq.DistributedElevatorMarker
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from StomperGlobals import *
from direct.distributed import ClockDelta
from direct.showbase.PythonUtil import lerp
import math
from otp.level import DistributedEntity
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from otp.level import BasicEntities
from direct.task import Task
from toontown.toonbase import ToontownGlobals

class DistributedElevatorMarker(BasicEntities.DistributedNodePathEntity):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElevatorMarker')
    elevatorMarkerModels = ['phase_9/models/cogHQ/square_stomper']

    def __init__(self, cr):
        BasicEntities.DistributedNodePathEntity.__init__(self, cr)

    def generateInit(self):
        self.notify.debug('generateInit')
        BasicEntities.DistributedNodePathEntity.generateInit(self)

    def generate(self):
        self.notify.debug('generate')
        BasicEntities.DistributedNodePathEntity.generate(self)

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)
        self.loadModel()

    def disable(self):
        self.notify.debug('disable')
        self.ignoreAll()
        DistributedEntity.DistributedEntity.disable(self)

    def delete(self):
        self.notify.debug('delete')
        self.unloadModel()
        BasicEntities.DistributedNodePathEntity.delete(self)

    def loadModel(self):
        self.rotateNode = self.attachNewNode('rotate')
        self.model = None
        if __dev__:
            self.model = loader.loadModel(self.elevatorMarkerModels[self.modelPath])
            self.model.reparentTo(self.rotateNode)
        return

    def unloadModel(self):
        if self.model:
            self.model.removeNode()
            del self.model
            self.model = None
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\DistributedElevatorMarker.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:34 Pacific Daylight Time
