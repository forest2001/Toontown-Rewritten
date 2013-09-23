from direct.distributed.ConnectionRepository import ConnectionRepository
from pandac.PandaModules import *
from AIMsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class AIRepository(ConnectionRepository):

    '''dclassesByName = {} #dict mapping str to dclass
    minChannel = 0
    maxChannel = 0
    districtId = 0
    dbObjContext = 0
    estateMgr= UnknownObject()
    timeManager = UnknownObject()
    holidayManager = UnknownObject()
    minigameDifficulty = 0
    minigameSafezoneId = 0
    toontownTimeManager = UnknownObject()
    questManager = UnknownObject()
    fishManager = UnknownObject()
    partyManager = UnknownObject()
    petMgr = UnknownObject()
    SillyMeterMgr = UnknownObject()
    dialogueManager = UnknownObject()
    securityMgr = UnknownObject()
    banManager = UnkObj()
    cogSuitMessageSent = False
    welcomeValleyManager = unkobj()
    catalogManager = unkobj()
    doLiveUpdates = False
    deliveryManager = uo()#the abbriviations keep getting shorter and shorter
    wantEmblems = False
    suitPlanners = {}
    suitInvasionManager = uo()
    teleportRegistrar = uo()
    tutorialManager = uo()
    currentPopulation = 0;'''

    def __init__(self, es_ip, es_port, dcFileNames, serverId, minChannel, maxChannel, dcSuffix='AI'):

        self.minChannel = minChannel
        self.maxChannel = maxChannel
        assert maxChannel >= minChannel

        self.dcSuffix = dcSuffix
        self.readDCFile(dcFileNames)
        self.ourChannel = self.allocateChannel()
        self.channelAllocator = UniqueIdAllocator(minChannel, maxChannel)

        self.districtId = 0
        self.serverId = serverId

        self.dbObjContext = 0
        self.dbObjMap = {}

    def handleDistObjEnter(self, di):
        parentId = di.getUint32()
        zoneId = di.getUint32()
        dclass = dclassesByNumer[di.getUint16()]
        doId = di.getUint32()
        if doId in self.doId2do:
            self.notify.warning('Received redundant entry for object %s' % doId)
            return
        if self.minChannel <= doId <= self.maxChannel:
            self.notify.error('Received object entry for one of our own objects: %s' % doId)
            return

        classDef = dclass.getClassDef()
        if classDef == None:
            self.notify.error('Could not create an undefined %s object.' % dclass.getName())
        distObj = classDef(self)
        distObj.dclass = dclass
        distObj.doId = doId
        distObj.doNotDeallocateChannel = 1 # We never added the object channel. We don't own it.
        self.doId2do[doId] = distObj
        distObj.generateInit()
        distObj.generate()
        distObj.setLocation(parentId, zoneId)
        distObj.updateRequiredFields(dclass, di)
        self.notify.debug('New DO:%s, dclass:%s' % (doId, dclass.getName()))

    def handleDistObjExit(self, di):
        doId = di.getUint32()
        do = self.doId2do.get(doId)
        if do is not None:
            do.delete()

    def handleDistObjLocation(self, di):
        doId = di.getUint32()
        newParentId = di.getUint32()
        newZoneId = di.getUint32()
        oldParentId = di.getUint32()
        oldZoneId = di.getUint32()
        do = self.doId2do.get(doId)
        if do is not None:
            do.setLocation(newParentId, newZoneId)
        else:
            self.notify.warning('Received CHANGE_ZONE for unknown doId %s' % doId)

    def handleMessage(self, msgType, di):
        # This could be overridden by a subclass, if it wishes to add handling for
        # additional message types.
        if msgType == STATESERVER_OBJECT_ENTER_AI_RECV:
            self.handleDistObjEnter(di)
        elif msgType == STATESERVER_OBJECT_LEAVING_AI_INTEREST:
            self.handleDistObjExit(di)
        elif msgType == STATESERVER_OBJECT_CHANGE_ZONE:
            self.handleDistObjLocation(di)

    def handleDatagram(self, di):
        if self.notify.getDebug():
            print 'AIRepository received datagram:'
            di.getDatagram().dumpHex(ostream)

        msgType = self.getMsgType()

        self.handleMessage(msgType, di)

    def getAvatarIdFromSender(self):
        '''Returns the last avatar id recv'd'''
        return (self.sender & 0xFFFFFFFF)

    def writeServerEvent(self, eventType, *args):
        '''air.writeServerEvent('suspicious', senderId, "setParent(0)")'''
        '''The usage of this method seems to be for logging events to the EventLogger Server.
        Hopefully this isn't strictly required at the moment...'''

        dg = PyDatagram()
        dg.addString('AIServer:%s' % self.serverId)
        dg.addString(eventType)
        for arg in args:
            dg.addString(str(arg))

        # TODO: Send dg off to the EL over UDP.

    def stopTrackRequestDeletedDO(self, do):
        '''unknown atm'''
        '''seems like this is used to stop tracking updates to the DO which no longer exists'''

    def deallocateChannel(self, channel):
        '''frees a doId so it can be used again'''
        self.channelAllocator.free(channel)

    def allocateChannel(self):
        '''returns an unused doId'''
        return self.channelAllocator.allocate()

    def registerForChannel(self, channel):
        '''has the ai server subscribe to a channel'''
        dg = PyDatagram()
        dg.addUint8(1)
        dg.addUint64(CONTROL_MESSAGE)
        dg.addUint16(CONTROL_SET_CHANNEL)
        dg.addUint64(channel)
        self.send(dg)

    def unregisterForChannel(self, channel):
        '''has the ai server un?subscribe to a channel'''
        dg = PyDatagram()
        dg.addUint8(1)
        dg.addUint64(CONTROL_MESSAGE)
        dg.addUint16(CONTROL_REMOVE_CHANNEL)
        dg.addUint64(channel)
        self.send(dg)

    def addInterest(self, do, zoneId, note = '', event = None):
        '''unknown use? I thought only clients had interest'''
        '''the lecture says there's no such thing as an ai interest.. there's something called airecv'''

    def sendSetLocation(self, do, parentId, zoneId):
        '''see otpclientrepository for something similar'''
        dg = PyDatagram()
        dg.addServerHeader(do.doId, self.ourChannel, STATESERVER_OBJECT_SET_ZONE)
        dg.addUint32(parentId)
        dg.addUint32(zoneId)
        self.send(dg)

    def startMessageBundle(self, name):
        '''unknown atm'''

    def sendMessageBundle(self, doId):
        '''unknown atm'''

    def sendUpdate(self, do, fieldName, args = []):
        '''updates field according to dclass'''
        self.sendUpdateToChannel(do, do.doId, fieldName, args)

    def sendUpdateToChannel(self, do, channel, fieldName, args = []):
        '''sends field update to specific channel'''
        dg = dclassesByName[fieldName].aiFormatUpdate(fieldName, do.doId, channel, self.ourChannel, args) #get parameters later
        self.send(dg)

    def generateWithRequired(self, do, parentId, zoneId, optionalFields):
        '''same as client, just to the stateserver instead of CA'''
        if do.doId is None:
            do.doId = self.allocateChannel()
        dg = self.dclass.aiFormatGenerate(do, do.doId, parentId, zoneId, do.generateTargetChannel(self), self.ourChannel, optionalFields)
        self.send(dg)

    def generateWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields):
        '''creates object, but without allocating doid'''
        dg = self.dclass.aiFormatGenerate(do, doId, parentId, zoneId, do.generateTargetChannel(self), self.ourChannel, optionalFields)
        self.send(dg)

    def addDOToTables(self, do, location):
        '''unknown at this time'''

    def requestDelete(self, do):
        '''called to delete a DO'''

    def startTrackRequestDeletedDO(self, do):
        '''unknown atm'''

    def sendSetZone(self, do, zoneId):
        '''sets a msg to set a DO's zone'''
        dg = PyDatagram()
        dg.addServerHeader(do.doId, self.ourChannel, STATESERVER_OBJECT_SET_ZONE)
        dg.addUint32(self.districtId)
        dg.addUint32(zoneId)
        self.send(dg)

    def getRender(self, zoneId):
        '''unknown'''

    def getNonCollidableParent(self, zoneId):
        '''unknown'''

    def getParentMgr(self, zoneId):
        '''unknown'''

    def getCollTrav(self,zoneId, *args, **kArgs):#i don't think python has those , it does
        '''unknown'''

    def getZoneDataStore(self):
        '''returns the AIZoneDataStore'''

    def getAvatarExitEvent(self):
        '''unknown, used in Barrier'''

    def _isValidPlayerLocation(self, parentId, zoneId):
        '''checks if a player would ever possibly be in parentId, zoneId. Used as anti-cheat'''
        return True #FIXME

    def incrementPopulation(self):
        '''adds to the district's population count'''#FIXME: Update district stats
        self.currentPopulation = self.currentPopulation + 1

    def decrementPopulation(self):
        '''guess removes to district pop count!!'''
        self.currentPopulation = self.currentPopulation - 1

    def getTrackClsends(self):
        '''used in Clsendtracker'''

    def describeMessage(self, msgStream, unknown, dataStr):
        '''used in Clsendtracker'''

    def getObjectsOfClassInZone(self, districtId, zoneId, classType):
        '''returns all objects of type classType in zoneId'''

    def setAllowClientSend(self, avId, do, fieldNameList):
        '''allows avId to send fields in fieldNameList to do without getting booted'''

    def loadDNAFileAI(self, dnaStore, dnaFileName):
        '''loads a dna file into dnastore'''

    def genDNAFileName(self, zoneId):
        '''generates a dna filename given a zoneId'''

    def sendQueryToonMaxHp(self, doId, event):
        '''queries the db for the toon's max hp'''

    def sendFieldQuery(self, unk1, un2, accountId, event):
        """sendFieldQuery('AccountAI', 'ACCOUNT_AV_SET', accountId, self._handleDbCheckGetAvSetResult)"""

    def getDo(self, doId):
        return self.doId2do(doId)


