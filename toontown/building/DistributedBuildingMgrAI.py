import os
from direct.task.Task import Task
import cPickle
from otp.ai.AIBaseGlobal import *
import DistributedBuildingAI
import HQBuildingAI
#import GagshopBuildingAI
#import PetshopBuildingAI
#from toontown.building.KartShopBuildingAI import KartShopBuildingAI
#from toontown.building import DistributedAnimBuildingAI
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
import time
import random

class DistributedBuildingMgrAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuildingMgrAI')
    serverDatafolder = simbase.config.GetString('server-data-folder', '')

    def __init__(self, air, branchID, dnaStore, trophyMgr):
        self.branchID = branchID
        self.canonicalBranchID = ZoneUtil.getCanonicalZoneId(branchID)
        self.air = air
        self.__buildings = {}
        self.dnaStore = dnaStore
        self.trophyMgr = trophyMgr
        self.shard = str(air.districtId)
        self.backupExtension = '.bu'
        self.findAllLandmarkBuildings()
        self.doLaterTask = None
        return

    def cleanup(self):
        taskMgr.remove(str(self.branchID) + '_delayed_save-timer')
        for building in self.__buildings.values():
            building.cleanup()

        self.__buildings = {}

    def isValidBlockNumber(self, blockNumber):
        return self.__buildings.has_key(blockNumber)

    def delayedSaveTask(self, task):
        self.save()
        self.doLaterTask = None
        return Task.done

    def isSuitBlock(self, blockNumber):
        return self.__buildings[blockNumber].isSuitBlock()

    def getSuitBlocks(self):
        blocks = []
        for i in self.__buildings.values():
            if i.isSuitBlock():
                blocks.append(i.getBlock()[0])

        return blocks

    def getEstablishedSuitBlocks(self):
        blocks = []
        for i in self.__buildings.values():
            if i.isEstablishedSuitBlock():
                blocks.append(i.getBlock()[0])

        return blocks

    def getToonBlocks(self):
        blocks = []
        for i in self.__buildings.values():
            if isinstance(i, HQBuildingAI.HQBuildingAI):
                continue
            if not i.isSuitBlock():
                blocks.append(i.getBlock()[0])

        return blocks

    def getBuildings(self):
        return self.__buildings.values()

    def getFrontDoorPoint(self, blockNumber):
        return self.__buildings[blockNumber].getFrontDoorPoint()

    def getBuildingTrack(self, blockNumber):
        return self.__buildings[blockNumber].track

    def getBuilding(self, blockNumber):
        return self.__buildings[blockNumber]

    def setFrontDoorPoint(self, blockNumber, point):
        return self.__buildings[blockNumber].setFrontDoorPoint(point)

    def getDNABlockLists(self):
        blocks = []
        hqBlocks = []
        gagshopBlocks = []
        petshopBlocks = []
        kartshopBlocks = []
        animBldgBlocks = []
        for blockId, block in self.dnaStore.getBlocks():
            blockNumber = blockId
            buildingType = block.buildingType
            if buildingType == 'hq':
                hqBlocks.append(blockNumber)
            elif buildingType == 'gagshop':
                gagshopBlocks.append(blockNumber)
            elif buildingType == 'petshop':
                petshopBlocks.append(blockNumber)
            elif buildingType == 'kartshop':
                kartshopBlocks.append(blockNumber)
            elif buildingType == 'animbldg':
                animBldgBlocks.append(blockNumber)
            else:
                blocks.append(blockNumber)

        return (blocks,
         hqBlocks,
         gagshopBlocks,
         petshopBlocks,
         kartshopBlocks,
         animBldgBlocks)

    def findAllLandmarkBuildings(self):
        buildings = self.load()
        blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks, animBldgBlocks = self.getDNABlockLists()
        for block in blocks:
            self.newBuilding(block, buildings.get(block, None))

        for block in animBldgBlocks:
            self.newAnimBuilding(block, buildings.get(block, None))

        for block in hqBlocks:
            self.newHQBuilding(block)

        for block in gagshopBlocks:
            self.newGagshopBuilding(block)

        if simbase.wantPets:
            for block in petshopBlocks:
                self.newPetshopBuilding(block)

        if simbase.wantKarts:
            for block in kartshopBlocks:
                self.newKartShopBuilding(block)

        return

    def newBuilding(self, blockNumber, blockData = None):
        building = DistributedBuildingAI.DistributedBuildingAI(self.air, blockNumber, self.branchID, self.trophyMgr)
        building.generateWithRequired(self.branchID)
        if blockData:
            building.track = blockData.get('track', 'c')
            building.difficulty = int(blockData.get('difficulty', 1))
            building.numFloors = int(blockData.get('numFloors', 1))
            building.numFloors = max(1, min(5, building.numFloors))
            if not ZoneUtil.isWelcomeValley(building.zoneId):
                building.updateSavedBy(blockData.get('savedBy'))
            else:
                self.notify.warning('we had a cog building in welcome valley %d' % building.zoneId)
            building.becameSuitTime = blockData.get('becameSuitTime', time.time())
            if blockData['state'] == 'suit':
                building.setState('suit')
            elif blockData['state'] == 'cogdo':
                if simbase.air.wantCogdominiums:
                    building.setState('cogdo')
            else:
                building.setState('toon')
        else:
            building.setState('toon')
        self.__buildings[blockNumber] = building
        return building

    def newAnimBuilding(self, blockNumber, blockData = None):
        return
        building = DistributedAnimBuildingAI.DistributedAnimBuildingAI(self.air, blockNumber, self.branchID, self.trophyMgr)
        building.generateWithRequired(self.branchID)
        if blockData:
            building.track = blockData.get('track', 'c')
            building.difficulty = int(blockData.get('difficulty', 1))
            building.numFloors = int(blockData.get('numFloors', 1))
            if not ZoneUtil.isWelcomeValley(building.zoneId):
                building.updateSavedBy(blockData.get('savedBy'))
            else:
                self.notify.warning('we had a cog building in welcome valley %d' % building.zoneId)
            building.becameSuitTime = blockData.get('becameSuitTime', time.time())
            if blockData['state'] == 'suit':
                building.setState('suit')
            else:
                building.setState('toon')
        else:
            building.setState('toon')
        self.__buildings[blockNumber] = building
        return building

    def newHQBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        self.notify.debug("Spawning HQ ext: {0} int: {1}".format(exteriorZoneId, interiorZoneId))
        building = HQBuildingAI.HQBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newGagshopBuilding(self, blockNumber):
        return
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        building = GagshopBuildingAI.GagshopBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newPetshopBuilding(self, blockNumber):
        return
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        building = PetshopBuildingAI.PetshopBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newKartShopBuilding(self, blockNumber):
        return
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        building = KartShopBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def getFileName(self):
        f = '%s%s_%d.buildings' % (self.serverDatafolder, self.shard, self.branchID)
        return f

    def saveTo(self, file, block = None):
        if block:
            pickleData = block.getPickleData()
            cPickle.dump(pickleData, file)
        else:
            for i in self.__buildings.values():
                if isinstance(i, HQBuildingAI.HQBuildingAI):
                    continue
                pickleData = i.getPickleData()
                cPickle.dump(pickleData, file)

    def fastSave(self, block):
        return
        try:
            fileName = self.getFileName() + '.delta'
            working = fileName + '.temp'
            if os.path.exists(working):
                os.remove(working)
            os.rename(fileName, working)
            file = open(working, 'w')
            file.seek(0, 2)
            self.saveTo(file, block)
            file.close()
            os.rename(working, fileName)
        except IOError:
            self.notify.error(str(sys.exc_info()[1]))

    def save(self):
        try:
            fileName = self.getFileName()
            backup = fileName + self.backupExtension
            if os.path.exists(fileName):
                os.rename(fileName, backup)
            file = open(fileName, 'w')
            file.seek(0)
            self.saveTo(file)
            file.close()
            if os.path.exists(backup):
                os.remove(backup)
        except EnvironmentError:
            self.notify.warning(str(sys.exc_info()[1]))

    def loadFrom(self, file):

        #0	BUILD_MAP         None
        #3	STORE_FAST        'blocks'
        blocks = {}

