# 2013.08.22 22:19:10 Pacific Daylight Time
# Embedded file name: toontown.coghq.LawbotOfficeDiamondRoom_Battle00_Cogs
from SpecImports import *
from toontown.toonbase import ToontownGlobals
CogParent = 10000
BattlePlace1 = 10000
BattleCellId = 0
BattleCells = {BattleCellId: {'parentEntId': BattlePlace1,
                'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(-8, 4, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel + 1,
  'battleCell': BattleCellId,
  'pos': Point3(-3, 4, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(3, 4, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel + 1,
  'battleCell': BattleCellId,
  'pos': Point3(8, 4, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1}]
ReserveCogData = []
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\LawbotOfficeDiamondRoom_Battle00_Cogs.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:19:10 Pacific Daylight Time
