import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.estate import GardenGlobals
from direct.actor import Actor
from pandac.PandaModules import NodePath

class CatalogGardenItem(CatalogItem.CatalogItem):
    __module__ = __name__
    sequenceNumber = 0

    def makeNewItem(self, itemIndex = 0, count = 3, tagCode = 1):
        self.gardenIndex = itemIndex
        self.numItems = count
        self.giftCode = tagCode
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
            return 1
        else:
            return 100

    def reachedPurchaseLimit(self, avatar):
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        return 0

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptGarden
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.GardenTypeName

    def getName(self):
        name = GardenGlobals.Specials[self.gardenIndex]['photoName']
        return name

    def recordPurchase--- This code section failed: ---

0	LOAD_FAST         'avatar'
3	JUMP_IF_FALSE     '31'

6	LOAD_FAST         'avatar'
9	LOAD_ATTR         'addGardenItem'
12	LOAD_FAST         'self'
15	LOAD_ATTR         'gardenIndex'
18	LOAD_FAST         'self'
21	LOAD_ATTR         'numItems'
24	CALL_FUNCTION_2   None
27	POP_TOP           None
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_GLOBAL       'ToontownGlobals'
34	LOAD_ATTR         'P_ItemAvailable'
37	RETURN_VALUE      None
38	JUMP_FORWARD      '41'
41_0	COME_FROM         '38'

Syntax error at or near `JUMP_FORWARD' token at offset 38

    def getPicture(self, avatar):
        photoModel = GardenGlobals.Specials[self.gardenIndex]['photoModel']
        if GardenGlobals.Specials[self.gardenIndex].has_key('photoAnimation'):
            modelPath = photoModel + GardenGlobals.Specials[self.gardenIndex]['photoAnimation'][0]
            animationName = GardenGlobals.Specials[self.gardenIndex]['photoAnimation'][1]
            animationPath = photoModel + animationName
            self.model = Actor.Actor()
            self.model.loadModel(modelPath)
            self.model.loadAnims(dict([[animationName, animationPath]]))
            frame, ival = self.makeFrameModel(self.model, 0)
            ival = ActorInterval(self.model, animationName, 2.0)
            photoPos = GardenGlobals.Specials[self.gardenIndex]['photoPos']
            frame.setPos(photoPos)
            photoScale = GardenGlobals.Specials[self.gardenIndex]['photoScale']
            self.model.setScale(photoScale)
            self.hasPicture = True
            return (frame, ival)
        else:
            self.model = loader.loadModel(photoModel)
            frame = self.makeFrame()
            self.model.reparentTo(frame)
            photoPos = GardenGlobals.Specials[self.gardenIndex]['photoPos']
            self.model.setPos(*photoPos)
            photoScale = GardenGlobals.Specials[self.gardenIndex]['photoScale']
            self.model.setScale(photoScale)
            self.hasPicture = True
            return (frame, None)
        return None

    def cleanupPicture(self):
        CatalogItem.CatalogItem.cleanupPicture(self)
        self.model.detachNode()
        self.model = None
        return

    def output(self, store = -1):
        return 'CatalogGardenItem(%s%s)' % (self.gardenIndex, self.formatOptionalData(store))

    def compareTo(self, other):
        return 0

    def getHashContents(self):
        return self.gardenIndex

    def getBasePrice(self):
        beanCost = GardenGlobals.Specials[self.gardenIndex]['beanCost']
        return beanCost

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.gardenIndex = di.getUint8()
        self.numItems = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.gardenIndex)
        dg.addUint8(self.numItems)

    def getRequestPurchaseErrorText(self, retcode):
        retval = CatalogItem.CatalogItem.getRequestPurchaseErrorText(self, retcode)
        origText = retval
        if retval == TTLocalizer.CatalogPurchaseItemAvailable or retval == TTLocalizer.CatalogPurchaseItemOnOrder:
            recipeKey = GardenGlobals.getRecipeKeyUsingSpecial(self.gardenIndex)
            if not recipeKey == -1:
                retval += GardenGlobals.getPlantItWithString(self.gardenIndex)
                if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
                    if GardenGlobals.ACCELERATOR_USED_FROM_SHTIKER_BOOK:
                        retval = origText
                        retval += TTLocalizer.UseFromSpecialsTab
                    retval += TTLocalizer.MakeSureWatered
        return retval

    def getRequestPurchaseErrorTextTimeout(self):
        return 20

    def getDeliveryTime(self):
        if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
            return 24 * 60
        else:
            return 0

    def getPurchaseLimit(self):
        if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
            return 1
        else:
            return 0

    def compareTo(self, other):
        if self.gardenIndex != other.gardenIndex:
            return self.gardenIndex - other.gardenIndex
        return self.gardenIndex - other.gardenIndex

    def reachedPurchaseLimit(self, avatar):
        if avatar.onOrder.count(self) != 0:
            return 1
        if avatar.mailboxContents.count(self) != 0:
            return 1
        for specials in avatar.getGardenSpecials():
            if specials[0] == self.gardenIndex:
                if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
                    return 1

        return 0

    def isSkillTooLow(self, avatar):
        recipeKey = GardenGlobals.getRecipeKeyUsingSpecial(self.gardenIndex)
        recipe = GardenGlobals.Recipes[recipeKey]
        numBeansRequired = len(recipe['beans'])
        canPlant = avatar.getBoxCapability()
        result = False
        if canPlant < numBeansRequired:
            result = True
        if not result and GardenGlobals.Specials.has_key(self.gardenIndex) and GardenGlobals.Specials[self.gardenIndex].has_key('minSkill'):
            minSkill = GardenGlobals.Specials[self.gardenIndex]['minSkill']
            if avatar.shovelSkill < minSkill:
                result = True
            else:
                result = False
        return result

    def noGarden(self, avatar):
        return not avatar.getGardenStarted()

    def isGift(self):
        return 0# decompiled 0 files: 0 okay, 1 failed, 0 verify failed

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\catalog\CatalogGardenItem.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'avatar'
3	JUMP_IF_FALSE     '31'

6	LOAD_FAST         'avatar'
9	LOAD_ATTR         'addGardenItem'
12	LOAD_FAST         'self'
15	LOAD_ATTR         'gardenIndex'
18	LOAD_FAST         'self'
21	LOAD_ATTR         'numItems'
24	CALL_FUNCTION_2   None
27	POP_TOP           None
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_GLOBAL       'ToontownGlobals'
34	LOAD_ATTR         'P_ItemAvailable'
37	RETURN_VALUE      None
38	JUMP_FORWARD      '41'
41_0	COME_FROM         '38'

Syntax error at or near `JUMP_FORWARD' token at offset 38

