from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.toonbase import TTLocalizer
import PartyGlobals

class DistributedPartyCannonActivityAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyCannonActivityAI")
    
    def __init__(self, air, parent, activityTuple):
        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)
        self.cloudColors = {}
        self.cloudsHit = {}

    def setMovie(self, todo0, todo1):
        pass

    def setLanded(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if avId != toonId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to land someone else!')
            return
        if not avId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to land while not playing the cannon activity!')
            return
        self.toonsPlaying.remove(avId)
        reward = self.cloudsHit[avId] * PartyGlobals.CannonJellyBeanReward
        if reward > PartyGlobals.CannonMaxTotalReward:
            reward = PartyGlobals.CannonMaxTotalReward
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to award beans while not in district!')
            return
        # TODO: Pass a msgId(?) to the client so the client can use whatever localizer it chooses.
        # Ideally, we shouldn't even be passing strings that *should* be localized.
        self.sendUpdateToAvatarId(avId, 'showJellybeanReward', [reward, av.getMoney(), TTLocalizer.PartyCannonResults % (reward, self.cloudsHit[avId])])
        av.addMoney(reward)
        self.sendUpdate('setMovie', [PartyGlobals.CANNON_MOVIE_LANDED, avId])
        del self.cloudsHit[avId]

    def b_setCannonWillFire(self, cannonId, rot, angle, toonId):
        self.toonsPlaying.append(toonId)
        self.cloudsHit[toonId] = 0
        self.sendUpdate('setCannonWillFire', [cannonId, rot, angle])

    def cloudsColorRequest(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'cloudsColorResponse', [self.cloudColors.values()])

    def requestCloudHit(self, cloudId, r, g, b):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to hit cloud in cannon activity they\'re not using!')
            return
        self.cloudColors[cloudId] = [cloudId, r, g, b]
        self.sendUpdate('setCloudHit', [cloudId, r, g, b])
        self.cloudsHit[avId] += 1

    def setToonTrajectoryAi(self, launchTime, x, y, z, h, p, r, vx, vy, vz):
        self.sendUpdate('setToonTrajectory', [self.air.getAvatarIdFromSender(), launchTime, x, y, z, h, p, r, vx, vy, vz])

    def setToonTrajectory(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7, todo8, todo9, todo10):
        pass

    def updateToonTrajectoryStartVelAi(self, vx, vy, vz):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('updateToonTrajectoryStartVel', [avId, vx, vy, vz])

    def updateToonTrajectoryStartVel(self, todo0, todo1, todo2, todo3):
        pass

