from pandac.PandaModules import *
from toontown.battle.BattleProps import *
from toontown.battle.BattleSounds import *
from toontown.distributed.ToontownMsgTypes import *
from direct.gui.DirectGui import cleanupDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from toontown.battle import BattlePlace
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.task import Task
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.battle import BattleParticles
from toontown.building import Elevator
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toon.Toon import teleportDebug
from toontown.estate import HouseGlobals
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import *
from otp.nametag import NametagGlobals
visualizeZones = base.config.GetBool('visualize-zones', 0)

class Street(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('Street')

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.fsm = ClassicFSM.ClassicFSM('Street', [State.State('start', self.enterStart, self.exitStart, ['walk',
          'tunnelIn',
          'doorIn',
          'teleportIn',
          'elevatorIn']),
         State.State('walk', self.enterWalk, self.exitWalk, ['push',
          'sit',
          'stickerBook',
          'WaitForBattle',
          'battle',
          'DFA',
          'trialerFA',
          'doorOut',
          'elevator',
          'tunnelIn',
          'tunnelOut',
          'teleportOut',
          'quest',
          'stopped',
          'fishing',
          'purchase',
          'died']),
         State.State('sit', self.enterSit, self.exitSit, ['walk']),
         State.State('push', self.enterPush, self.exitPush, ['walk']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'push',
          'sit',
          'battle',
          'DFA',
          'trialerFA',
          'doorOut',
          'elevator',
          'tunnelIn',
          'tunnelOut',
          'WaitForBattle',
          'teleportOut',
          'quest',
          'stopped',
          'fishing',
          'purchase']),
         State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle', 'walk']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
         State.State('doorIn', self.enterDoorIn, self.exitDoorIn, ['walk']),
         State.State('doorOut', self.enterDoorOut, self.exitDoorOut, ['walk']),
         State.State('elevatorIn', self.enterElevatorIn, self.exitElevatorIn, ['walk']),
         State.State('elevator', self.enterElevator, self.exitElevator, ['walk']),
         State.State('trialerFA', self.enterTrialerFA, self.exitTrialerFA, ['trialerFAReject', 'DFA']),
         State.State('trialerFAReject', self.enterTrialerFAReject, self.exitTrialerFAReject, ['walk']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject', 'teleportOut', 'tunnelOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walk']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk',
          'teleportOut',
          'quietZone',
          'WaitForBattle',
          'battle']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn', 'quietZone', 'WaitForBattle']),
         State.State('died', self.enterDied, self.exitDied, ['quietZone']),
         State.State('tunnelIn', self.enterTunnelIn, self.exitTunnelIn, ['walk']),
         State.State('tunnelOut', self.enterTunnelOut, self.exitTunnelOut, ['final']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['teleportIn']),
         State.State('quest', self.enterQuest, self.exitQuest, ['walk', 'stopped']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk']),
         State.State('fishing', self.enterFishing, self.exitFishing, ['walk']),
         State.State('purchase', self.enterPurchase, self.exitPurchase, ['walk']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')
        self.parentFSM = parentFSM
        self.tunnelOriginList = []
        self.elevatorDoneEvent = 'elevatorDone'
        self.eventLights = []
        self.visInterestHandle = None
        self.zoneInterestHandle = None
        self.visZones = []
        self.visInterestChanged = False

    def enter(self, requestStatus, visibilityFlag = 1, arrowsOn = 1):
        teleportDebug(requestStatus, 'Street.enter(%s)' % (requestStatus,))
        self._ttfToken = None
        self.fsm.enterInitialState()
        base.playMusic(self.loader.music, looping=1, volume=0.8)
        self.loader.geom.reparentTo(render)
        if visibilityFlag:
            self.visibilityOn()
        base.localAvatar.setGeom(self.loader.geom)
        base.localAvatar.setOnLevelGround(1)
        self._telemLimiter = TLGatherAllAvs('Street', RotationLimitToH)
        NametagGlobals.setMasterArrowsOn(arrowsOn) #TODO: fix me cfsworks

        def __lightDecorationOn__():
            geom = base.cr.playGame.getPlace().loader.geom
            self.loader.hood.eventLights = geom.findAllMatches('**/*light*')
            self.loader.hood.eventLights += geom.findAllMatches('**/*lamp*')
            self.loader.hood.eventLights += geom.findAllMatches('**/prop_snow_tree*')
            self.loader.hood.eventLights += geom.findAllMatches('**/prop_tree*')
            self.loader.hood.eventLights += geom.findAllMatches('**/*christmas*')
            for light in self.loader.hood.eventLights:
                light.setColorScaleOff(1)

        newsManager = base.cr.newsManager
        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            #Halloween Event
            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds or ToontownGlobals.SPOOKY_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:
                lightsOff = Sequence(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(0.55, 0.55, 0.65, 1)), Func(self.loader.hood.startSpookySky))
                lightsOff.start()
            else:
                self.loader.hood.startSky()
                lightsOn = LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(1, 1, 1, 1))
                lightsOn.start()
            #Christmas Event
            if (ToontownGlobals.WINTER_DECORATIONS in holidayIds or ToontownGlobals.WACKY_WINTER_DECORATIONS in holidayIds) and self.loader.hood.snowySkyFile:
                lightsOff = Sequence(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(0.7, 0.7, 0.8, 1)), Func(self.loader.hood.startSnowySky), Func(__lightDecorationOn__))
                lightsOff.start()
                self.snowEvent = BattleParticles.loadParticleFile('snowdisk.ptf')
                self.snowEvent.setPos(0, 30, 10)
                #2 and 3 are only for the blizzard event and should be removed
                self.snowEvent2 = BattleParticles.loadParticleFile('snowdisk.ptf')
                self.snowEvent2.setPos(0, 10, 10)
                self.snowEvent3 = BattleParticles.loadParticleFile('snowdisk.ptf')
                self.snowEvent3.setPos(0, 20, 5)
                self.snowEventRender = base.cr.playGame.hood.loader.geom.attachNewNode('snowRender')
                self.snowEventRender.setDepthWrite(2)
                self.snowEventRender.setBin('fixed', 1)
                self.snowEventFade = None
                self.snowEvent.start(camera, self.snowEventRender)
                #2 and 3 are only for the blizzard event and should be removed
                self.snowEvent2.start(camera, self.snowEventRender)
                self.snowEvent3.start(camera, self.snowEventRender)
            else:
                self.loader.hood.startSky()
                lightsOn = LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(1, 1, 1, 1))
                lightsOn.start()
        else:
            self.loader.hood.startSky()
            lightsOn = LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(1, 1, 1, 1))
            lightsOn.start()
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        self.enterZone(requestStatus['zoneId'])
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.loader.nodeList, self.zoneId)
        if self.zoneId:
            self.zoneInterestHandle = base.cr.addInterest(base.localAvatar.defaultShard, [self.zoneId-(self.zoneId%100)], 'global_streetVis')
        self.fsm.request(requestStatus['how'], [requestStatus])
        self.replaceStreetSignTextures()
        return

    def exit(self, visibilityFlag = 1):
        if visibilityFlag:
            self.visibilityOff()
        self.loader.geom.reparentTo(hidden)
        self._telemLimiter.destroy()
        del self._telemLimiter

        def __lightDecorationOff__():
            for light in self.eventLights:
                light.reparentTo(hidden)

        newsManager = base.cr.newsManager
        NametagGlobals.setMasterArrowsOn(0) #TODO: cfsworks fix me plx
        self.loader.hood.stopSky()
        self.loader.music.stop()
        base.localAvatar.setGeom(render)
        base.localAvatar.setOnLevelGround(0)
        if not self.visInterestHandle is None:
            base.cr.removeInterest(self.visInterestHandle)
        if not self.zoneInterestHandle is None:
            base.cr.removeInterest(self.zoneInterestHandle)

    def load(self):
        BattlePlace.BattlePlace.load(self)
        self.parentFSM.getStateNamed('street').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('street').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.enterZone(None)
        cleanupDialog('globalDialog')
        self.ignoreAll()
        BattlePlace.BattlePlace.unload(self)
        return

    def enterElevatorIn(self, requestStatus):
        self._eiwbTask = taskMgr.add(Functor(self._elevInWaitBldgTask, requestStatus['bldgDoId']), uniqueName('elevInWaitBldg'))

    def _elevInWaitBldgTask(self, bldgDoId, task):
        bldg = base.cr.doId2do.get(bldgDoId)
        if bldg:
            if bldg.elevatorNodePath is not None:
                self._enterElevatorGotElevator()
                return Task.done
        return Task.cont

    def _enterElevatorGotElevator(self):
        messenger.send('insideVictorElevator')

    def exitElevatorIn(self):
        taskMgr.remove(self._eiwbTask)

    def enterElevator(self, distElevator):
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed('elevator'), self.elevatorDoneEvent, distElevator)
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        self.fsm.request('elevator', [distElevator])
        return None

    def handleElevatorDone(self, doneStatus):
        self.notify.debug('handling elevator done event')
        where = doneStatus['where']
        if where == 'reject':
            if hasattr(base.localAvatar, 'elevatorNotifier') and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where in ('suitInterior', 'cogdoInterior'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleElevatorDone')

    def enterTunnelIn(self, requestStatus):
        self.enterZone(requestStatus['zoneId'])
        BattlePlace.BattlePlace.enterTunnelIn(self, requestStatus)

    def enterTeleportIn(self, requestStatus):
        teleportDebug(requestStatus, 'Street.enterTeleportIn(%s)' % (requestStatus,))
        zoneId = requestStatus['zoneId']
        self._ttfToken = self.addSetZoneCompleteCallback(Functor(self._teleportToFriend, requestStatus))
        self.enterZone(zoneId)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    def _teleportToFriend(self, requestStatus):
        avId = requestStatus['avId']
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        if avId != -1:
            if not base.cr.doId2do.has_key(avId):
                teleportDebug(requestStatus, "couldn't find friend %s" % avId)
                handle = base.cr.identifyFriend(avId)
                requestStatus = {'how': 'teleportIn',
                 'hoodId': hoodId,
                 'zoneId': hoodId,
                 'shardId': None,
                 'loader': 'safeZoneLoader',
                 'where': 'playground',
                 'avId': avId}
                self.fsm.request('final')
                self.__teleportOutDone(requestStatus)
        return

    def exitTeleportIn(self):
        self.removeSetZoneCompleteCallback(self._ttfToken)
        self._ttfToken = None
        BattlePlace.BattlePlace.exitTeleportIn(self)
        return

    def enterTeleportOut(self, requestStatus):
        if requestStatus.has_key('battle'):
            self.__teleportOutDone(requestStatus)
        else:
            BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        shardId = requestStatus['shardId']
        if hoodId == self.loader.hood.id and shardId == None:
            if zoneId == self.zoneId:
                self.fsm.request('teleportIn', [requestStatus])
            elif requestStatus['where'] == 'street' and ZoneUtil.getBranchZone(zoneId) == self.loader.branchZone:
                self.fsm.request('quietZone', [requestStatus])
            else:
                self.doneStatus = requestStatus
                messenger.send(self.doneEvent)
        elif hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
        return

    def exitTeleportOut(self):
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def goHomeFailed(self, task):
        self.notifyUserGoHomeFailed()
        self.ignore('setLocalEstateZone')
        self.doneStatus['avId'] = -1
        self.doneStatus['zoneId'] = self.getZoneId()
        self.fsm.request('teleportIn', [self.doneStatus])
        return Task.done

    def renameFloorPolys(self, nodeList):
        for i in nodeList:
            collNodePaths = i.findAllMatches('**/+CollisionNode')
            numCollNodePaths = collNodePaths.getNumPaths()
            visGroupName = i.node().getName()
            for j in range(numCollNodePaths):
                collNodePath = collNodePaths.getPath(j)
                bitMask = collNodePath.node().getIntoCollideMask()
                if bitMask.getBit(1):
                    collNodePath.node().setName(visGroupName)

    def hideAllVisibles(self):
        for i in self.loader.nodeList:
            i.stash()

    def showAllVisibles(self):
        for i in self.loader.nodeList:
            i.unstash()

    def visibilityOn(self):
        self.hideAllVisibles()
        self.accept('on-floor', self.enterZone)

    def visibilityOff(self):
        self.ignore('on-floor')
        self.showAllVisibles()

    def addVisInterest(self, zone):
        self.notify.debug('addVisInterest zone=%i'%zone)
        self.visZones.append(zone)
        self.visInterestChanged = True

    def removeVisInterest(self, zone):
        self.notify.debug('removeVisInterest zone=%i'%zone)
        try:
            self.visZones.remove(zone)
            self.visInterestChanged = True
        except ValueError: #item was not in the list
            self.notify.warning('Street.removeVisInterest called on zone %i that isn\'t in interest' % zone)
    
    def updateVisInterest(self):
        if self.visInterestChanged:
            self.notify.debug('updateVisInterest zones=' + str(self.visZones) + ' handle=' +str(self.visInterestHandle))
            self.visInterestChanged = False
            if self.visInterestHandle is None:
                if len(self.visZones) > 0:
                    self.visInterestHandle = base.cr.addInterest(base.localAvatar.defaultShard, self.visZones, 'streetVis')
            else:
                base.cr.alterInterest(self.visInterestHandle, base.localAvatar.defaultShard, self.visZones)

    def doEnterZone(self, newZoneId):
        if self.zoneId != None:
            for i in self.loader.nodeDict[self.zoneId]:
                if newZoneId:
                    if i not in self.loader.nodeDict[newZoneId]:
                        self.loader.fadeOutDict[i].start()
                        self.loader.exitAnimatedProps(i)
                        self.removeVisInterest(self.loader.nodeToZone[i])
                else:
                    self.removeVisInterest(self.loader.nodeToZone[i])
                    i.stash()
                    self.loader.exitAnimatedProps(i)

        if newZoneId != None:
            for i in self.loader.nodeDict[newZoneId]:
                if self.zoneId:
                    if i not in self.loader.nodeDict[self.zoneId]:
                        self.loader.fadeInDict[i].start()
                        self.loader.enterAnimatedProps(i)
                        self.addVisInterest(self.loader.nodeToZone[i])
                else:
                    if self.loader.fadeOutDict[i].isPlaying():
                        self.loader.fadeOutDict[i].finish()
                    if self.loader.fadeInDict[i].isPlaying():
                        self.loader.fadeInDict[i].finish()
                    self.loader.enterAnimatedProps(i)
                    i.unstash()
                    self.addVisInterest(self.loader.nodeToZone[i])

        self.updateVisInterest()
        if newZoneId != self.zoneId:
            if visualizeZones:
                if self.zoneId != None:
                    self.loader.zoneDict[self.zoneId].clearColor()
                if newZoneId != None:
                    self.loader.zoneDict[newZoneId].setColor(0, 0, 1, 1, 100)
            if newZoneId != None:
                base.cr.sendSetZoneMsg(newZoneId)
                self.notify.debug('Entering Zone %d' % newZoneId)
            self.zoneId = newZoneId
        geom = base.cr.playGame.getPlace().loader.geom
        self.eventLights = geom.findAllMatches('**/*light*')
        self.eventLights += geom.findAllMatches('**/*lamp*')
        self.eventLights += geom.findAllMatches('**/prop_snow_tree*')
        self.eventLights += geom.findAllMatches('**/prop_tree*')
        self.eventLights += geom.findAllMatches('**/*christmas*')
        for light in self.eventLights:
            light.setColorScaleOff(1)
        return

    def replaceStreetSignTextures(self):
        if not hasattr(base.cr, 'playGame'):
            return
        place = base.cr.playGame.getPlace()
        if place is None:
            return
        geom = base.cr.playGame.getPlace().loader.geom
        signs = geom.findAllMatches('**/*tunnelAheadSign*;+s')
        if signs.getNumPaths() > 0:
            streetSign = base.cr.streetSign
            signTexturePath = streetSign.StreetSignBaseDir + '/' + streetSign.StreetSignFileName
            loaderTexturePath = Filename(str(signTexturePath))
            alphaPath = 'phase_4/maps/tt_t_ara_gen_tunnelAheadSign_a.rgb'
            inDreamland = False
            if place.zoneId and ZoneUtil.getCanonicalHoodId(place.zoneId) == ToontownGlobals.DonaldsDreamland:
                inDreamland = True
            alphaPath = 'phase_4/maps/tt_t_ara_gen_tunnelAheadSign_a.rgb'
            if Filename(signTexturePath).exists():
                signTexture = loader.loadTexture(loaderTexturePath, alphaPath)
            for sign in signs:
                if Filename(signTexturePath).exists():
                    sign.setTexture(signTexture, 1)
                if inDreamland:
                    sign.setColorScale(0.525, 0.525, 0.525, 1)

        return
