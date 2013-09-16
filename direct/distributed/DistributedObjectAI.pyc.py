# 2013.08.22 22:14:04 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectBase import DistributedObjectBase
from direct.showbase import PythonUtil
from pandac.PandaModules import *

class DistributedObjectAI(DistributedObjectBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObjectAI')
    QuietZone = 1

    def __init__(self, air):
        try:
            self.DistributedObjectAI_initialized
        except:
            self.DistributedObjectAI_initialized = 1
            DistributedObjectBase.__init__(self, air)
            self.accountName = ''
            self.air = air
            className = self.__class__.__name__
            self.dclass = self.air.dclassesByName[className]
            self.__preallocDoId = 0
            self.lastNonQuietZone = None
            self._DOAI_requestedDelete = False
            self.__nextBarrierContext = 0
            self.__barriers = {}
            self.__generated = False
            self.__generates = 0
            self._zoneData = None

        return

    def getDeleteEvent(self):
        if hasattr(self, 'doId'):
            return 'distObjDelete-%s' % self.doId
        return None

    def sendDeleteEvent(self):
        delEvent = self.getDeleteEvent()
        if delEvent:
            messenger.send(delEvent)

    def getCacheable(self):
        return False

    def deleteOrDelay(self):
        self.delete()

    def getDelayDeleteCount(self):
        return 0

    def delete(self):
        self.__generates -= 1
        if self.__generates < 0:
            self.notify.debug('DistributedObjectAI: delete() called more times than generate()')
        if self.__generates == 0:
            if self.air is not None:
                if not self._DOAI_requestedDelete:
                    pass
                self._DOAI_requestedDelete = False
                self.releaseZoneData()
                for barrier in self.__barriers.values():
                    barrier.cleanup()

                self.__barriers = {}
                self.air.stopTrackRequestDeletedDO(self)
                if not hasattr(self, 'doNotDeallocateChannel'):
                    if self.air and not hasattr(self.air, 'doNotDeallocateChannel'):
                        if self.air.minChannel <= self.doId <= self.air.maxChannel:
                            self.air.deallocateChannel(self.doId)
                self.air = None
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
        pass

    def addInterest(self, zoneId, note = '', event = None):
        self.air.addInterest(self.doId, zoneId, note, event)

    def b_setLocation(self, parentId, zoneId):
        self.d_setLocation(parentId, zoneId)
        self.setLocation(parentId, zoneId)

    def d_setLocation(self, parentId, zoneId):
        self.air.sendSetLocation(self, parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        if self.parentId == parentId and self.zoneId == zoneId:
            return
        oldParentId = self.parentId
        oldZoneId = self.zoneId
        self.air.storeObjectLocation(self, parentId, zoneId)
        if oldParentId != parentId or oldZoneId != zoneId:
            self.releaseZoneData()
            messenger.send(self.getZoneChangeEvent(), [zoneId, oldZoneId])
            if zoneId != DistributedObjectAI.QuietZone:
                lastLogicalZone = oldZoneId
                if oldZoneId == DistributedObjectAI.QuietZone:
                    lastLogicalZone = self.lastNonQuietZone
                self.handleLogicalZoneChange(zoneId, lastLogicalZone)
                self.lastNonQuietZone = zoneId

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

    def postGenerateMessage(self):
        self.__generated = True
        messenger.send(self.uniqueName('generate'), [self])

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

    def startMessageBundle(self, name):
        self.air.startMessageBundle(name)

    def sendMessageBundle(self):
        self.air.sendMessageBundle(self.doId)

    def getZoneChangeEvent(self):
        return DistributedObjectAI.staticGetZoneChangeEvent(self.doId)

    def getLogicalZoneChangeEvent(self):
        return DistributedObjectAI.staticGetLogicalZoneChangeEvent(self.doId)

    @staticmethod
    def staticGetZoneChangeEvent(doId):
        return 'DOChangeZone-%s' % doId

    @staticmethod
    def staticGetLogicalZoneChangeEvent(doId):
        return 'DOLogicalChangeZone-%s' % doId

    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        messenger.send(self.getLogicalZoneChangeEvent(), [newZoneId, oldZoneId])

    def getZoneData(self):
        if self._zoneData is None:
            from otp.ai.AIZoneData import AIZoneData
            self._zoneData = AIZoneData(self.air, self.parentId, self.zoneId)
        return self._zoneData

    def releaseZoneData(self):
        if self._zoneData is not None:
            self._zoneData.destroy()
            self._zoneData = None
        return

    def getRender(self):
        return self.getZoneData().getRender()

    def getNonCollidableParent(self):
        return self.getZoneData().getNonCollidableParent()

    def getParentMgr(self):
        return self.getZoneData().getParentMgr()

    def getCollTrav(self, *args, **kArgs):
        return self.getZoneData().getCollTrav(*args, **kArgs)

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
        self.air.generateWithRequired(self, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    def generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields = []):
        if self.__preallocDoId:
            self.__preallocDoId = 0
        self.air.generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()

    def generateOtpObject(self, parentId, zoneId, optionalFields = [], doId = None):
        if self.__preallocDoId:
            doId = self.doId
            self.__preallocDoId = 0
        if doId is None:
            self.doId = self.air.allocateChannel()
        else:
            self.doId = doId
        self.air.addDOToTables(self, location=(parentId, zoneId))
        self.sendGenerateWithRequired(self.air, parentId, zoneId, optionalFields)
        self.generate()
        self.announceGenerate()
        self.postGenerateMessage()
        return

    def generate(self):
        self.__generates += 1

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
        self.air.startTrackRequestDeletedDO(self)
        self._DOAI_requestedDelete = True

    def taskName(self, taskString):
        return '%s-%s' % (taskString, self.doId)

    def uniqueName(self, idString):
        return '%s-%s' % (idString, self.doId)

    def logSuspicious(self, avId, msg):
        self.air.writeServerEvent('suspicious', avId, msg)
        self.notify.warning('suspicious: avId: %s -- %s' % (avId, msg))

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
            self.sendUpdate('setBarrierData', [self.getBarrierData()])
        else:
            callback(avIds)
        return context

    def getBarrierData(self):
        data = []
        for context, barrier in self.__barriers.items():
            avatars = barrier.pendingAvatars
            if avatars:
                data.append((context, barrier.name, avatars))

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

    def _retrieveCachedData(self):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedObjectAI.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:05 Pacific Daylight Time
