# 2013.08.22 22:18:55 Pacific Daylight Time
# Embedded file name: toontown.coghq.FactoryEntityCreator
from otp.level import EntityCreator
import FactoryLevelMgr
import PlatformEntity
import ConveyorBelt
import GearEntity
import PaintMixer
import GoonClipPlane
import MintProduct
import MintProductPallet
import MintShelf
import PathMasterEntity
import RenderingEntity

class FactoryEntityCreator(EntityCreator.EntityCreator):
    __module__ = __name__

    def __init__(self, level):
        EntityCreator.EntityCreator.__init__(self, level)
        nothing = EntityCreator.nothing
        nonlocal = EntityCreator.nonlocal
        self.privRegisterTypes({'activeCell': nonlocal,
         'crusherCell': nonlocal,
         'battleBlocker': nonlocal,
         'beanBarrel': nonlocal,
         'button': nonlocal,
         'conveyorBelt': ConveyorBelt.ConveyorBelt,
         'crate': nonlocal,
         'door': nonlocal,
         'directionalCell': nonlocal,
         'gagBarrel': nonlocal,
         'gear': GearEntity.GearEntity,
         'goon': nonlocal,
         'gridGoon': nonlocal,
         'golfGreenGame': nonlocal,
         'goonClipPlane': GoonClipPlane.GoonClipPlane,
         'grid': nonlocal,
         'healBarrel': nonlocal,
         'levelMgr': FactoryLevelMgr.FactoryLevelMgr,
         'lift': nonlocal,
         'mintProduct': MintProduct.MintProduct,
         'mintProductPallet': MintProductPallet.MintProductPallet,
         'mintShelf': MintShelf.MintShelf,
         'mover': nonlocal,
         'paintMixer': PaintMixer.PaintMixer,
         'pathMaster': PathMasterEntity.PathMasterEntity,
         'rendering': RenderingEntity.RenderingEntity,
         'platform': PlatformEntity.PlatformEntity,
         'sinkingPlatform': nonlocal,
         'stomper': nonlocal,
         'stomperPair': nonlocal,
         'laserField': nonlocal,
         'securityCamera': nonlocal,
         'elevatorMarker': nonlocal,
         'trigger': nonlocal,
         'moleField': nonlocal,
         'maze': nonlocal})
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\FactoryEntityCreator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:55 Pacific Daylight Time
