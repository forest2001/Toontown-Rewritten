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
        self.cameraIds = []
        
    def generate(self):
        DistributedObject.generate(self)
        self.tv = loader.loadModel('phase_4/models/events/tv')
        self.tv.reparentTo(render)
        self.tv.setPosHpr(-16, 1, 5, 180, 0, 0)
        self.buffer = base.win.makeTextureBuffer("tv", 512, 256)
        self.buffer.setSort(-100)
        self.camera = base.makeCamera(self.buffer)
        self.camera.reparentTo(render)
                
        ts = self.tv.find('**/screen').findTextureStage('*')
        self.tv.find('**/screen').setTexture(ts, self.buffer.getTexture(), 1)
        taskMgr.add(cameraTask, 'DistributedECM RTT')
                
    def disable(self):
        self.tv.removeNode()
        self.screen = None
        
    def setMainCamera(self, new):
        self.mainCam = new
        
    def setCameraIds(self, ids):
        self.cameraIds = ids
                
def cameraTask(task):
    dCamera = base.cr.doId2do.get(base.cr.cameraManager.mainCam)
    if not dCamera:
        return task.again
    base.cr.cameraManager.camera.reparentTo(dCamera)
    return task.again