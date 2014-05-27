import time
from panda3d.core import *

# If we don't have PSUTIL, don't return system statistics.
try:
    from psutil import cpu_percent, virtual_memory
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

shard_status_interval = ConfigVariableInt(
    'shard-status-interval', 20,
    'How often to send shard status update messages.')

shard_status_timeout = ConfigVariableInt(
    'shard-status-timeout', 30,
    'The maximum time between receiving shard status update messages before'
    ' the receiver assumes the shard is no longer online.')


class ShardStatusSender:
    def __init__(self, air):
        self.air = air

        self.interval = None

    def start(self):
        # Set the average frame rate interval to match shard status interval.
        globalClock.setAverageFrameRateInterval(shard_status_interval.getValue())

        # Prepare an "offline status" to register as a postremove:
        offlineStatus = {'channel': self.air.ourChannel,
                         'offline': True
                        }
        dg = self.air.netMessenger.prepare('shardStatus', [offlineStatus])
        self.air.addPostRemove(dg)

        # Fire off the first status, which also starts the interval:
        self.sendStatus()

    def sendStatus(self):
        status = {'channel': self.air.ourChannel,
                  'districtId': self.air.distributedDistrict.doId,
                  'districtName': self.air.distributedDistrict.name,
                  'population': self.air.districtStats.getAvatarCount(),
                  'avg-frame-rate': round(globalClock.getAverageFrameRate(), 5),
                 }
        if HAS_PSUTIL:
            status['cpu-usage'] = cpu_percent(interval=None, percpu=True)
            status['mem-usage'] = virtual_memory().percent

        self.air.netMessenger.send('shardStatus', [status])

        # Fire up another interval:
        if self.interval is not None:
            self.interval.remove()

        self.interval = taskMgr.doMethodLater(
            shard_status_interval.getValue(), self.__interval,
            'ShardStatusInterval')

    def __interval(self, task):
        self.interval = None # So we don't get removed twice.

        self.sendStatus()

        return task.done

class ShardStatusReceiver:
    def __init__(self, air):
        self.air = air

        self.shards = {}

        self.air.netMessenger.accept('shardStatus', self, self._handleStatus)

    def _handleStatus(self, status):
        channel = status.get('channel')
        if channel is None:
            return # ???

        if status.get('offline'):
            if channel in self.shards:
                del self.shards[channel]
            return

        # Bind a timestamp so we can filter:
        status['lastSeen'] = int(time.time())

        self.shards[channel] = status

    def getShards(self):
        # Calculate the "expiry time" -- shards seen before this time are
        # ignored.
        expiryTime = int(time.time()) - shard_status_timeout.getValue()

        result = []
        for shard in self.shards.values():
            if shard['lastSeen'] < expiryTime:
                continue
            result.append(shard)

        return result
