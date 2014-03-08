from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.election.DistributedElectionCameraAI import DistributedElectionCameraAI
from otp.ai.MagicWordGlobal import *

class DistributedElectionCameraManagerAI(DistributedObjectAI):
    def __init__(self, air):
    
        DistributedObjectAI.__init__(self, air)
        self.air.cameraManager = self
        
        self.mainCamera = 0
        
    def getMainCamera(self):
        return self.mainCamera
        
    def d_setMainCamera(self, cam):
        self.sendUpdate('setMainCamera', [cam])
        
    def b_setMainCamera(self, cam):
        self.setMainCamera(cam)
        self.d_setMainCamera(self, cam)
        
    def setMainCamera(self, cam):
        self.mainCamera = cam
        
@magicWord()
def createManager():
    if not hasattr(simbase.air, 'cameraManager'):
        camera = DistributedElectionCameraAI(simbase.air)
        camera.generateWithRequired(2000)
        camera.b_setPosHpr(-16, 1, 5, 0, 0, 0)
        manager = DistributedElectionCameraManagerAI(simbase.air)
        manager.setMainCamera(camera.doId)
        manager.generateWithRequired(2000)