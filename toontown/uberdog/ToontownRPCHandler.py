import pymongo
# For naming constants:
from toontown.uberdog.ClientServicesManagerUD import *

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
