from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import *
from otp.ai.MagicWordGlobal import *

class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.currentContext = 0
        self.requests = {}

    def friendQuery(self, requested):
        avId = self.air.getAvatarIdFromSender()
        if not requested in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to friend a player that does not exist!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to send friendQuery while not on district!')
            return
        context = self.currentContext
        self.requests[context] = [ [ avId, requested ], 'friendQuery']
        self.currentContext += 1
        self.sendUpdateToAvatarId(requested, 'inviteeFriendQuery', [avId, av.getName(), av.getDNAString(), context])

    def cancelFriendQuery(self, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to cancel a request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][0]:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to cancel someone elses request!')
            return
        self.requests[context][1] = 'cancelled'
        self.sendUpdateToAvatarId(self.requests[context][0][1], 'inviteeCancelFriendQuery', [context])

    def inviteeFriendConsidering(self, yesNo, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to consider a friend request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to consider for someone else!')
            return
        if self.requests[context][1] != 'friendQuery':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to reconsider friend request!')
            return
        if yesNo != 1:
            self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendConsidering', [yesNo, context])
            del self.requests[context]
            return
        self.requests[context][1] = 'friendConsidering'
        self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendConsidering', [yesNo, context])

    def inviteeFriendResponse(self, response, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to respond to a friend request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to respond to someone else\'s request!')
            return
        if self.requests[context][1] == 'cancelled':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to respond to non-active friend request!')
            return
        self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendResponse', [response, context])
        if response == 1:
            requested = self.air.doId2do.get(self.requests[context][0][1])
            requester = self.air.doId2do.get(self.requests[context][0][0])

            if not (requested and requester):
                # Likely they logged off just before a response was sent. RIP.
                return


            # Allow both toons to teleport to each other.
            dg = PyDatagram()
            dg.addServerHeader(self.GetPuppetConnectionChannel(requested.getDoId()), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
            dg.addUint32(requester.getDoId())
            dg.addUint16(self.air.dclassesByName['DistributedToonAI'].getNumber())
            self.air.send(dg)

            dg = PyDatagram()
            dg.addServerHeader(self.GetPuppetConnectionChannel(requester.getDoId()), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
            dg.addUint32(requested.getDoId())
            dg.addUint16(self.air.dclassesByName['DistributedToonAI'].getNumber())
            self.air.send(dg)

            requested.extendFriendsList(requester.getDoId(), 0)
            requester.extendFriendsList(requested.getDoId(), 0)

            requested.d_setFriendsList(requested.getFriendsList())
            requester.d_setFriendsList(requester.getFriendsList())
        del self.requests[context]


    def inviteeAcknowledgeCancel(self, context):
        avId = self.air.getAvatarIdFromSender()
        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to acknowledge the cancel of a friend request that doesn\'t exist!')
            return
        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to acknowledge someone else\'s cancel!')
            return
        if self.requests[context][1] != 'cancelled':
            self.air.writeServerEvent('suspicious', avId=avId, issue='Player tried to cancel non-cancelled request!')
            return
        del self.requests[context]


    def friendConsidering(self, todo0, todo1):
        pass

    def friendResponse(self, todo0, todo1):
        pass

    def inviteeFriendQuery(self, todo0, todo1, todo2, todo3):
        pass

    def inviteeCancelFriendQuery(self, todo0):
        pass

    def requestSecret(self):
        pass

    def requestSecretResponse(self, todo0, todo1):
        pass

    def submitSecret(self, todo0):
        pass

    def submitSecretResponse(self, todo0, todo1):
        pass

@magicWord(category=CATEGORY_OVERRIDE, types=[int])
def truefriend(avIdShort):
    '''Automagically add a toon as a true friend.'''
    admin = spellbook.getInvoker()
    avIdFull = 400000000 - (300000000 - avIdShort)
    av = simbase.air.doId2do.get(avIdFull)
    if not av:
        return 'avId not found/online!'
    if int(str(avIdFull)[:2]) >= 40: # AI
        return '%s is an NPC!' % av.getName()
    if not av._isGM:
        return '%s is not a staff member!' % av.getName()


    admin.extendFriendsList(av.getDoId(), 1)
    av.extendFriendsList(admin.getDoId(), 1)

    admin.d_setFriendsList(admin.getFriendsList())
    av.d_setFriendsList(av.getFriendsList())
