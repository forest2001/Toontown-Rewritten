import ActiveCell
from direct.directnotify import DirectNotifyGlobal

class CrusherCell(ActiveCell.ActiveCell):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CrusherCell')

    def __init__(self, cr):
        ActiveCell.ActiveCell.__init__(self, cr)
