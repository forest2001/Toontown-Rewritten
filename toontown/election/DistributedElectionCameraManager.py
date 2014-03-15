from direct.distributed.DistributedObject import DistributedObject
#lel copy+pasted imports
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from otp.ai.MagicWordGlobal import *
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps
from direct.task import Task


class DistributedElectionCameraManager(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.cameraManager = self
        self.mainCam = 0
        self.cameraIds = []
        self.cameraViewEnabled = False
    def generate(self):
        DistributedObject.generate(self)

        # Load the TV, and give it a nice idle animation.
        # This will probably be moved somewhere else once we get it into the scripted sequence
        self.tv = loader.loadModel('phase_4/models/events/tv')
        self.tv.reparentTo(render)
        self.tv.setPosHprScale(87.85, -0.25, 21.0, 270.0, 0.0, 0.0, 1.5, 1.5, 1.5)
        self.tvIdle = Sequence(
            self.tv.posInterval(2.5, (87.85, -0.25, 22.0), blendType='easeInOut'),
            self.tv.posInterval(2.5, (87.85, -0.25, 21.0), blendType='easeInOut'),
        )
        self.tvIdle.loop()

        # Attach a cog's propeller onto the TV. Foreshadowing!
        self.prop = BattleProps.globalPropPool.getProp('propeller')
        propJoint = self.tv.find('**/topSphere')
        self.prop.reparentTo(propJoint)
        self.prop.loop('propeller', fromFrame=0, toFrame=8)
        self.prop.setZ(1.5)
        self.prop.setScale(2.0, 1.5, 1.0)

        self.buffer = base.win.makeTextureBuffer("tv", 512, 256)
        self.buffer.setSort(-100)
        self.camera = base.makeCamera(self.buffer)
        self.camera.reparentTo(render)
                
        ts = self.tv.find('**/screen').findTextureStage('*')
        self.tv.find('**/screen').setTexture(ts, self.buffer.getTexture(), 1)
                
    def disable(self):
        self.tv.removeNode()
        self.screen = None
        
    def setMainCamera(self, new):
        self.mainCam = new
        if self.mainCam != 0:
            if new in self.cr.doId2do:
                self.camera.reparentTo(self.cr.doId2do[new])
                if self.cameraViewEnabled:
                    camNP = NodePath(self.winCam)
                    camNP.reparentTo(self.cr.doId2do[new])
            else:
                self.acceptOnce('generate-%d' % new, self.setCam)
            
    def setCam(self, cam):
        self.camera.reparentTo(cam)
        
    def setCameraIds(self, ids):
        self.cameraIds = ids
        
    def _toggleCameraView(self):
        self.winCam = Camera('cam')
        camNP = NodePath(self.winCam)
        camNP.reparentTo(self.cr.doId2do[self.mainCam])
        base.win.getActiveDisplayRegion(0).setCamera(camNP)
        self.cameraViewEnabled = True
        
@magicWord(category=CATEGORY_CAMERA)
def cameraView():
    if not hasattr(base.cr, 'cameraManager'):
       return 'No Camera Manager.'
    base.cr.cameraManager._toggleCameraView()
