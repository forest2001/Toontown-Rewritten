from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct

class MintProductPallet(MintProduct.MintProduct):
    Models = {CashbotMintIntA: 'phase_10/models/cashbotHQ/DoubleCoinStack',
     CashbotMintIntB: 'phase_10/models/cogHQ/DoubleMoneyStack',
     CashbotMintIntC: 'phase_10/models/cashbotHQ/DoubleGoldStack'}
    Scales = {CashbotMintIntA: 1.0,
     CashbotMintIntB: 1.0,
     CashbotMintIntC: 1.0}
