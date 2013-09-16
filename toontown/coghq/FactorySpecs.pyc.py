# 2013.08.22 22:19:02 Pacific Daylight Time
# Embedded file name: toontown.coghq.FactorySpecs
from toontown.toonbase import ToontownGlobals
import SellbotLegFactorySpec
import SellbotLegFactoryCogs
import LawbotLegFactorySpec
import LawbotLegFactoryCogs

def getFactorySpecModule(factoryId):
    return FactorySpecModules[factoryId]


def getCogSpecModule(factoryId):
    return CogSpecModules[factoryId]


FactorySpecModules = {ToontownGlobals.SellbotFactoryInt: SellbotLegFactorySpec,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactorySpec}
CogSpecModules = {ToontownGlobals.SellbotFactoryInt: SellbotLegFactoryCogs,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactoryCogs}
if __dev__:
    import FactoryMockupSpec
    FactorySpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupSpec
    import FactoryMockupCogs
    CogSpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupCogs
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\FactorySpecs.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:02 Pacific Daylight Time
