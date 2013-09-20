# 2013.08.22 22:23:14 Pacific Daylight Time
# Embedded file name: toontown.parties.DecorBase


class DecorBase():
    __module__ = __name__

    def __init__(self, decorId, x, y, h):
        self.decorId = decorId
        self.x = x
        self.y = y
        self.h = h

    def __str__(self):
        string = 'decorId=%d ' % self.decorId
        string += '(%d,%d,%d) ' % (self.x, self.y, self.h)
        return string

    def __repr__(self):
        return self.__str__()
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\DecorBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:14 Pacific Daylight Time
