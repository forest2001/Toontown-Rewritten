from direct.directnotify import DirectNotifyGlobal
from toontown.coghq.ActiveCellAI import ActiveCellAI

class DirectionalCellAI(ActiveCellAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DirectionalCellAI")

