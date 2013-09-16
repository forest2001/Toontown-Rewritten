# 2013.08.22 22:18:24 Pacific Daylight Time
# Embedded file name: toontown.coghq.CrusherCell
import ActiveCell
from direct.directnotify import DirectNotifyGlobal

class CrusherCell(ActiveCell.ActiveCell):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CrusherCell')

    def __init__(self, cr):
        ActiveCell.ActiveCell.__init__(self, cr)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coghq\CrusherCell.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:18:24 Pacific Daylight Time
