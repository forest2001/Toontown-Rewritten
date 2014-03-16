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

@magicWord(category=CATEGORY_CAMERA, types=[str, str])
def cameras(cmd, args=''):
    if not hasattr(simbase.air, 'cameraManager') and cmd != 'spawn':
        return "There is no Camera Manager!"
    
    if cmd == 'spawn':
        if hasattr(simbase.air, 'cameraManager'):
            return "A Camera Manager already exists!"
        cameras = []
        for cameraId in range(5):
            cam = DistributedElectionCameraAI(simbase.air)
            cam.setState('Waiting', globalClockDelta.getRealNetworkTime(), 0, 0, 0, 0, 0, 0)
            cam.generateWithRequired(2000)
            cam.b_setPosHpr(0, 0, 0, 0, 0, 0)
            cameras.append(cam.getDoId())
        camMgr = DistributedElectionCameraManagerAI(simbase.air)
        camMgr.setMainCamera(cameras[0])
        camMgr.setCameraIds(cameras)
        camMgr.generateWithRequired(2000)
        return "Camera Manager has been spawned successfully."
    
    args = args.split()
    camMgr = simbase.air.cameraManager
	
    if cmd == 'move':
        # A bunch of sanity checks...
        if len(args) < 2:
            return "You haven't specified enough parameters!"
        camId = int(args[0])
        if not 0 <= camId <= len(camMgr.ids):
            return "Invalid Camera ID specified."
        cam = simbase.air.doId2do.get(camMgr.ids[camId], None)
        if not cam:
            return "Could not locate camera in the AIR doId2do table."
        # Lets move the camera somewhere...
        if args[1] == 'here':
            av = spellbook.getTarget()
            cam._moveTo(av.getX(), av.getY(), av.getZ() + 3.0, av.getH(), 0)
            return "Camera %d is moving to %s." % (camId, av.getName())
        if args[1] == 'to':
            # This is fun...
            if len(args) < 7:
                return "You haven't specified enough position parameters! (x, y, z, h, p)"
            cam._moveTo(float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]))
            return "Camera %d is moving to the specified location." % camId
        return "Invalid arguments for 'move' specified. (to, here valid)"
        
    if cmd == 'follow':
        if len(args) < 2:
            return "You haven't specified enough parameters!"
        camId = int(args[0])
        if not 0 <= camId <= len(camMgr.ids):
            return "Invalid Camera ID specified."
        cam = simbase.air.doId2do.get(camMgr.ids[camId], None)
        if not cam:
            return "Could not locate camera in the AIR doId2do table."
        if args[1] == 'behind':
            cam._followBehind(spellbook.getTarget())
            return "Camera %d is now stalking target from behind." % camId
        elif args[1] == 'front':
            cam._watch(spellbook.getTarget())
            return "Camera %d is now stalking target from the front." % camId
        return "Invalid arguments for 'follow' specified. (behind, front)"
        
    if cmd == 'setmain':
        camId = int(args[0])
        if not 0 <= camId <= len(camMgr.ids):
            return "Invalid Camera ID specified."
        camMgr.b_setMainCamera(camMgr.ids[camId])
        return 'Camera %d is now main camera.' % camId
    return 'That command doesn\'t exist. (try setmain, follow, or move)'