#6	SETUP_EXCEPT      '55'
        try:

#9	SETUP_LOOP        '51'
            while 1:

                #12	LOAD_GLOBAL       'cPickle'
                #15	LOAD_ATTR         'load'
                #18	LOAD_FAST         'file'
                #21	CALL_FUNCTION_1   None
                #24	STORE_FAST        'pickleData'
                pickleData = cPickle.load(file)
        

                #27	LOAD_FAST         'pickleData'
                #30	LOAD_FAST         'blocks'
                #33	LOAD_GLOBAL       'int'
                #36	LOAD_FAST         'pickleData'
                #39	LOAD_CONST        'block'
                #42	BINARY_SUBSCR     None
                #43	CALL_FUNCTION_1   None
                #46	STORE_SUBSCR      None
                #47	JUMP_BACK         '12'
                #50	POP_BLOCK         None
                #51_0	COME_FROM         '9'
                #51	POP_BLOCK         None
                #52	JUMP_FORWARD      '72'
                #55_0	COME_FROM         '6'
                blocks[int(pickleData['block'])] = pickleData

        #55	DUP_TOP           None
        #56	LOAD_GLOBAL       'EOFError'
        #59	COMPARE_OP        'exception match'
        #62	JUMP_IF_FALSE     '71'
        #65	POP_TOP           None
        #66	POP_TOP           None
        #67	POP_TOP           None
        except EOFError:
            pass

        #68	JUMP_FORWARD      '72'
        #71	END_FINALLY       None
        #72_0	COME_FROM         '52'
        #72_1	COME_FROM         '71'

        #72	LOAD_FAST         'blocks'
        #75	RETURN_VALUE      None
        #-1	RETURN_LAST       None
        return blocks

    def load(self):
        fileName = self.getFileName()
        try:
            file = open(fileName + self.backupExtension, 'r')
            if os.path.exists(fileName):
                os.remove(fileName)
        except IOError:
            try:
                file = open(fileName, 'r')
            except IOError:
                return {}

        file.seek(0)
        blocks = self.loadFrom(file)
        file.close()
        return blocks
# VERIFICATION PASSED
