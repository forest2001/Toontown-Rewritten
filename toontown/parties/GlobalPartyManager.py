from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.distributed.PyDatagram import *
from direct.directnotify.DirectNotifyGlobal import directNotify

class GlobalPartyManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('GlobalPartyManager')