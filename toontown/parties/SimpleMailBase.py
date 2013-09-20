# 2013.08.22 22:23:43 Pacific Daylight Time
# Embedded file name: toontown.parties.SimpleMailBase


class SimpleMailBase():
    __module__ = __name__

    def __init__(self, msgId, senderId, year, month, day, body):
        self.msgId = msgId
        self.senderId = senderId
        self.year = year
        self.month = month
        self.day = day
        self.body = body

    def __str__(self):
        string = 'msgId=%d ' % self.msgId
        string += 'senderId=%d ' % self.senderId
        string += 'sent=%s-%s-%s ' % (self.year, self.month, self.day)
        string += 'body=%s' % self.body
        return string
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\SimpleMailBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:43 Pacific Daylight Time
