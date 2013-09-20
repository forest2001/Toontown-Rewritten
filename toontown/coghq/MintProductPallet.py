# 2013.08.22 22:19:17 Pacific Daylight Time
# Embedded file name: toontown.coghq.MintProductPallet
from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct

class MintProductPallet(MintProduct.MintProduct):
    __module__ = __name__
    Models = {CashbotMintIntA: 'phase_10/models/cashbotHQ/DoubleCoinStack.bam',
     CashbotMintIntB: 'phase_10/models/cogHQ/DoubleMoneyStack.bam',
     CashbotMintIntC: 'phase_10/models/cashbotHQ/DoubleGoldStack.bam'}
    Scales = {CashbotMintIntA: 1.0,
     CashbotMintIntB: 1.0,
     CashbotMintIntC: 1.0}
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\MintProductPallet.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:17 Pacific Daylight Time
