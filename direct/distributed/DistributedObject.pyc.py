# 2013.08.22 22:14:03 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedObject
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectBase import DistributedObjectBase
from direct.showbase.PythonUtil import StackTrace
ESNew = 1
ESDeleted = 2
ESDisabling = 3
ESDisabled = 4
ESGenerating = 5
ESGenerated = 6
ESNum2Str = {ESNew: 'ESNew',
 ESDeleted: 'ESDeleted',
 ESDisabling: 'ESDisabling',
 ESDisabled: 'ESDisabled',
 ESGenerating: 'ESGenerating',
 ESGenerated: 'ESGenerated'}

class DistributedObject(DistributedObjectBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObject')
    neverDisable = 0

    def __init__(self, cr):
        try:
            self.DistributedObject_initialized
        except:
            self.DistributedObject_initialized = 1
            DistributedObjectBase.__init__(self, cr)
            self.setCacheable(0)
            self._token2delayDeleteName = {}
            self._delayDeleteForceAllow = False
            self._delayDeleted = 0
            self.activeState = ESNew
            self.__nextContext = 0
            self.__callbacks = {}
            self.__barrierContext = None

        return

    def getAutoInterests(self):

        def _getAutoInterests(cls):
            if 'autoInterests' in cls.__dict__:
                autoInterests = cls.autoInterests
            else:
                autoInterests = set()
                for base in cls.__bases__:
                    autoInterests.update(_getAutoInterests(base))

                if cls.__name__ in self.cr.dclassesByName:
                    dclass = self.cr.dclassesByName[cls.__name__]
                    field = dclass.getFieldByName('AutoInterest')
                    if field is not None:
                        p = DCPacker()
                        p.setUnpackData(field.getDefaultValue())
                        len = p.rawUnpackUint16() / 4
                        for i in xrange(len):
                            zone = int(p.rawUnpackUint32())
                            autoInterests.add(zone)

                    autoInterests.update(autoInterests)
                    cls.autoInterests = autoInterests
            return set(autoInterests)

        autoInterests = _getAutoInterests(self.__class__)
        if len(autoInterests) > 1:
            self.notify.error('only one auto-interest allowed per DC class, %s has %s autoInterests (%s)' % (self.dclass.getName(), len(autoInterests), list(autoInterests)))
        _getAutoInterests = None
        return list(autoInterests)

    def setNeverDisable(self, bool):
        self.neverDisable = bool

    def getNeverDisable(self):
        return self.neverDisable

    def _retrieveCachedData(self):
        if self.cr.doDataCache.hasCachedData(self.doId):
            self._cachedData = self.cr.doDataCache.popCachedData(self.doId)

    def setCachedData(self, name, data):
        self.cr.doDataCache.setCachedData(self.doId, name, data)

    def hasCachedData(self, name):
        if not hasattr(self, '_cachedData'):
            return False
        return name in self._cachedData

    def getCachedData(self, name):
        data = self._cachedData[name]
        del self._cachedData[name]
        return data

    def flushCachedData(self, name):
        self._cachedData[name].flush()

    def setCacheable(self, bool):
        self.cacheable = bool

    def getCacheable(self):
        return self.cacheable

    def deleteOrDelay(self):
        if len(self._token2delayDeleteName) > 0:
            if not self._delayDeleted:
                self._delayDeleted = 1
                messenger.send(self.getDelayDeleteEvent())
                if len(self._token2delayDeleteName) > 0:
                    self.delayDelete()
                    if len(self._token2delayDeleteName) > 0:
                        self._deactivateDO()
        else:
            self.disableAnnounceAndDelete()

    def disableAnnounceAndDelete(self):
        self.disableAndAnnounce()
        self.delete()
        self._destroyDO()

    def getDelayDeleteCount(self):
        return len(self._token2delayDeleteName)

    def getDelayDeleteEvent(self):
        return self.uniqueName('delayDelete')

    def getDisableEvent(self):
        return self.uniqueName('disable')

    def disableAndAnnounce(self):
        if self.activeState != ESDisabled:
            self.activeState = ESDisabling
            messenger.send(self.getDisableEvent())
            self.disable()
            self.activeState = ESDisabled
            if not self._delayDeleted:
                self._deactivateDO()

    def announceGenerate(self):
        pass

    def _deactivateDO(self):
        self.networkDelete()
        if not self.cr:
            self.notify.warning('self.cr is none in _deactivateDO %d' % self.doId)
            if hasattr(self, 'destroyDoStackTrace'):
                print self.destroyDoStackTrace
        self.__callbacks = {}
        self.cr.closeAutoInterests(self)
        self.setLocation(0, 0)
        self.cr.deleteObjectLocation(self, self.parentId, self.zoneId)

    def networkDelete(self):
        pass

    def _destroyDO(self):
        self.destroyDoStackTrace = StackTrace()
        if hasattr(self, '_cachedData'):
            for name, cachedData in self._cachedData.iteritems():
                self.notify.warning('flushing unretrieved cached data: %s' % name)
                cachedData.flush()

            del self._cachedData
        self.cr = None
        self.dclass = None
        return

    def disable(self):
        pass

    def isDisabled(self):
        return self.activeState < ESGenerating

    def isGenerated(self):
        return self.activeState == ESGenerated

    def delete(self):
        try:
            self.DistributedObject_deleted
        except:
            self.DistributedObject_deleted = 1

    def generate(self):
        self.activeState = ESGenerating
        if not hasattr(self, '_autoInterestHandle'):
            self.cr.openAutoInterests(self)

    def generateInit(self):
        self.activeState = ESGenerating

    def getDoId(self):
        return self.doId

    def postGenerateMessage(self):
        if self.activeState != ESGenerated:
            self.activeState = ESGenerated
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

    def sendUpdate(self, fieldName, args = [], sendToId = None):
        if self.cr:
            dg = self.dclass.clientFormatUpdate(fieldName, sendToId or self.doId, args)
            self.cr.send(dg)

    def sendDisableMsg(self):
        self.cr.sendDisableMsg(self.doId)

    def sendDeleteMsg(self):
        self.cr.sendDeleteMsg(self.doId)

    def taskName(self, taskString):
        return '%s-%s' % (taskString, self.doId)

    def uniqueName(self, idString):
        return '%s-%s' % (idString, self.doId)

    def getCallbackContext(self, callback, extraArgs = []):
        context = self.__nextContext
        self.__callbacks[context] = (callback, extraArgs)
        self.__nextContext = self.__nextContext + 1 & 65535
        return context

    def getCurrentContexts(self):
        return self.__callbacks.keys()

    def getCallback(self, context):
        return self.__callbacks[context][0]

    def getCallbackArgs(self, context):
        return self.__callbacks[context][1]

    def doCallbackContext(self, context, args):
        tuple = self.__callbacks.get(context)
        if tuple:
            callback, extraArgs = tuple
            completeArgs = args + extraArgs
            if callback != None:
                callback(*completeArgs)
            del self.__callbacks[context]
        else:
            self.notify.warning('Got unexpected context from AI: %s' % context)
        return

    def setBarrierData(self, data):
        for context, name, avIds in data:
            for avId in avIds:
                if self.cr.isLocalId(avId):
                    self.__barrierContext = (context, name)
                    return

        self.__barrierContext = None
        return

    def getBarrierData(self):
        return ((0, '', []),)

    def doneBarrier(self, name = None):
        if self.__barrierContext != None:
            context, aiName = self.__barrierContext
            if name == None or name == aiName:
                self.sendUpdate('setBarrierReady', [context])
                self.__barrierContext = None
        return

    def addInterest(self, zoneId, note = '', event = None):
        return self.cr.addInterest(self.getDoId(), zoneId, note, event)

    def removeInterest(self, handle, event = None):
        return self.cr.removeInterest(handle, event)

    def b_setLocation(self, parentId, zoneId):
        self.d_setLocation(parentId, zoneId)
        self.setLocation(parentId, zoneId)

    def d_setLocation(self, parentId, zoneId):
        self.cr.sendSetLocation(self.doId, parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        self.cr.storeObjectLocation(self, parentId, zoneId)

    def getLocation(self):
        try:
            if self.parentId == 0 and self.zoneId == 0:
                return None
            if self.parentId == 4294967295L and self.zoneId == 4294967295L:
                return None
            return (self.parentId, self.zoneId)
        except AttributeError:
            return None

        return None

    def getParentObj(self):
        if self.parentId is None:
            return
        return self.cr.doId2do.get(self.parentId)

    def isLocal(self):
        return self.cr and self.cr.isLocalId(self.doId)

    def isGridParent(self):
        return 0

    def execCommand(self, string, mwMgrId, avId, zoneId):
        pass
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedObject.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:04 Pacific Daylight Time
