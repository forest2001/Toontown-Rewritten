from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.election.DistributedElectionCameraAI import DistributedElectionCameraAI
from direct.distributed.ClockDelta import *
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
        self.d_setMainCamera(cam)
        
    def setMainCamera(self, cam):
        self.mainCamera = cam
    
    def getCameraIds(self):
        return self.ids
    
    def setCameraIds(self, ids):
        self.ids = ids
        
    def d_setCameraIds(self, ids):
        self.sendUpdate('setCameraIds', [ids])
        
    def b_setCameraIds(self, ids):
        self.setCameraIds(ids)
        self.d_setCameraIds(ids)
        
@magicWord()
def spawnCameras(category=CATEGORY_CAMERA):
    if not hasattr(simbase.air, 'cameraManager'):
        cameras = []
        for i in range(5):
            camera = DistributedElectionCameraAI(simbase.air)
            camera.setState('Waiting', globalClockDelta.getRealNetworkTime(), 0, 0, 0, 0, 0, 0)
            camera.generateWithRequired(2000)
            camera.b_setPosHpr(0, 0, 0, 0, 0, 0)
            cameras.append(camera.getDoId())
        manager = DistributedElectionCameraManagerAI(simbase.air)
        manager.setMainCamera(cameras[0])
        manager.setCameraIds(cameras)
        manager.generateWithRequired(2000)
        return 'Created ElectionCameraManager and 5 cameras.'
    return 'There are already cameras.'
        
@magicWord(types=[int], category=CATEGORY_CAMERA)
def camComeHere(id):
    if not hasattr(simbase.air, 'cameraManager'):
        return 'Create some cameras with spawnCameras first.'
    if id >= len(simbase.air.cameraManager.ids) or id < 0:
        return 'Invalid camera number.'
    cam = simbase.air.doId2do[simbase.air.cameraManager.ids[id]]
    av = spellbook.getTarget()
    cam._moveTo(av.getX(), av.getY(), av.getZ() + 3.0, av.getH(), 0)
    return 'Camera %d is moving to %s.' % (id, av.getName())
    
@magicWord(types=[int, float, float, float, float, float], category=CATEGORY_CAMERA)
def camGoTo(id, x, y, z, h, p):
    if not hasattr(simbase.air, 'cameraManager'):
        return 'Create some cameras with spawnCameras first.'
    if id >= len(simbase.air.cameraManager.ids) or id < 0:
        return 'Invalid camera number.'
    cam = simbase.air.doId2do[simbase.air.cameraManager.ids[id]]
    cam.__moveTo(x, y, z, h, p)
    return 'Camera moving to point.'
    
@magicWord(types=[int], category=CATEGORY_CAMERA)
def camFollowBehind(id):
    if not hasattr(simbase.air, 'cameraManager'):
        return 'Create some cameras with spawnCameras first.'
    if id >= len(simbase.air.cameraManager.ids) or id < 0:
        return 'Invalid camera number.'
    cam = simbase.air.doId2do[simbase.air.cameraManager.ids[id]]
    cam._followBehind(spellbook.getTarget())
    return 'Camera now in follow mode.'

@magicWord(types=[int], category=CATEGORY_CAMERA)
def camFollowFront(id):
    if not hasattr(simbase.air, 'cameraManager'):
        return 'Create some cameras with spawnCameras first.'
    if id >= len(simbase.air.cameraManager.ids) or id < 0:
        return 'Invalid camera number.'
    cam = simbase.air.doId2do[simbase.air.cameraManager.ids[id]]
    cam._watch(spellbook.getTarget())
    return 'Camera now in follow mode.'

    
@magicWord(types=[int], category=CATEGORY_CAMERA)
def setMainCam(id):
    if not hasattr(simbase.air, 'cameraManager'):
        return 'Create some cameras with spawnCameras first.'
    if id >= len(simbase.air.cameraManager.ids) or id < 0:
        return 'Invalid camera number.'
    simbase.air.cameraManager.b_setMainCamera(simbase.air.cameraManager.ids[id])
    return 'Camera %d is now main camera.' % id