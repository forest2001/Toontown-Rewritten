import pymongo
# For naming constants:
from toontown.uberdog.ClientServicesManagerUD import *
# For renaming Toons with rejected names:
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import TTLocalizer

class ToontownRPCHandler:
    def __init__(self, air):
        self.air = air

    def rpc_ping(self, request, data):
        """For testing purposes: This just echos back the provided data."""
        return data

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
