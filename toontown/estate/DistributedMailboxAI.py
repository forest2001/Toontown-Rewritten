from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem
import MailboxGlobals

class DistributedMailboxAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailboxAI")
    
    def __init__(self, air, house):
        DistributedObjectAI.__init__(self, air)
        self.house = house
        self.housePos = house.housePos
        self.name = house.name
        self.avId = None

    def getHouseId(self):
        return self.house.getDoId()

    def getHousePos(self):
        return self.housePos
        
    def getName(self):
        return self.name

    def setFullIndicator(self, fullIndicator):
        pass

    def b_setFullIndicator(self, fullIndicator):
        self.setFullIndicator(fullIndicator)
        self.d_setFullIndicator(fullIndicator)
        
    def d_setFullIndicator(self, fullIndicator):
        self.sendUpdate('setFullIndicator', [fullIndicator])
        
    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.house.avatarId:
            self.d_setMovie(MailboxGlobals.MAILBOX_MOVIE_NOT_OWNER, avId)
            taskMgr.doMethodLater(2, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            return
        if self.avId:
            # We're using the mailbox twice! Burn!
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to use a mailbox twice at one time!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to use mailbox from another shard!')
            return
        inMailbox = len(av.mailboxContents)
        onOrder = len(av.onOrder)
        if inMailbox:
            self.d_setMovie(MailboxGlobals.MAILBOX_MOVIE_READY, avId)
            self.avId = avId
        elif onOrder:
            self.d_setMovie(MailboxGlobals.MAILBOX_MOVIE_WAITING, avId)
        else:
            self.d_setMovie(MailboxGlobals.MAILBOX_MOVIE_EMPTY, avId)
        taskMgr.doMethodLater(2, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Exited mailbox without using it first!')
            return
        self.d_setMovie(MailboxGlobals.MAILBOX_MOVIE_EXIT, avId)
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
        self.avId = None
        taskMgr.doMethodLater(2, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])

    def freeAvatar(self):
        pass

    def setMovie(self, todo0, todo1):
        pass
        
    def d_setMovie(self, mode, avId):
        self.sendUpdate('setMovie', [mode, avId])
        
    def __resetMovie(self):
        self.d_setMovie(MailboxGlobals.MAILBOX_MOVIE_CLEAR, 0)

    def acceptItemMessage(self, context, item, index, optional):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            return
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if index >= len(av.mailboxContents):
            self.sendUpdateToAvatarId(avId, 'acceptItemResponse', [context, ToontownGlobals.P_InvalidIndex])
            return
        item = av.mailboxContents[index]
        del av.mailboxContents[index]
        av.b_setMailboxContents(av.mailboxContents)
        self.sendUpdateToAvatarId(avId, 'acceptItemResponse', [context, item.recordPurchase(av, optional)])
        

    def acceptItemResponse(self, todo0, todo1):
        pass

    def discardItemMessage(self, context, item, index, optional):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            return
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if index >= len(av.mailboxContents):
            self.sendUpdateToAvatarId(avId, 'discardItemResponse', [context, ToontownGlobals.P_InvalidIndex])
            return
        del av.mailboxContents[index]
        av.b_setMailboxContents(av.mailboxContents)
        self.sendUpdateToAvatarId(avId, 'discardItemResponse', [context, ToontownGlobals.P_ItemAvailable])

    def discardItemResponse(self, todo0, todo1):
        pass

    def acceptInviteMessage(self, todo0, todo1):
        pass

    def rejectInviteMessage(self, todo0, todo1):
        pass

    def markInviteReadButNotReplied(self, todo0):
        pass

