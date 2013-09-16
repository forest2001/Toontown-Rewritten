# 2013.08.22 22:23:41 Pacific Daylight Time
# Embedded file name: toontown.parties.PartyReplyInfo


class SingleReply():
    __module__ = __name__

    def __init__(self, inviteeId, status):
        self.inviteeId = inviteeId
        self.status = status


class PartyReplyInfoBase():
    __module__ = __name__

    def __init__(self, partyId, partyReplies):
        self.partyId = partyId
        self.replies = []
        for oneReply in partyReplies:
            self.replies.append(SingleReply(*oneReply))

    def __str__(self):
        string = 'partyId=%d ' % self.partyId
        for reply in self.replies:
            string += '(%d:%d) ' % (reply.inviteeId, reply.status)

        return string
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\parties\PartyReplyInfo.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:41 Pacific Daylight Time
