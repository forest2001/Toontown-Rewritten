from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.FSM import FSM
from direct.distributed.PyDatagram import *
from toontown.toon.ToonDNA import ToonDNA
from toontown.makeatoon.NameGenerator import NameGenerator
from toontown.toonbase import TTLocalizer
from otp.distributed import OtpDoGlobals
from sys import platform
from pymongo.errors import AutoReconnect
import time
import hmac
import hashlib
import json
from ClientServicesManager import FIXED_KEY

REPORT_REASONS = [
    'MODERATION_FOUL_LANGUAGE', 'MODERATION_PERSONAL_INFO',
    'MODERATION_RUDE_BEHAVIOR', 'MODERATION_BAD_NAME', 'MODERATION_HACKING',
]

# --- ACCOUNT DATABASES ---
class LocalAccountDB:
    def __init__(self, csm):
        self.csm = csm

    def lookup(self, cookie, callback):
        if cookie.startswith('.'):
            # Beginning a cookie with . symbolizes "invalid"
            callback({'success': False,
                      'reason': 'Invalid cookie specified!'})
            return

        # databaseId must be a uint32, so we'll use the crc32 of the cookie:
        import zlib
        databaseId = zlib.crc32(cookie)&0x7FFFFFFF

        callback({'success': True,
                  'databaseId': databaseId,
                  'adminAccess': 507,
                  'betaKeyQuest': 1})

class RemoteAccountDB:
    def __init__(self, csm):
        self.csm = csm

    def lookup(self, cookie, callback):
        def rpcCallback(result=None):
            if result is None:
                # This is an errback:
                callback({'success': False,
                          'reason': 'Could not contact the account server'})
                return

            if type(result) != dict:
                callback({'success': False,
                          'reason': 'Account server responded with an unknown'
                                    ' object type.'})
                return

            if result.get('success'):
                if 'databaseId' not in result:
                    callback({'success': False,
                              'reason': 'Account server did not provide a'
                                        ' databaseId.'})
                    return
            else:
                result.setdefault('reason', 'Unspecified reason.')

            callback(result)

        self.csm.air.rpc.call('redeemCookie', cookie=cookie,
                              _callback=rpcCallback, _errback=rpcCallback)

# Constants used by the naming FSM:
WISHNAME_LOCKED = 0
WISHNAME_OPEN = 1
WISHNAME_PENDING = 2
WISHNAME_APPROVED = 3
WISHNAME_REJECTED = 4

# --- FSMs ---
class OperationFSM(FSM):
    TARGET_CONNECTION = False

    def __init__(self, csm, target):
        self.csm = csm
        self.target = target
        FSM.__init__(self, self.__class__.__name__)

    def enterKill(self, reason=''):
        if self.TARGET_CONNECTION:
            self.csm.killConnection(self.target, reason)
        else:
            self.csm.killAccount(self.target, reason)
        self.demand('Off')

    def enterOff(self):
        if self.TARGET_CONNECTION:
            del self.csm.connection2fsm[self.target]
        else:
            del self.csm.account2fsm[self.target]

