from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
import cPickle

class DistributedToonInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonInteriorAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
    
    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block
        
    def d_setZoneIdAndBlock(self, zoneId, block):
        self.sendUpdate('setZoneIdAndBlock', [zoneId, block])
    
    def b_setZoneIdAndBlock(self, zoneId, block):
        self.setZoneIdAndBlock(zoneId, block)
        self.d_setZoneIdAndBlock(zoneId, block)
        
    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def setToonData(self, toonData):
        pass
        
    def getToonData(self):
        return cPickle.dumps(None)

    def setState(self, state):
        self.timeStamp = globalClockDelta.getRealNetworkTime()
        self.state = state
    
    def getState(self):
        return [self.state, self.timeStamp]
        
    def nextSnowmanHeadPart(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            self.notify.warning('avId %d does not exist as an object in the AIRepo.' % avId)
            return False # Avatar does not even exist, water you doin'.
        
        av = self.air.doId2do.get(avId)
        if av.savedCheesyEffect == 14:
            #av.setSystemMessage(0, 'McQuack: You have already completed the snowman head quest!')
            return False # Avatar already has a snowman head.
            
        snowmanHeadInteriors = [
            2740, # TTC, Loopy Lane, Used Firecrackers
            4652, # MML, Alto Avenue, Full Stop Shop
            9608, # DDL, non-HQ street, Cat Nip For Cat Naps
            5710, # DG, Maple Street, Tuft Guy Gym
            1711, # DD, Seaweed Street, Deep-Sea Diner
            3620, # TB, Walrus Way, Skiing Clinic
        ]
        
        snowmanNPCWhispers = {
            snowmanHeadInteriors[0] : 'Smokey Joe',
            snowmanHeadInteriors[1] : 'Patty Pause',
            snowmanHeadInteriors[2] : 'Kathy Nip',
            snowmanHeadInteriors[3] : 'Lars Bicep',
            snowmanHeadInteriors[4] : 'Dinah Down',
            snowmanHeadInteriors[5] : 'Henry the Hazard',
        }
        
        if self.zoneId in snowmanHeadInteriors:
            if not hasattr(self.air, 'snowmanProgress'):
                self.air.snowmanProgress = {}
            
            if str(avId) in self.air.snowmanProgress:
                avProg = self.air.snowmanProgress.get(str(avId))
                if avProg == snowmanHeadInteriors[-1]:
                    #av.d_setSystemMessage(0, 'McQuack: You have already completed the snowman head quest!')
                    return False # They have already completed the quest.
                    
                avNextProg = snowmanHeadInteriors[snowmanHeadInteriors.index(avProg) + 1]
                
                if avNextProg == self.zoneId:
                    self.air.snowmanProgress[str(avId)] = avNextProg
                    shopsLeft = len(snowmanHeadInteriors) - (snowmanHeadInteriors.index(avNextProg) + 1)
                    if shopsLeft > 1:
                        av.d_setSystemMessage(0, '%s: Merry Christmas, %s! You have %s shops left.' % (snowmanNPCWhispers.get(self.zoneId), av.getName(), str(shopsLeft)))
                    elif shopsLeft == 1:
                        av.d_setSystemMessage(0, '%s: Merry Christmas, %s! You have %s shop left.' % (snowmanNPCWhispers.get(self.zoneId), av.getName(), str(shopsLeft)))
                    else:
                        av.d_setSystemMessage(0, '%s: Merry Christmas, %s!' % (snowmanNPCWhispers.get(self.zoneId), av.getName()))
                    
                if avNextProg == snowmanHeadInteriors[-1]:
                    av.b_setCheesyEffect(14, 0, 0)
                    av.d_setSystemMessage(0, 'McQuack: Congratulations on finding all the buildings. Enjoy your snowman head!')
            else:
                # start of quest
                self.air.snowmanProgress[str(avId)] = snowmanHeadInteriors[0]
                shopsLeft = len(snowmanHeadInteriors) - 1
                av.d_setSystemMessage(0, '%s: Merry Christmas, %s! You have %s shops left.' % (snowmanNPCWhispers.get(self.zoneId), av.getName(), str(shopsLeft)))
