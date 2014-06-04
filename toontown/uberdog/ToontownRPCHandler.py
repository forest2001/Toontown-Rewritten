import pymongo
# For listShards:
from toontown.distributed.ShardStatus import ShardStatusReceiver
# For naming constants:
from toontown.uberdog.ClientServicesManagerUD import *
# For renaming Toons with rejected names:
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import TTLocalizer
# For system message:
from otp.distributed import OtpDoGlobals

class ToontownRPCHandler:
    def __init__(self, air):
        self.air = air

        self.shardStatus = ShardStatusReceiver(self.air)

    def rpc_ping(self, request, data):
        """For testing purposes: This just echos back the provided data."""
        return data

    ### SHARD MANAGEMENT ###
    def rpc_listShards(self, request):
        return self.shardStatus.getShards()

    def rpc_closeDistrict(self, request, districtId):
        """Sets a district to unavailable, by districtId."""
        dclass = self.air.dclassesByName['ToontownDistrictAI']
        dg = dclass.aiFormatUpdate('rpcSetAvailable', districtId, districtId,
                                    self.air.ourChannel, [0])
        self.air.send(dg)

    ### UBERDOG MANAGEMENT ###
    def rpc_setEnableLogins(self, request, enable):
        """
        Tells the ClientServicesManagerUD to enable/disable all logins.
        Also tells the CSMUD what "disconnect" message to display (only has effect
        if logins are disabled).
        """
        self.air.netMessenger.send('enableLogins', [enable])

    ### GENERAL INFORMATION ###
    def rpc_getGSIDByAccount(self, request, accountId):
        """Gets the GSID for a given webserver account ID, or null if invalid."""
        account = self.air.mongodb.astron.objects.find_one(
            {'dclass':'Account', 'fields.ACCOUNT_ID': accountId})

        if account:
            return account['_id']

    def rpc_getAccountByGSID(self, request, gsId):
        """Gets the account ID associated to a particular GSID, or null if invalid."""
        account = self.air.mongodb.astron.objects.find_one({'_id': gsId})

        if account and account.get('dclass') == 'Account':
            return account.get('fields',{}).get('ACCOUNT_ID')

    def rpc_getAccountByAvatarID(self, request, avId):
        """Gets the account ID associated to a particular avatar (account), or null if invalid."""
        def callback(dclass, fields):
            if dclass is None:
                return request.result(None)
            if dclass.getName() is None:
                return request.result(None)

            return request.result(self.rpc_getAccountByGSID(request, fields.get('setDISLid',0)[0]))

        self.air.dbInterface.queryObject(self.air.dbId, avId, callback)

        return request

    def rpc_getAvatarsForGSID(self, request, gsId):
        """Gets the set of avatars (Toons) that exist on a given gsId, or null if invalid."""

        def callback(dclass, fields):
            if dclass is None:
                return request.result(None)

            if dclass.getName() is None:
                return request.result(None)

            request.result(fields.get('ACCOUNT_AV_SET'))

        self.air.dbInterface.queryObject(self.air.dbId, gsId, callback)

        return request

    ### NAME REVIEW ###
    def rpc_listPendingNames(self, request, count=50):
        """Returns up to 50 pending names, sorted by time spent in the queue.

        It is recommended that the name moderation app call this periodically
        to update its database, in order to ensure that no names got lost.
        """

        cursor = self.air.mongodb.astron.objects.find({'fields.WishNameState': WISHNAME_PENDING})

        cursor.sort('fields.WishNameTimestamp', pymongo.ASCENDING)
        cursor.limit(count)

        result = []
        for item in cursor:
            obj = {
                'avId': item['_id'],
                'name': item['fields']['WishName'],
                'time': item['fields']['WishNameTimestamp']
            }
            result.append(obj)

        return result

    def rpc_approveName(self, request, avId, name):
        """Approves the name of the specified avatar.
        For security, the name must be submitted again.

        On success, returns null.
        On failure, comes back with a JSON error. The failure codes are:
        -100: avId invalid
        -101: avId not in the "pending name approval" state
        -102: name does not match
        """

        def callback(fields):
            if fields is None:
                request.result(None)
            elif fields == {}:
                request.error(-100, 'avId invalid')
            elif fields.get('WishNameState') != WISHNAME_PENDING:
                request.error(-101, 'avId not in the "pending name approval" state')
            elif fields.get('WishName') != name:
                request.error(-102, 'name does not match')
            else:
                request.error(-1, 'Unexpected database failure')

        dclass = self.air.dclassesByName['DistributedPlayerAI']

        self.air.dbInterface.updateObject(self.air.dbId, avId, dclass,
                                          {'WishNameState': WISHNAME_APPROVED,
                                           'WishName': name},
                                          {'WishNameState': WISHNAME_PENDING,
                                           'WishName': name},
                                          callback)

        return request

    def rpc_rejectName(self, request, avId):
        """Rejects the name of the specified avatar.
        If the avatar already has a valid name, this will reset them back to
        their default 'Color Species' name (i.e. this call will have the same
        effect as the ~badName magic word).

        On success, returns null.
        On failure, comes back with a JSON error:
        -100: avId invalid
        """

        def callback(dclass, fields):
            if dclass is None or dclass.getName() != 'DistributedToon':
                return request.error(-100, 'avId invalid')

            dnaString = fields['setDNAString'][0]
            dna = ToonDNA()
            dna.makeFromNetString(dnaString)
            colorstring = TTLocalizer.NumToColor[dna.headColor]
            animaltype = TTLocalizer.AnimalToSpecies[dna.getAnimal()]
            name = colorstring + ' ' + animaltype

            dg = dclass.aiFormatUpdate('setName', avId, avId,
                                       self.air.ourChannel, [name])
            self.air.send(dg)
            dg = dclass.aiFormatUpdate('WishNameState', avId, avId,
                                       self.air.ourChannel, WISHNAME_REJECTED)
            self.air.send(dg)

            request.result(None)

        self.air.dbInterface.queryObject(self.air.dbId, avId, callback)

        return request

    def rpc_openName(self, request, avId):
        """Allows name changes by "opening up" the name of a specified avatar.
        This causes the "Name your Toon!" button to appear on the PAT screen,
        allowing users to submit a different name.

        On success, returns null.
        On failure, comes back with a JSON error:
        -100: avId invalid
        """

        def callback(dclass, fields):
            if fields is None or dclass.getName() != 'DistributedToon':
                return request.error(-100, 'avId invalid')

            self.air.dbInterface.updateObject(self.air.dbId, avId, dclass,
                                              {'WishNameState': WISHNAME_OPEN})

            return request.result(None)

        self.air.dbInterface.queryObject(self.air.dbId, avId, callback)

        return request

    def rpc_changeName(self, request, avId, name):
        """Changes the name of a Toon.
        This will also clear any name-approval status.

        On success, returns null.
        On failure, comes back with a JSON error:
        -100: avId invalid
        """

        def callback(dclass, fields):
            if fields is None or dclass.getName() != 'DistributedToon':
                return request.error(-100, 'avId invalid')

            dg = dclass.aiFormatUpdate('setName', avId, avId,
                                       self.air.ourChannel, [name])
            self.air.send(dg)
            dg = dclass.aiFormatUpdate('WishNameState', avId, avId,
                                       self.air.ourChannel, WISHNAME_LOCKED)
            self.air.send(dg)

            return request.result(None)

        self.air.dbInterface.queryObject(self.air.dbId, avId, callback)

        return request

    ### ADMIN MESSAGES AND KICKS ###
    def rpc_kickChannel(self, request, channel, code, reason):
        """Kicks any users whose CAs are subscribed to a particular channel.

        This always returns null.
        """

        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(code)
        dg.addString(reason)
        self.air.send(dg)

    def rpc_kickGSID(self, request, gsId, code, reason):
        """Kicks a particular user, by GSID.

        This always returns null.
        """

        channel = gsId + (1003L << 32)
        return self.rpc_kickChannel(request, channel, code, reason)

    def rpc_kickAvatar(self, request, avId, code, reason):
        """Kicks a particular user, by avId.

        This always returns null.
        """

        channel = avId + (1001L << 32)
        return self.rpc_kickChannel(request, channel, code, reason)

    def rpc_kickShard(self, request, shardId, code, reason):
        """Kicks all clients in a particular shard.

        This always returns null.
        """

        # Get doId of the district object:
        districtId = shardId + 1
        # Get channel of the uberzone:
        channel = districtId << 32 | 2

        return self.rpc_kickChannel(request, channel, code, reason)

    def rpc_kickAll(self, request, code, reason):
        """Kicks all clients.

        This always returns null.
        """

        channel = 10 # The Astron "all clients" channel.
        return self.rpc_kickChannel(request, channel, code, reason)

    def rpc_messageChannel(self, request, channel, code, params):
        """Messages any users whose CAs are subscribed to a particular channel.

        'code' is the system-message code for localization.
        'params' is an array of parameters used by that system message.

        To send a raw message as-is, use code 0 and put the message as the only
        item in the params array: (..., 0, ["Hello!"])

        This always returns null.
        """

        dclass = self.air.dclassesByName['ClientServicesManagerUD']
        dg = dclass.aiFormatUpdate('systemMessage',
                                   OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                   channel, self.air.ourChannel, [code, params])
        self.air.send(dg)

    def rpc_messageGSID(self, request, gsId, code, params):
        """Messages a particular user, by GSID.

        'code' is the system-message code for localization.
        'params' is an array of parameters used by that system message.

        To send a raw message as-is, use code 0 and put the message as the only
        item in the params array: (..., 0, ["Hello!"])

        This always returns null.
        """

        channel = gsId + (1003L << 32)
        return self.rpc_messageChannel(request, channel, code, params)

    def rpc_messageAvatar(self, request, avId, code, params):
        """Messages a particular user, by avId.

        'code' is the system-message code for localization.
        'params' is an array of parameters used by that system message.

        To send a raw message as-is, use code 0 and put the message as the only
        item in the params array: (..., 0, ["Hello!"])

        This always returns null.
        """

        channel = avId + (1001L << 32)
        return self.rpc_messageChannel(request, channel, code, params)

    def rpc_messageShard(self, request, shardId, code, params):
        """Messages all clients in a particular shard.

        'code' is the system-message code for localization.
        'params' is an array of parameters used by that system message.

        To send a raw message as-is, use code 0 and put the message as the only
        item in the params array: (..., 0, ["Hello!"])

        This always returns null.
        """

        # Get doId of the district object:
        districtId = shardId + 1
        # Get channel of the uberzone:
        channel = districtId << 32 | 2

        return self.rpc_messageChannel(request, channel, code, params)

    def rpc_messageAll(self, request, code, params):
        """Messages all clients.

        'code' is the system-message code for localization.
        'params' is an array of parameters used by that system message.

        To send a raw message as-is, use code 0 and put the message as the only
        item in the params array: (..., 0, ["Hello!"])

        This always returns null.
        """

        channel = 10 # The Astron "all clients" channel.
        return self.rpc_messageChannel(request, channel, code, params)