class LoginAccountFSM(OperationFSM):
    TARGET_CONNECTION = True
    notify = directNotify.newCategory('LoginAccountFSM')

    def enterStart(self, cookie):
        self.cookie = cookie

        self.demand('QueryAccountDB')

    def enterQueryAccountDB(self):
        self.csm.accountDB.lookup(self.cookie, self.__handleLookup)

    def __handleLookup(self, result):
        if not result.get('success'):
            self.csm.air.writeServerEvent('cookie-rejected', clientId=self.target, cookie=self.cookie)
            self.demand('Kill', result.get('reason', 'The accounts database rejected your cookie.'))
            return

        self.databaseId = result.get('databaseId', 0)
        self.adminAccess = result.get('adminAccess', 0)
        self.betaKeyQuest = result.get('betaKeyQuest', 0)

        # Binary bitmask in base10 form, added to the adminAccess.
        # To find out what they have access to, convert the serverAccess to 3-bit binary.
        # 2^2 = dev, 2^1 = qa, 2^0 = test
        serverType = config.GetString('server-type', 'dev')
        serverAccess = self.adminAccess % 10 # Get the last digit in their access.
        if (serverType == 'dev' and not serverAccess & 4) or \
           (serverType == 'qa' and not serverAccess & 2) or \
           (serverType == 'test' and not serverAccess & 1):
            self.csm.air.writeServerEvent('insufficient-access', clientId=self.target, cookie=self.cookie)
            self.demand('Kill', result.get('reason', 'You have insufficient access to login.'))
            return

        # Try to figure out the accountId using the databaseId.
        # To do this, query the MongoDB backend and ask it for the account:
        try:
            self.csm.air.mongodb.astron.objects.ensure_index('fields.ACCOUNT_ID')
            account = self.csm.air.mongodb.astron.objects.find_one({'fields.ACCOUNT_ID': self.databaseId})
        except AutoReconnect:
            taskMgr.doMethodLater(config.GetInt('mongodb-retry-time', 2), self.__retryLookup, 'retryLookUp-%d' % self.databaseId, extraArgs=[])
            return

        if account:
            self.accountId = account['_id']
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')

    def __retryLookup(self):
        try:
            self.csm.air.mongodb.astron.objects.ensure_index('fields.ACCOUNT_ID')
            account = self.csm.air.mongodb.astron.objects.find_one({'fields.ACCOUNT_ID': self.databaseId})
        except AutoReconnect:
            taskMgr.doMethodLater(config.GetInt('mongodb-retry-time', 2), self.__retryLookup, 'retryLookUp-%d' % self.databaseId, extraArgs=[])
            return

        if account:
            self.accountId = account['_id']
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')
    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.accountId,
                                             self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.demand('SetAccount')

    def enterCreateAccount(self):
        self.account = {'ACCOUNT_AV_SET': [0]*6,
                        'ESTATE_ID': 0,
                        'ACCOUNT_AV_SET_DEL': [],
                        'CREATED': time.ctime(),
                        'LAST_LOGIN': time.ctime(),
                        'BETA_KEY_QUEST': self.betaKeyQuest,
                        'ACCOUNT_ID': self.databaseId,
                        'ADMIN_ACCESS': self.adminAccess}

        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['AccountUD'],
            self.account,
            self.__handleCreate)

    def __handleCreate(self, accountId):
        if self.state != 'CreateAccount':
            self.notify.warning('Received create account response outside of CreateAccount state.')
            return

        if not accountId:
            self.notify.warning('Database failed to construct an account object!')
            self.demand('Kill', 'Your account object could not be created in the game database.')
            return

        self.csm.air.writeServerEvent('account-created', accId=accountId)

        self.accountId = accountId
        self.demand('SetAccount')

    def enterSetAccount(self):
        # First, if there's anybody on the account, kill 'em for redundant login:
        dg = PyDatagram()
        dg.addServerHeader(self.csm.GetAccountConnectionChannel(self.accountId),
                           self.csm.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(100)
        dg.addString('This account has been logged in elsewhere.')
        self.csm.air.send(dg)

        # Next, add this connection to the account channel.
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
        dg.addChannel(self.csm.GetAccountConnectionChannel(self.accountId))
        self.csm.air.send(dg)

        # Subscribe to any "staff" channels that the account has access to.
        access = self.account.get('ADMIN_ACCESS', 0)
        if access >= 200:
            # Subscribe to the moderator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_MOD_CHANNEL)
            self.csm.air.send(dg)
        if access >= 400:
            # Subscribe to the administrator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_ADMIN_CHANNEL)
            self.csm.air.send(dg)
        if access >= 500:
            # Subscribe to the system administrator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_SYSADMIN_CHANNEL)
            self.csm.air.send(dg)

        # Now set their sender channel to represent their account affiliation:
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.accountId << 32) # accountId in high 32 bits, 0 in low (no avatar)
        self.csm.air.send(dg)

        # Un-sandbox them!
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_SET_STATE)
        dg.addUint16(2) # ESTABLISHED state. BIG FAT SECURITY RISK!!!
        self.csm.air.send(dg)

        # Update the last login timestamp:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.accountId,
            self.csm.air.dclassesByName['AccountUD'],
            {'LAST_LOGIN': time.ctime(),
             'ACCOUNT_ID': self.databaseId,
             'ADMIN_ACCESS': self.adminAccess,
             'BETA_KEY_QUEST': self.betaKeyQuest})

        # Add a POST_REMOVE to the connection channel to execute the NetMessenger
        # message when the account connection goes RIP on the Client Agent.
        dgcleanup = self.csm.air.netMessenger.prepare('accountDisconnected', [self.accountId])
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.csm.air.send(dg)

        # We're done.
        self.csm.air.writeServerEvent('account-login', clientId=self.target, accId=self.accountId, webAccId=self.databaseId, cookie=self.cookie)
        self.csm.sendUpdateToChannel(self.target, 'acceptLogin', [])
        self.demand('Off')

class CreateAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('CreateAvatarFSM')

    def enterStart(self, dna, index):
        # Basic sanity-checking:
        if index >= 6:
            self.demand('Kill', 'Invalid index specified!')
            return

        if not ToonDNA().isValidNetString(dna):
            self.demand('Kill', 'Invalid DNA specified!')
            return

        self.index = index
        self.dna = dna

        # Okay, we're good to go, let's query their account.
        self.demand('RetrieveAccount')

    def enterRetrieveAccount(self):
        # self.target is the accountId, so:
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.target,
                                             self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize; just in case avList is too long/short:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        # Make sure the index is open:
        if self.avList[self.index]:
            self.demand('Kill', 'This avatar slot is already taken by another avatar!')
            return

        # Okay, there's space, let's create the avatar!
        self.demand('CreateAvatar')

    def enterCreateAvatar(self):
        dna = ToonDNA()
        dna.makeFromNetString(self.dna)
        colorstring = TTLocalizer.NumToColor[dna.headColor]
        animaltype = TTLocalizer.AnimalToSpecies[dna.getAnimal()]
        name = colorstring + ' ' + animaltype

        toonFields = {
            'setName': (name,),
            'WishNameState': WISHNAME_OPEN,
            'WishName': '',
            'setDNAString': (self.dna,),
            'setDISLid': (self.target,)
        }

        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            toonFields,
            self.__handleCreate)

    def __handleCreate(self, avId):
        if not avId:
            self.demand('Kill', 'Database failed to create the new avatar object!')
            return

        self.avId = avId

        self.demand('StoreAvatar')

    def enterStoreAvatar(self):
        # Associate the avatar with the account...
        self.avList[self.index] = self.avId

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target, # i.e. the account ID
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET']},
            self.__handleStoreAvatar)

    def __handleStoreAvatar(self, fields):
        if fields:
            # TODO: delete self.avId
            self.demand('Kill', 'Database failed to associate the new avatar to your account!')
            return

        # Otherwise, we're done!
        self.csm.air.writeServerEvent('avatar-created', avId=self.avId, accId=self.target, dna=self.dna.encode('hex'), slot=self.index)
        self.csm.sendUpdateToAccountId(self.target, 'createAvatarResp', [self.avId])
        self.demand('Off')

class AvatarOperationFSM(OperationFSM):
    # This needs to be overridden.
    POST_ACCOUNT_STATE = 'Off'

    def enterRetrieveAccount(self):
        # Query the account:
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.target,
                                             self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize; just in case avList is too long/short:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        self.demand(self.POST_ACCOUNT_STATE)

class GetAvatarsFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('GetAvatarsFSM')
    POST_ACCOUNT_STATE = 'QueryAvatars'

    def enterStart(self):
        self.demand('RetrieveAccount')

    def enterQueryAvatars(self):
        self.pendingAvatars = set()
        self.avatarFields = {}
        for avId in self.avList:
            if avId:
                self.pendingAvatars.add(avId)

                def response(dclass, fields, avId=avId):
                    if self.state != 'QueryAvatars': return
                    if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
                        self.demand('Kill', "One of the account's avatars is invalid!")
                        return
                    # Since we weren't previously setting the DISLid of an avatar upon creating
                    # a toon, we will check to see if they already have a DISLid value or not.
                    # If they don't, we will set it here.
                    if not fields.has_key('setDISLid'):
                        self.csm.air.dbInterface.updateObject(
                            self.csm.air.dbId,
                            avId,
                            self.csm.air.dclassesByName['DistributedToonUD'],
                            {'setDISLid' : [self.target]}
                        )
                    self.avatarFields[avId] = fields
                    self.pendingAvatars.remove(avId)
                    if not self.pendingAvatars:
                        self.demand('SendAvatars')

                self.csm.air.dbInterface.queryObject(self.csm.air.dbId, avId,
                                                     response)

        if not self.pendingAvatars:
            self.demand('SendAvatars')

    def enterSendAvatars(self):
        potentialAvs = []

        for avId, fields in self.avatarFields.items():
            index = self.avList.index(avId)
            wns = fields.get('WishNameState', WISHNAME_LOCKED)
            name = fields['setName'][0]
            if wns == WISHNAME_OPEN:
                nameState = 1
            elif wns == WISHNAME_PENDING:
                nameState = 2
            elif wns == WISHNAME_APPROVED:
                nameState = 3
                name = fields['WishName']
            elif wns == WISHNAME_REJECTED:
                nameState = 4
            elif wns == WISHNAME_LOCKED:
                nameState = 0
            else:
                self.csm.notify.warning('Avatar %d is in unknown name state %s.' % (avId, wns))
                nameState = 0

            potentialAvs.append([avId, name, fields['setDNAString'][0],
                                 index, nameState])

        self.csm.sendUpdateToAccountId(self.target, 'setAvatars', [potentialAvs])
        self.demand('Off')

# This inherits from GetAvatarsFSM, because the delete operation ends in a
# setAvatars message being sent to the client.
class DeleteAvatarFSM(GetAvatarsFSM):
    notify = directNotify.newCategory('DeleteAvatarFSM')
    POST_ACCOUNT_STATE = 'ProcessDelete'

    def enterStart(self, avId):
        self.avId = avId
        GetAvatarsFSM.enterStart(self)

    def enterProcessDelete(self):
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to delete an avatar not in the account!')
            return

        index = self.avList.index(self.avId)
        self.avList[index] = 0

        avsDeleted = list(self.account.get('ACCOUNT_AV_SET_DEL', []))
        avsDeleted.append([self.avId, int(time.time())])

        estateId = self.account.get('ESTATE_ID', 0)

        if estateId != 0:
            # This assumes that the house already exists, but it shouldn't
            # be a problem if it doesn't.
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                estateId,
                self.csm.air.dclassesByName['DistributedEstateAI'],
                { 'setSlot%dToonId' % index : [0], 'setSlot%dItems' % index : [[]] }
            )

        if self.csm.air.friendsManager:
            self.csm.air.friendsManager.clearList(self.avId)
        else:
            friendsManagerDoId = OtpDoGlobals.OTP_DO_ID_TTR_FRIENDS_MANAGER
            dg = self.csm.air.dclassesByName['TTRFriendsManagerUD'].aiFormatUpdate(
                'clearList', friendsManagerDoId, friendsManagerDoId,
                self.csm.air.ourChannel, [self.avId]
            )
            self.csm.air.send(dg)

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target, # i.e. the account ID
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList,
             'ACCOUNT_AV_SET_DEL': avsDeleted},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET'],
             'ACCOUNT_AV_SET_DEL': self.account['ACCOUNT_AV_SET_DEL']},
            self.__handleDelete)

    def __handleDelete(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to mark the avatar deleted!')
            return
        self.csm.air.writeServerEvent('avatar-deleted', avId=self.avId, accId=self.target)
        self.demand('QueryAvatars')

class SetNameTypedFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNameTypedFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, name):
        self.avId = avId
        self.name = name

        if self.avId:
            self.demand('RetrieveAccount')
            return

        # Hmm, self.avId was 0. Okay, let's just cut to the judging:
        self.demand('CheckName')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'] != WISHNAME_OPEN:
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('CheckName')

    def enterCheckName(self):
        def callback(result=False):
            self.demand('JudgeName', result)

        self.csm.air.rpc.call('checkBlacklistedName', name=self.name,
                              _callback=callback, _errback=callback, _retry=True)

    def enterJudgeName(self, blacklisted):
        status = not blacklisted

        if self.avId and status:
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                self.avId,
                self.csm.air.dclassesByName['DistributedToonUD'],
                {'WishNameState': WISHNAME_PENDING,
                 'WishName': self.name,
                 'WishNameTimestamp': int(time.time())})

        if self.avId:
            self.csm.air.writeServerEvent('avatar-wishname', avId=self.avId, name=self.name)

            # Fire off the information to the webserver:
            self.csm.air.rpc.call('submitAvatarName', avId=self.avId, name=self.name,
                                  _retry=True)

        self.csm.sendUpdateToAccountId(self.target, 'setNameTypedResp', [self.avId, status])
        self.demand('Off')

class SetNamePatternFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNamePatternFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, pattern):
        self.avId = avId
        self.pattern = pattern

        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'] != WISHNAME_OPEN:
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('SetName')

    def enterSetName(self):
        # Render pattern into a string:
        parts = []
        for p,f in self.pattern:
            if p==213: p=212 # Don't allow the name Slappy if they try to add it back in NameMasterEnglish (it will generate a blank name)
            part = self.csm.nameGenerator.nameDictionary.get(p, ('',''))[1]
            if f: part = part[:1].upper() + part[1:]
            else: part = part.lower()
            parts.append(part)

        parts[2] += parts.pop(3) # Merge 2&3 (the last name) as there should be no space.
        while '' in parts: parts.remove('')
        name = ' '.join(parts)

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            {'WishNameState': WISHNAME_LOCKED,
             'WishName': '',
             'setName': (name,)})

        self.csm.air.writeServerEvent('avatar-named', avId=self.avId, name=name)
        self.csm.sendUpdateToAccountId(self.target, 'setNamePatternResp', [self.avId, 1])
        self.demand('Off')

class AcknowledgeNameFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('AcknowledgeNameFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to acknowledge name on an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        # Process the WishNameState change.
        wns = fields['WishNameState']
        wn = fields['WishName']
        name = fields['setName'][0]

        if wns == WISHNAME_APPROVED:
            wns = WISHNAME_LOCKED
            name = wn
            wn = ''
        elif wns == WISHNAME_REJECTED:
            wns = WISHNAME_OPEN
            wn = ''
        else:
            self.demand('Kill', "Tried to acknowledge name on an avatar in %s state!" % wns)
            return

        # Push the change back through:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            {'WishNameState': wns,
             'WishName': wn,
             'setName': (name,)},
            {'WishNameState': fields['WishNameState'],
             'WishName': fields['WishName'],
             'setName': fields['setName']})

        self.csm.sendUpdateToAccountId(self.target, 'acknowledgeAvatarNameResp', [])
        self.demand('Off')

class LoadAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('LoadAvatarFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to play an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatar = fields
        self.demand('SetAvatar')

    def enterSetAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # First, give them a POSTREMOVE to unload the avatar, just in case they
        # disconnect while we're working.
        dgcleanup = PyDatagram()
        dgcleanup.addServerHeader(self.avId, channel, STATESERVER_OBJECT_DELETE_RAM)
        dgcleanup.addUint32(self.avId)
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.csm.air.send(dg)

        # Get the avatar's "true" access. (without "server" bit)
        adminAccess = self.account.get('ADMIN_ACCESS', 0)
        adminAccess = adminAccess - adminAccess % 100

        # Activate the avatar on the DBSS:
        self.csm.air.sendActivate(self.avId, 0, 0,
                                  self.csm.air.dclassesByName['DistributedToonUD'],
                                  {'setAdminAccess': [adminAccess],
                                   'setWantBetaKeyQuest': [self.account.get('BETA_KEY_QUEST', 0)],
                                   'setWebAccountId': [self.account.get('ACCOUNT_ID', 0)]})

        # Next, add them to the avatar channel:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
        dg.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(dg)

        # Now set their sender channel to represent their account affiliation:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.target<<32 | self.avId) # accountId in high 32 bits, avatar in low
        self.csm.air.send(dg)

        # Finally, grant ownership and shut down.
        dg = PyDatagram()
        dg.addServerHeader(self.avId, self.csm.air.ourChannel, STATESERVER_OBJECT_SET_OWNER)
        dg.addChannel(self.csm.GetAccountConnectionChannel(self.target)) # Set ownership channel to the connection's account channel.
        self.csm.air.send(dg)

        # Tell everything that an avatar is coming online!
        friendsList = [x for x, y in self.avatar['setFriendsList'][0]]
        self.csm.air.netMessenger.send('avatarOnline', [self.avId, friendsList])

        # Post-remove for an avatar that disconnects unexpectedly.
        dgcleanup = self.csm.air.netMessenger.prepare('avatarOffline', [self.avId])
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.csm.air.send(dg)

        self.csm.air.writeServerEvent('avatar-chosen', avId=self.avId, accId=self.target)
        self.demand('Off')

class UnloadAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('UnloadAvatarFSM')

    def enterStart(self, avId):
        self.avId = avId

        # We don't even need to query the account, we know the avatar is being played!
        self.demand('UnloadAvatar')

    def enterUnloadAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Fire off the avatarOffline message.
        self.csm.air.netMessenger.send('avatarOffline', [self.avId])

        # Get lost, POST_REMOVES!:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_CLEAR_POST_REMOVES)
        self.csm.air.send(dg)

        # Remove avatar channel:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_CLOSE_CHANNEL)
        dg.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(dg)

        # Reset sender channel:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.target<<32) # accountId in high 32 bits, no avatar in low
        self.csm.air.send(dg)

        # Unload avatar object:
        dg = PyDatagram()
        dg.addServerHeader(self.avId, channel, STATESERVER_OBJECT_DELETE_RAM)
        dg.addUint32(self.avId)
        self.csm.air.send(dg)

        # Done!
        self.csm.air.writeServerEvent('avatar-unload', avId=self.avId)
        self.demand('Off')

# --- ACTUAL CSMUD ---
class ClientServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ClientServicesManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        # These keep track of the connection/account IDs currently undergoing an
        # operation on the CSM. This is to prevent (hacked) clients from firing up more
        # than one operation at a time, which could potentially lead to exploitation
        # of race conditions.
        self.connection2fsm = {}
        self.account2fsm = {}

        # For processing name patterns.
        self.nameGenerator = NameGenerator()

        # Instantiate our account DB interface using config:
        dbtype = config.GetString('accountdb-type', 'local')
        if dbtype == 'local':
            self.accountDB = LocalAccountDB(self)
        elif dbtype == 'remote':
            self.accountDB = RemoteAccountDB(self)
        else:
            self.notify.error('Invalid account DB type configured: %s' % dbtype)

        # Listen out for any accounts that disconnect.
        self.air.netMessenger.accept('accountDisconnected', self, self.__accountDisconnected)

        # This attribute determines if we want to disable logins.
        self.loginsEnabled = True
        # Listen out for any messages that tell us to disable logins.
        self.air.netMessenger.accept('enableLogins', self, self.setLoginEnabled)

    def __accountDisconnected(self, accountId):
        def callback(dclass, fields):
            if dclass != self.air.dclassesByName['AccountUD']:
                return
            webId = fields.get('ACCOUNT_ID')
            self.air.rpc.call('avatarExit', webAccId=webId)
        self.air.dbInterface.queryObject(self.air.dbId, accountId, callback)

    def killConnection(self, connId, reason):
        dg = PyDatagram()
        dg.addServerHeader(connId, self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(122)
        dg.addString(reason)
        self.air.send(dg)

    def killConnectionFSM(self, connId):
        fsm = self.connection2fsm.get(connId)
        if not fsm:
            self.notify.warning('Tried to kill connection %d for duplicate FSM, but none exists!' % connId)
            return
        self.killConnection(connId, 'An operation is already underway: ' + fsm.name)

    def killAccount(self, accountId, reason):
        self.killConnection(self.GetAccountConnectionChannel(accountId), reason)

    def killAccountFSM(self, accountId):
        fsm = self.account2fsm.get(accountId)
        if not fsm:
            self.notify.warning('Tried to kill account %d for duplicate FSM, but none exists!' % accountId)
            return
        self.killAccount(accountId, 'An operation is already underway: ' + fsm.name)

    def runAccountFSM(self, fsmtype, *args):
        sender = self.air.getAccountIdFromSender()

        if not sender:
            self.killAccount(sender, 'Client is not logged in.')

        if sender in self.account2fsm:
            self.killAccountFSM(sender)
            return

        self.account2fsm[sender] = fsmtype(self, sender)
        self.account2fsm[sender].request('Start', *args)

    def setLoginEnabled(self, enable):
        if not enable:
            self.notify.warning('The CSMUD has been told to reject logins! All future logins will now be rejected.')
        self.loginsEnabled = enable

    def login(self, cookie, sig):
        self.notify.debug('Received login cookie %r from %d' % (cookie, self.air.getMsgSender()))

        sender = self.air.getMsgSender()

        if not self.loginsEnabled:
            # Logins are currently disabled... RIP!
            dg = PyDatagram()
            dg.addServerHeader(sender, self.air.ourChannel, CLIENTAGENT_EJECT)
            dg.addUint16(200)
            dg.addString('Logins are currently disabled. Please try again later.')
            self.air.send(dg)

        if sender>>32:
            # Oops, they have an account ID on their connection already!
            self.killConnection(sender, 'Client is already logged in.')
            return

        # Test the signature
        key = config.GetString('csmud-secret', 'streetlamps') + config.GetString('server-version', 'no_version_set') + FIXED_KEY
        computedSig = hmac.new(key, cookie, hashlib.sha256).digest()
        if sig != computedSig:
            self.killConnection(sender, 'The accounts database rejected your cookie')
            return

        if sender in self.connection2fsm:
            self.killConnectionFSM(sender)
            return

        self.connection2fsm[sender] = LoginAccountFSM(self, sender)
        self.connection2fsm[sender].request('Start', cookie)

    def requestAvatars(self):
        self.notify.debug('Received avatar list request from %d' % (self.air.getMsgSender()))
        self.runAccountFSM(GetAvatarsFSM)

    def createAvatar(self, dna, index):
        self.runAccountFSM(CreateAvatarFSM, dna, index)

    def deleteAvatar(self, avId):
        self.runAccountFSM(DeleteAvatarFSM, avId)

    def setNameTyped(self, avId, name):
        self.runAccountFSM(SetNameTypedFSM, avId, name)

    def setNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4):
        self.runAccountFSM(SetNamePatternFSM, avId, [(p1, f1), (p2, f2),
                                                     (p3, f3), (p4, f4)])

    def acknowledgeAvatarName(self, avId):
        self.runAccountFSM(AcknowledgeNameFSM, avId)

    def chooseAvatar(self, avId):
        currentAvId = self.air.getAvatarIdFromSender()
        accountId = self.air.getAccountIdFromSender()
        if currentAvId and avId:
            self.killAccount(accountId, 'A Toon is already chosen!')
            return
        elif not currentAvId and not avId:
            # This isn't really an error, the client is probably just making sure
            # none of its Toons are active.
            return

        if avId:
            self.runAccountFSM(LoadAvatarFSM, avId)
        else:
            self.runAccountFSM(UnloadAvatarFSM, currentAvId)

    def reportPlayer(self, avId, category):
        reporterId = self.air.getAvatarIdFromSender()
        if len(REPORT_REASONS) <= category:
            self.air.writeServerEvent("suspicious", avId=reporterId, issue="Invalid report reason index (%d) sent by avatar." % category)
            return
        self.air.writeServerEvent("player-reported", reporterId=reporterId, avId=avId, category=REPORT_REASONS[category])
        # TODO: RPC call to web to say this person was reported.
        # This will require a database query to fetch the webId associated with the reported player.
        # Either that, or the web can make an RPC call to the server to get webId from avId.