from direct.distributed.DistributedObject import DistributedObject

class DistributedAprilToonsMgr(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
