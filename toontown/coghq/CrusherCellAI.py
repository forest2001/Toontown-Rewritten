from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.ActiveCellAI import ActiveCellAI

class CrusherCellAI(ActiveCellAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CrusherCellAI")

