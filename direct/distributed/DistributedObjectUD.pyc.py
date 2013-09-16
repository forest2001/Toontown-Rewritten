# 2013.08.22 22:14:05 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectBase import DistributedObjectBase
from direct.showbase import PythonUtil
from pandac.PandaModules import *

class DistributedObjectUD(DistributedObjectBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObjectUD')
    QuietZone = 1

    def __init__(self, air):
        try:
            self.DistributedObjectUD_initialized
        except:
            self.DistributedObjectUD_initialized = 1
            DistributedObjectBase.__init__(self, air)
            self.accountName = ''
            self.air = air
            className = self.__class__.__name__
            self.dclass = self.air.dclassesByName[className]
            self.__preallocDoId = 0
            self.lastNonQuietZone = None
            self._DOUD_requestedDelete = False
            self.__nextBarrierContext = 0
            self.__barriers = {}
            self.__generated = False
            self.__generates = 0

        return

    def getDeleteEvent(self):
        if hasattr(self, 'doId'):
            return 'distObjDelete-%s' % self.doId
        return None

    def sendDeleteEvent(self):
        delEvent = self.getDeleteEvent()
        if delEvent:
            messenger.send(delEvent)

    def delete(self):
        self.__generates -= 1
        if self.__generates < 0:
            self.notify.debug('DistributedObjectUD: delete() called more times than generate()')
        if self.__generates == 0:
            if self.air is not None:
                if not self._DOUD_requestedDelete:
                    pass
                self._DOUD_requestedDelete = False
                for barrier in self.__barriers.values():
                    barrier.cleanup()

                self.__barriers = {}
                self.parentId = None
                self.zoneId = None
                self.__generated = False
        return

    def isDeleted(self):
        return self.air == None

    def isGenerated(self):
        return self.__generated

    def getDoId(self):
        return self.doId

    def preAllocateDoId(self):
        self.doId = self.air.allocateChannel()
        self.__preallocDoId = 1

    def announceGenerate(self):
        self.__generated = True

    def postGenerateMessage(self):
        messenger.send(self.uniqueName('generate'), [self])

    def addInterest(self, zoneId, note = '', event = None):
        self.air.addInterest(self.getDoId(), zoneId, note, event)

    def b_setLocation(self, parentId, zoneId):
        self.d_setLocation(parentId, zoneId)
        self.setLocation(parentId, zoneId)

    def d_setLocation(self, parentId, zoneId):
        self.air.sendSetLocation(self, parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        self.air.storeObjectLocation(self, parentId, zoneId)

    def getLocation(self):
        try:
            if self.parentId <= 0 and self.zoneId <= 0:
                return None
            if self.parentId == 4294967295L and self.zoneId == 4294967295L:
                return None
            return (self.parentId, self.zoneId)
        except AttributeError:
            return None

        return None

    def updateRequiredFields(self, dclass, di):
        dclass.receiveUpdateBroadcastRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()

    def updateAllRequiredFields(self, dclass, di):
        dclass.receiveUpdateAllRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()

    def updateRequiredOtherFields(self, dclass, di):
        dclass.receiveUpdateBroadcastRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()
        dclass.receiveUpdateOther(self, di)

    def updateAllRequiredOtherFields(self, dclass, di):
        dclass.receiveUpdateAllRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()
        dclass.receiveUpdateOther(self, di)

    def sendSetZone(self, zoneId):
        self.air.sendSetZone(self, zoneId)

    def getZoneChangeEvent(self):
        return 'DOChangeZone-%s' % self.doId

    def getLogicalZoneChangeEvent(self):
        return 'DOLogicalChangeZone-%s' % self.doId

    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        messenger.send(self.getLogicalZoneChangeEvent(), [newZoneId, oldZoneId])

    def getRender(self):
        return self.air.getRender(self.zoneId)

    def getNonCollidableParent(self):
        return self.air.getNonCollidableParent(self.zoneId)

    def getParentMgr(self):
        return self.air.getParentMgr(self.zoneId)

    def getCollTrav(self, *args, **kArgs):
        return self.air.getCollTrav(self.zoneId, *args, **kArgs)

    def sendUpdate(self, fieldName, args = []):
        if self.air:
            self.air.sendUpdate(self, fieldName, args)

    def GetPuppetConnectionChannel(self, doId):
        return doId + (1L << 32)

    def GetAccountConnectionChannel(self, doId):
        return doId + (3L << 32)

    def GetAccountIDFromChannelCode(self, channel):
        return channel >> 32

    def GetAvatarIDFromChannelCode(self, channel):
        return channel & 4294967295L

    def sendUpdateToAvatarId(self, avId, fieldName, args):
        channelId = self.GetPuppetConnectionChannel(avId)
        self.sendUpdateToChannel(channelId, fieldName, args)

    def sendUpdateToAccountId(self, accountId, fieldName, args):
        channelId = self.GetAccountConnectionChannel(accountId)
        self.sendUpdateToChannel(channelId, fieldName, args)

    def sendUpdateToChannel(self, channelId, fieldName, args):
        if self.air:
            self.air.sendUpdateToChannel(self, channelId, fieldName, args)

    def generateWithRequired(self, zoneId, optionalFields = []):
        if self.__preallocDoId:
            self.__preallocDoId = 0
            return self.generateWithRequiredAndId(self.doId, zoneId, optionalFields)
        parentId = self.air.districtId
        self.parentId = parentId
        self.zoneId = zoneId
        self.air.generateWithRequired(self, parentId, zoneId, optionalFields)
        self.generate()

    def generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields = []):
        if self.__preallocDoId:
            self.__preallocDoId = 0
        self.air.generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    def generateOtpObject(self, parentId, zoneId, optionalFields = [], doId = None):
        if self.__preallocDoId:
            doId = self.__preallocDoId
            self.__preallocDoId = 0
        if doId is None:
            self.doId = self.air.allocateChannel()
        else:
            self.doId = doId
        self.air.addDOToTables(self, location=(parentId, zoneId))
        self.sendGenerateWithRequired(self.air, parentId, zoneId, optionalFields)
        self.generate()
        return

    def generate(self):
        self.__generates += 1
        self.air.storeObjectLocation(self, self.parentId, self.zoneId)

    def generateInit(self, repository = None):
        pass

    def generateTargetChannel(self, repository):
        if hasattr(self, 'dbObject'):
            return self.doId
        return repository.serverId

    def sendGenerateWithRequired(self, repository, parentId, zoneId, optionalFields = []):
        dg = self.dclass.aiFormatGenerate(self, self.doId, parentId, zoneId, self.generateTargetChannel(repository), repository.ourChannel, optionalFields)
        repository.send(dg)

    def initFromServerResponse(self, valDict):
        dclass = self.dclass
        for key, value in valDict.items():
            dclass.directUpdate(self, key, value)

    def requestDelete(self):
        if not self.air:
            doId = 'none'
            if hasattr(self, 'doId'):
                doId = self.doId
            self.notify.warning('Tried to delete a %s (doId %s) that is already deleted' % (self.__class__, doId))
            return
        self.air.requestDelete(self)
        self._DOUD_requestedDelete = True

    def taskName(self, taskString):
        return '%s-%s' % (taskString, self.doId)

    def uniqueName(self, idString):
        return '%s-%s' % (idString, self.doId)

    def validate(self, avId, bool, msg):
        if not bool:
            self.air.writeServerEvent('suspicious', avId, msg)
            self.notify.warning('validate error: avId: %s -- %s' % (avId, msg))
        return bool

    def beginBarrier(self, name, avIds, timeout, callback):
        from otp.ai import Barrier
        context = self.__nextBarrierContext
        self.__nextBarrierContext = self.__nextBarrierContext + 1 & 65535
        if avIds:
            barrier = Barrier.Barrier(name, self.uniqueName(name), avIds, timeout, doneFunc=PythonUtil.Functor(self.__barrierCallback, context, callback))
            self.__barriers[context] = barrier
            self.sendUpdate('setBarrierData', [self.__getBarrierData()])
        else:
            callback(avIds)
        return context

    def __getBarrierData(self):
        data = []
        for context, barrier in self.__barriers.items():
            toons = barrier.pendingToons
            if toons:
                data.append((context, barrier.name, toons))

        return data

    def ignoreBarrier(self, context):
        barrier = self.__barriers.get(context)
        if barrier:
            barrier.cleanup()
            del self.__barriers[context]

    def setBarrierReady(self, context):
        avId = self.air.getAvatarIdFromSender()
        barrier = self.__barriers.get(context)
        if barrier == None:
            return
        barrier.clear(avId)
        return

    def __barrierCallback(self, context, callback, avIds):
        barrier = self.__barriers.get(context)
        if barrier:
            barrier.cleanup()
            del self.__barriers[context]
            callback(avIds)
        else:
            self.notify.warning('Unexpected completion from barrier %s' % context)

    def isGridParent(self):
        return 0

    def execCommand(self, string, mwMgrId, avId, zoneId):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedObjectUD.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:06 Pacific Daylight Time
