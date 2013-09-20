# 2013.08.22 22:19:18 Pacific Daylight Time
# Embedded file name: toontown.coghq.MintShelf
from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct

class MintShelf(MintProduct.MintProduct):
    __module__ = __name__
    Models = {CashbotMintIntA: 'phase_10/models/cashbotHQ/shelf_A1MoneyBags',
     CashbotMintIntB: 'phase_10/models/cashbotHQ/shelf_A1Money',
     CashbotMintIntC: 'phase_10/models/cashbotHQ/shelf_A1Gold'}
    Scales = {CashbotMintIntA: 1.0,
     CashbotMintIntB: 1.0,
     CashbotMintIntC: 1.0}
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\MintShelf.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:18 Pacific Daylight Time
