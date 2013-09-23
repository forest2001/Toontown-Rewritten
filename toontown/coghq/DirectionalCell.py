import ActiveCell
from direct.directnotify import DirectNotifyGlobal

class DirectionalCell(ActiveCell.ActiveCell):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DirectionalCell')

    def __init__(self, cr):
        ActiveCell.ActiveCell.__init__(self, cr)
