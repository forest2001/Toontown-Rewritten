from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.PotentialAvatar import PotentialAvatar
from pandac.PandaModules import *

class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')

    # --- LOGIN LOGIC ---
    def performLogin(self, doneEvent):
        self.doneEvent = doneEvent

        cookie = self.cr.playToken or 'dev'

        self.notify.debug('Sending login cookie: ' + cookie)
        self.sendUpdate('login', [cookie])

    def acceptLogin(self):
        messenger.send(self.doneEvent, [{'mode': 'success'}])


    # --- AVATARS LIST ---
    def requestAvatars(self):
        self.sendUpdate('requestAvatars')

    def setAvatars(self, avatars):
        avList = []
        for avNum, avName, avDNA, avPosition, aname in avatars:
            names = [avName, '', '', '']
            avList.append(PotentialAvatar(avNum, names, avDNA, avPosition, aname))

        self.cr.handleAvatarsList(avList)


    # --- AVATAR CHOICE ---
    def sendChooseAvatar(self, avId):
        self.sendUpdate('chooseAvatar', [avId])

    def avatarResponse(self, avatarId, avDetails):
        dg = Datagram(avDetails)
        di = DatagramIterator(dg)
        self.cr.handleAvatarResponseMsg(avatarId, di)
