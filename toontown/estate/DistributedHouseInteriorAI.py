from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from DistributedFurnitureManagerAI import *
from DNAFurnitureReaderAI import DNAFurnitureReaderAI
from toontown.dna.DNAParser import *

# The house interior DNA files for each
houseInteriors = [
    'phase_5.5/dna/house_interior3.dna',
    'phase_5.5/dna/house_interior4.dna',
    'phase_5.5/dna/house_interior5.dna',
    'phase_5.5/dna/house_interior7.dna',
    'phase_5.5/dna/house_interior8.dna',
    'phase_5.5/dna/house_interior10.dna',
]

class DistributedHouseInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHouseInteriorAI")
    
    def __init__(self, air, house):
        DistributedObjectAI.__init__(self, air)
        self.house = house

        self.houseId = 0
        self.houseIndex = 0
        self.wallpaper = ''
        self.windows = ''

        self.furnitureManager = DistributedFurnitureManagerAI(self.air, self.house, self)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.furnitureManager.generateWithRequired(self.zoneId)

    def delete(self):
        DistributedObjectAI.delete(self)

        self.furnitureManager.delete()

    def initialize(self):
        # Get DNA file appropriate to this house...
        dnaFile = houseInteriors[self.houseIndex]

        # Load DNA...
        dnaStorage = DNAStorage()
        dnaData = loadDNAFileAI(dnaStorage, dnaFile)

        # Read it into furniture...
        furnitureReader = DNAFurnitureReaderAI(dnaData)

        # Set furniture:
        self.furnitureManager.setItems(furnitureReader.getBlob())

        # Save:
        self.furnitureManager.saveToHouse()

    def setHouseId(self, houseId):
        self.houseId = houseId
        
    def d_setHouseId(self, houseId):
        self.sendUpdate('setHouseId', [houseId])
        
    def b_setHouseId(self, houseId):
        self.setHouseId(houseId)
        self.d_setHouseId(houseId)
        
    def getHouseId(self):
        return self.houseId

    def setHouseIndex(self, index):
        self.houseIndex = index
        
    def d_setHouseIndex(self, index):
        self.sendUpdate('setHouseIndex', [index])
        
    def b_setHouseIndex(self, index):
        self.setHouseIndex(index)
        self.d_setHouseIndex(index)

    def getHouseIndex(self):
        return self.houseIndex
    
    def setWallpaper(self, wallpaper):
        self.wallpaper = wallpaper
        
    def d_setWallpaper(self, wallpaper):
        self.sendUpdate('setWallpaper', [wallpaper])
        
    def b_setWallpaper(self, wallpaper):
        self.setWallpaper(wallpaper)
        if self.isGenerated():
            self.d_setWallpaper(wallpaper)
        
    def getWallpaper(self):
        return self.wallpaper

    def setWindows(self, windows):
        self.windows = windows
        
    def d_setWindows(self, windows):
        self.sendUpdate('setWindows', [windows])
        
    def b_setWindows(self, windows):
        self.setWindows(windows)
        if self.isGenerated():
            self.d_setWindows(windows)
        
    def getWindows(self):
        return self.windows
