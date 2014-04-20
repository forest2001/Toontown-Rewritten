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
        self.tvOn = True

    def generate(self):
        DistributedObject.generate(self)

        # Load the TV, and give it a nice idle animation.
        # This will probably be moved somewhere else once we get it into the scripted sequence
        self.tv = loader.loadModel('phase_4/models/events/election_tv')
        self.tv.reparentTo(render)
        self.tv.setPosHprScale(87.85, -0.25, 40.0, 270.0, 0.0, 0.0, 1.5, 1.5, 1.5)
        self.tv.hide()

        self.tvIdle = Sequence(
            self.tv.posInterval(2.5, (87.85, -0.25, 22.0), blendType='easeInOut'),
            self.tv.posInterval(2.5, (87.85, -0.25, 21.0), blendType='easeInOut'),
        )
        self.tvFlyIn = Sequence(
            Func(self.tv.show),
            Func(self.tv.setTransparency, 1),
            Parallel(self.tv.colorScaleInterval(1, colorScale=VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0)), self.tv.posInterval(4, (87.85, -0.25, 20.0), blendType='easeInOut')),
            Func(self.tv.setTransparency, 0),
            self.tv.posInterval(2, (87.85, -0.25, 21.0)),
            Func(self.tvIdle.loop)
        )

        # Attach a cog's propeller onto the TV. Foreshadowing!
        self.prop = BattleProps.globalPropPool.getProp('propeller')
        propJoint = self.tv.find('**/topSphere')
        self.prop.reparentTo(propJoint)
        self.prop.loop('propeller', fromFrame=0, toFrame=8)
        self.prop.setPos(0, 1, 2)
        self.prop.setScale(2.0, 1.5, 1.0)

        self.buffer = base.win.makeTextureBuffer("tv", 512, 256)
        self.buffer.setSort(-100)
        self.camera = base.makeCamera(self.buffer)
        self.camera.reparentTo(render)
                
        ts = self.tv.find('**/screen').findTextureStage('*')
        self.tv.find('**/screen').setTexture(ts, self.buffer.getTexture(), 1)
        self.tv.find('**/screen').setTexScale(ts, 1.2, 1.2)
        self.tv.find('**/screen').setTexOffset(ts, -0.09, -0.1)
        self.tv.find('**/screen').setTexHpr(ts, 1, 0, 0)
                
    def disable(self):
        if self.tvOn:
            base.graphicsEngine.removeWindow(self.buffer)
        self.camera.removeNode()
        self.prop.cleanup()
        self.prop.removeNode()
        self.tv.removeNode()

    def setMainCamera(self, new):
        if self.mainCam != 0 and self.cameraViewEnabled:
            self.cr.doId2do[self.mainCam].camera.show()
        self.mainCam = new
        if self.mainCam != 0:
            if new in self.cr.doId2do:
                self.camera.reparentTo(self.cr.doId2do[new])
                if self.cameraViewEnabled:
                    self.cr.doId2do[new].camera.hide()
            else:
                self.acceptOnce('generate-%d' % new, self.setCam)
            
    def setCam(self, cam):
        self.camera.reparentTo(cam)
        if self.cameraViewEnabled:
            cam.camera.hide()
        
    def setCameraIds(self, ids):
        self.cameraIds = ids
        
    def disableScreen(self):
        if self.tvOn:
            #gg hacks
            self.tvOn = False
            tex = loader.loadTexture("phase_4/maps/tv_standby.jpg")
            ts = self.tv.find('**/screen').findTextureStage('*')
            self.tv.find('**/screen').setTexture(ts, tex, 1)
            self.tv.find('**/screen').setTexScale(ts, 1.2, 1.2)
            self.tv.find('**/screen').setTexOffset(ts, -0.09, -0.1)
            self.tv.find('**/screen').setTexHpr(ts, 1, 0, 0)
            parent = self.camera.getParent()
            self.camera.removeNode()
            self.camera = parent.attachNewNode('ECMNode')
            base.graphicsEngine.removeWindow(self.buffer)
            if self.cameraViewEnabled:
                base.camera.reparentTo(self.camera)
        
    def _toggleCameraView(self):
        base.localAvatar.stopUpdateSmartCamera()
        base.camera.setPosHpr(0,0,0,0,0,0)
        base.camera.reparentTo(self.camera)
        self.cameraViewEnabled = True
        if self.mainCam != 0:
            self.cr.doId2do[self.mainCam].camera.hide()
@magicWord(category=CATEGORY_CAMERA)
def cameraView():
    if not hasattr(base.cr, 'cameraManager'):
       return 'No Camera Manager.'
    base.cr.cameraManager._toggleCameraView()
