from direct.distributed.DistributedObject import DistributedObject
#lel copy+pasted imports
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.task import Task


class DistributedElectionCameraManager(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.cameraManager = self
        self.mainCam = 0
        
    def generate(self):
        DistributedObject.generate(self)
        self.tv = loader.loadModel('phase_4/models/events/tv')
        self.tv.reparentTo(render)
        self.tv.setPosHpr(-16, 1, 5, 0, 0, 0)
        self.buffer = base.win.makeTextureBuffer("tv", 512, 256)
        self.buffer.setSort(-100)
        self.camera = base.makeCamera(self.buffer)
        self.camera.reparentTo(render)
        
        self.tv.find('**/screen').setTexture(self.buffer.getTexture(), 1)
        taskMgr.add(cameraTask, 'DistributedECM RTT')
        
    def disable(self):
        self.tv.removeNode()
        self.screen = None
        
    def setMainCamera(self, new):
        self.mainCam = new
        
def cameraTask(task):
    dCamera = base.cr.doId2do.get(base.cr.cameraManager.mainCam)
    if not dCamera:
        return task.again
    base.cr.cameraManager.camera.setPos(dCamera.getX(), dCamera.getY(), dCamera.getZ())
    return task.again