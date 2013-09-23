from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectLabel import *
from direct.gui.DirectButton import *
from direct.showbase import BulletinBoardWatcher
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPGlobals
from direct.interval.IntervalGlobal import *
from RaceGag import RaceGag
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import ToonHeadFrame
from toontown.racing.KartDNA import InvalidEntry, getAccessory, getDefaultColor
from pandac.PandaModules import CardMaker, OrthographicLens, LineSegs
from direct.distributed import DistributedSmoothNode
from math import fmod
from math import sqrt
from RaceGUI import RaceGUI
import RaceGlobals
from direct.task.Task import Task
from toontown.hood import SkyUtil
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.battle.BattleProps import *
from toontown.minigame import MinigameRulesPanel
from toontown.racing import Piejectile
from toontown.racing import EffectManager
from toontown.racing import PiejectileManager

class DistributedRace(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRace')
    ReadyPost = 'RaceReady'
    WinEvent = 'RaceWinEvent'
    BGM_BaseDir = 'phase_6/audio/bgm/'
    SFX_BaseDir = 'phase_6/audio/sfx/'
    SFX_StartBoop = SFX_BaseDir + 'KART_raceStart1.mp3'
    SFX_StartBoop2 = SFX_BaseDir + 'KART_raceStart2.mp3'
    SFX_Applause = SFX_BaseDir + 'KART_Applause_%d.mp3'

    def __init__(self, cr):
        self.qbox = loader.loadModel('phase_6/models/karting/qbox')
        self.boostArrowTexture = loader.loadTexture('phase_6/maps/boost_arrow.jpg', 'phase_6/maps/boost_arrow_a.rgb')
        self.boostArrowTexture.setMinfilter(Texture.FTLinear)
        DistributedObject.DistributedObject.__init__(self, cr)
        self.kartMap = {}
        self.fsm = ClassicFSM.ClassicFSM('Race', [State.State('join', self.enterJoin, self.exitJoin, ['prep', 'leave']),
         State.State('prep', self.enterPrep, self.exitPrep, ['tutorial', 'leave']),
         State.State('tutorial', self.enterTutorial, self.exitTutorial, ['start', 'waiting', 'leave']),
         State.State('waiting', self.enterWaiting, self.exitWaiting, ['start', 'leave']),
         State.State('start', self.enterStart, self.exitStart, ['racing', 'leave']),
         State.State('racing', self.enterRacing, self.exitRacing, ['finished', 'leave']),
         State.State('finished', self.enterFinished, self.exitFinished, ['leave']),
         State.State('leave', self.enterLeave, self.exitLeave, [])], 'join', 'leave')
        self.gui = RaceGUI(self)
        base.race = self
        self.currT = 0
        self.currLapT = 0
        self.currGag = 0
        self.tdelay = 0
        self.finished = False
        self.thrownGags = []
        self.effectManager = EffectManager.EffectManager()
        self.piejectileManager = PiejectileManager.PiejectileManager()
        self.lastTimeUpdate = globalClock.getFrameTime()
        self.initGags()
        self.canShoot = True
        self.isUrbanTrack = False
        self.hasFog = False
        self.dummyNode = None
        self.fog = None
        self.bananaSound = base.loadSfx('phase_6/audio/sfx/KART_tossBanana.mp3')
        self.anvilFall = base.loadSfx('phase_6/audio/sfx/KART_Gag_Hit_Anvil.mp3')
        self.accept('leaveRace', self.leaveRace)
        self.toonsToLink = []
        self.curveTs = []
        self.curvePoints = []
        self.localKart = None
        self.musicTrack = None
        self.victory = None
        self.miscTaskNames = []
        self.boostDir = {}
        self.knownPlace = {}
        self.placeFixup = []
        self.curve = None
        self.barricadeSegments = 100.0
        self.outerBarricadeDict = {}
        self.innerBarricadeDict = {}
        self.maxLap = 0
        self.oldT = 0
        self.debugIt = 0
        self.startPos = None
        return

    def generate(self):
        self.notify.debug('generate: %s' % self.doId)
        DistributedObject.DistributedObject.generate(self)
        bboard.post('race', self)
        self.roomWatcher = None
        self.cutoff = 0.01
        self.startBoopSfx = base.loadSfx(self.SFX_StartBoop)
        self.startBoop2Sfx = base.loadSfx(self.SFX_StartBoop2)
        return

    def announceGenerate(self):
        self.notify.debug('announceGenerate: %s' % self.doId)
        DistributedObject.DistributedObject.announceGenerate(self)
        musicFile = self.BGM_BaseDir + RaceGlobals.TrackDict[self.trackId][7]
        self.raceMusic = base.loadMusic(musicFile)
        base.playMusic(self.raceMusic, looping=1, volume=0.8)
        camera.reparentTo(render)
        if self.trackId in (RaceGlobals.RT_Urban_1,
         RaceGlobals.RT_Urban_1_rev,
         RaceGlobals.RT_Urban_2,
         RaceGlobals.RT_Urban_2_rev):
            self.isUrbanTrack = True
        self.oldFarPlane = base.camLens.getFar()
        base.camLens.setFar(12000)
        localAvatar.startPosHprBroadcast()
        localAvatar.d_broadcastPositionNow()
        DistributedSmoothNode.activateSmoothing(1, 1)
        self.reversed = self.trackId / 2.0 > int(self.trackId / 2.0)
        for i in range(3):
            base.loader.tick()

        self.sky = loader.loadModel('phase_3.5/models/props/TT_sky')
        self.sky.setPos(0, 0, 0)
        self.sky.setScale(20.0)
        self.sky.setFogOff()
        if self.trackId in (RaceGlobals.RT_Urban_1,
         RaceGlobals.RT_Urban_1_rev,
         RaceGlobals.RT_Urban_2,
         RaceGlobals.RT_Urban_2_rev):
            self.loadFog()
        self.setupGeom()
        self.startSky()
        for i in range(5):
            base.loader.tick()

    def disable(self):
        self.notify.debug('disable %s' % self.doId)
        if self.musicTrack:
            self.musicTrack.finish()
        self.raceMusic.stop()
        self.stopSky()
        if self.sky is not None:
            self.sky.removeNode()
        if self.dummyNode:
            self.dummyNode.removeNode()
            self.dummyNode = None
        for taskName in self.miscTaskNames:
            taskMgr.remove(taskName)

        taskMgr.remove('raceWatcher')
        self.ignoreAll()
        DistributedSmoothNode.activateSmoothing(1, 0)
        if self.isUrbanTrack:
            self.unloadUrbanTrack()
        if self.fog:
            render.setFogOff()
            del self.fog
            self.fog = None
        if self.geom is not None:
            self.geom.hide()
        base.camLens.setFar(self.oldFarPlane)
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        self.notify.debug('delete %s' % self.doId)
        if self.gui:
            self.gui.destroy()
            self.gui = None
        if self.geom is not None:
            self.geom.removeNode()
            self.geom = None
            for i in self.gags:
                i.delete()
                del i

        self.piejectileManager.delete()
        if self.curveTs:
            del self.curveTs
        if self.curvePoints:
            del self.curvePoints
        if self.curve:
            del self.curve
        if self.victory:
            del self.victory
        del self.fsm
        del self.anvilFall
        del self.bananaSound
        del self.localKart
        DistributedObject.DistributedObject.delete(self)
        taskMgr.remove(self.uniqueName('countdownTimerTask'))
        taskMgr.remove('raceWatcher')
        bboard.remove('race')
        self.ignoreAll()
        del base.race
        return

    def d_requestThrow(self, x, y, z):
        self.sendUpdate('requestThrow', [x, y, z])

    def d_requestKart(self):
        self.sendUpdate('requestKart', [])

    def waitingForJoin(self):
        self.notify.debug('I got the barrier')
        self.fsm.enterInitialState()

    def racerDisconnected(self, avId):
        self.notify.debug('lost racer: %s' % avId)
        if avId in self.kartMap:
            if avId in self.toonsToLink:
                self.toonsToLink.remove(avId)
            toon = base.cr.doId2do.get(avId, None)
            kart = base.cr.doId2do.get(self.kartMap.get(avId, None), None)
            self.avIds.remove(avId)
            del self.kartMap[avId]
            self.gui.racerLeft(avId, unexpected=True)
            if kart:
                kart.reparentTo(hidden)
            if toon:
                toon.reparentTo(hidden)
            if len(self.toonsToLink) == 0:
                self.doneBarrier('waitingForPrep')
        return

    def setPlace(self, avId, totalTime, place, entryFee, qualify, winnings, bonus, trophies, circuitPoints, circuitTime):
        if self.fsm.getCurrentState().getName() == 'leaving':
            return
        if avId == localAvatar.doId:
            cheerToPlay = place + (4 - self.numRacers)
            if cheerToPlay > 4:
                cheerToPlay = 4
            self.victory = base.loadSfx(self.SFX_Applause % cheerToPlay)
            self.victory.play()
        self.knownPlace[avId] = place
        kart = base.cr.doId2do.get(self.kartMap.get(avId, None), None)
        avatar = base.cr.doId2do.get(avId, None)
        if avatar:
            self.gui.racerFinished(avId, self.trackId, place, totalTime, entryFee, qualify, winnings, bonus, trophies, circuitPoints, circuitTime)
            taskName = 'hideAv: %s' % avId
            taskMgr.doMethodLater(6, avatar.reparentTo, taskName, extraArgs=[hidden])
            self.miscTaskNames.append(taskName)
        if kart:
            taskName = 'hideKart: %s' % self.localKart.doId
            taskMgr.doMethodLater(6, kart.reparentTo, taskName, extraArgs=[hidden])
            self.miscTaskNames.append(taskName)
        return

    def setCircuitPlace(self, avId, place, entryFee, winnings, bonus, trophies):
        print 'setting cicruit place'
        if self.fsm.getCurrentState().getName() == 'leaving':
            return
        if avId == localAvatar.doId:
            cheerToPlay = place + (4 - self.numRacers)
            self.victory = base.loadSfx(self.SFX_Applause % cheerToPlay)
            self.victory.play()
        oldPlace = 0
        if self.knownPlace.get(avId):
            oldPlace = self.knownPlace[avId]
            self.placeFixup.append([oldPlace - 1, place - 1])
        avatar = base.cr.doId2do.get(avId, None)
        if avatar:
            print 'circuit trophies %s' % trophies
            print 'winnings %s' % winnings
            self.gui.racerFinishedCircuit(avId, oldPlace, entryFee, winnings, bonus, trophies)
        return

    def endCircuitRace(self):
        print self.placeFixup
        self.gui.circuitFinished(self.placeFixup)

    def prepForRace(self):
        self.fsm.request('prep')

    def startRace(self, startTime = 0):
        self.baseTime = globalClockDelta.networkToLocalTime(startTime)
        self.fsm.request('start')

    def startTutorial(self):
        self.fsm.request('tutorial')

    def genGag(self, slot, number, type):
        self.notify.debug('making gag...')
        if not self.gags[slot].isActive():
            self.gags[slot].genGag(number, type)

    def dropAnvilOn(self, ownerId, avId, timeStamp):
        kart = base.cr.doId2do.get(self.kartMap.get(avId, None), None)
        if kart:
            if avId != ownerId:
                if avId == localAvatar.doId:
                    self.anvilFall.play()
                    kart.dropOnMe(timeStamp)
                else:
                    kart.dropOnHim(timeStamp)
        return

    def shootPiejectile(self, sourceId, targetId, type = 0):
        kart = base.cr.doId2do.get(self.kartMap.get(sourceId, None), None)
        if kart:
            self.piejectileManager.addPiejectile(sourceId, targetId, type)
        return

    def goToSpeedway(self, avIds, reason = RaceGlobals.Exit_UserReq):
        self.notify.debug('goToSpeedway %s %s' % (avIds, reason))
        if localAvatar.doId in avIds:
            base.loader.endBulkLoad('atRace')
            self.kartCleanup()
            self.doneBarrier('waitingForExit')
            self.sendUpdate('racerLeft', [localAvatar.doId])
            out = {'loader': 'safeZoneLoader',
             'where': 'playground',
             'how': 'teleportIn',
             'hoodId': localAvatar.lastHood,
             'zoneId': localAvatar.lastHood,
             'shardId': None,
             'avId': -1,
             'reason': reason}
            base.cr.playGame.fsm.request('quietZone', [out])
        return

    def kartCleanup(self):
        kart = self.localKart
        if kart:
            kart.setState('P', 0)
            for i in self.avIds:
                if i != localAvatar.doId:
                    toon = base.cr.doId2do.get(i, None)
                    if toon:
                        toon.stopSmooth()
                        toon.setScale(1)
                        toon.setShear(0, 0, 0)
                        toon.reparentTo(render)
                        kart.doHeadScale(toon, None)

        localAvatar.setPos(0, 14, 0)
        localAvatar.sendCurrentPosition()
        return

    def heresMyT(self, avId, avNumLaps, avTime, timestamp):
        self.gui.updateRacerInfo(avId, curvetime=avNumLaps + avTime)

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def setRaceType(self, raceType):
        self.raceType = raceType

    def setCircuitLoop(self, circuitLoop):
        self.circuitLoop = circuitLoop

    def setTrackId(self, id):
        DistributedRace.notify.debug('setTrackId: %s' % id)
        self.trackId = id

    def setAvatars(self, avIds):
        ids = ''
        for i in avIds:
            ids += str(i) + ' '

        DistributedRace.notify.debug('setAvatars: %s' % ids)
        self.avIds = avIds
        self.avT = [0] * len(self.avIds)

    def setLapCount(self, lapCount):
        self.lapCount = lapCount

    def setStartingPlaces(self, startList):
        self.startingPlaces = startList

    def enterJoin(self):
        self.doneBarrier('waitingForJoin')
        self.notify.debug('entering Join')

    def exitJoin(self):
        pass

    def setEnteredRacers(self, avAndKarts):
        self.notify.debug('setEnteredRacers %s' % avAndKarts)
        avatarsGone = []
        avatarsLeft = []
        self.numRacers = len(avAndKarts)
        for i in avAndKarts:
            if i[0] in self.avIds:
                self.kartMap[i[0]] = i[1]
                avatarsLeft.append(i[0])

        for i in self.avIds:
            if i not in avatarsLeft:
                avatarsGone.append(i)

        base.loader.tick()
        for i in avatarsGone:
            self.avIds.remove(i)

        self.toonsToLink = list(self.avIds)
        for i in avAndKarts:
            self.cr.relatedObjectMgr.requestObjects(i, allCallback=self.__gotKartAvatarLink)

    def __gotKartAvatarLink(self, avAndKart):
        self.notify.debug('got a Link')
        toon = avAndKart[0]
        kart = avAndKart[1]
        base.loader.tick()
        if toon.doId in self.toonsToLink:
            self.toonsToLink.remove(toon.doId)
        if toon.doId == localAvatar.doId:
            self.localKart = kart
        if len(self.toonsToLink) == 0:
            self.doneBarrier('waitingForPrep')

    def enterPrep(self):
        self.d_requestKart()
        self.notify.debug('entering Prep State')
        if self.reversed:
            self.spin = Vec3(180, 0, 0)
        else:
            self.spin = Vec3(0, 0, 0)
        for i in range(4):
            base.loader.tick()

        self.gui.initRaceMode()
        self.gui.initResultMode()
        self.myPos = self.startingPos[self.startingPlaces[self.avIds.index(localAvatar.doId)]]
        self.localKart.setPosHpr(self.myPos[0], self.myPos[1] + self.spin)
        self.localKart.setupLapCollisions()
        if self.dummyNode:
            self.dummyNode.setPosHpr(self.myPos[0], self.myPos[1] + self.spin)
        self.currentPole = self.findSegmentStart()
        self.rabbitPoint = Vec3(0, 0, 0)
        self.doneBarrier('waitingForReady')

    def exitPrep(self):
        pass

    def enterTutorial(self):
        self.notify.debug('entering Tutorial State')
        base.loader.endBulkLoad('atRace')
        self.localKart.setPosHpr(self.myPos[0], self.myPos[1] + self.spin)
        base.transitions.irisIn()
        self.rulesDoneEvent = 'finishedRules'
        self.accept(self.rulesDoneEvent, self.handleRulesDone)
        self.rulesPanel = MinigameRulesPanel.MinigameRulesPanel('RacingRulesPanel', self.getTitle(), self.getInstructions(), self.rulesDoneEvent, 10)
        self.rulesPanel.load()
        self.rulesPanel.frame.setPos(0, 0, -0.6667)
        self.rulesPanel.enter()

    def exitTutorial(self):
        self.ignore(self.rulesDoneEvent)
        self.rulesPanel.exit()
        self.rulesPanel.unload()
        del self.rulesPanel

    def getTitle(self):
        return TTLocalizer.KartRace_TitleInfo

    def getInstructions(self):
        return TTLocalizer.KartRace_TrackInfo[self.trackId]

    def handleRulesDone(self):
        self.doneBarrier('readRules')
        self.fsm.request('waiting')

    def enterWaiting(self):
        self.waitingLabel = DirectLabel()
        self.waitingLabel['text'] = TTLocalizer.BuildingWaitingForVictors
        self.waitingLabel.setScale(TTLocalizer.DRenterWaiting)

    def exitWaiting(self):
        self.waitingLabel.remove()

    def enterStart(self):
        waitTime = self.baseTime - globalClock.getFrameTime()
        taskName = 'enableRaceModeLater'
        taskMgr.doMethodLater(1, self.gui.enableRaceMode, taskName, extraArgs=[])
        self.miscTaskNames.append(taskName)
        for i in self.avIds:
            self.gui.racerEntered(i)

        self.startCountdownClock(waitTime, 0)
        taskMgr.doMethodLater(waitTime, self.fsm.request, 'goToRacing', extraArgs=['racing'])

    def exitStart(self):
        pass

    def enterRacing(self):
        self.localKart.setInput(1)
        self.gui.setTimerEnabled(True)
        self.raceTask = taskMgr.add(self.raceWatcher, 'raceWatcher')

    def exitRacing(self):
        pass

    def raceWatcher(self, task):
        kart = base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        if self.localKart.amIClampingPosition():
            self.notify.debug('teleporting kart %d back to main track' % localAvatar.doId)
            self.localKart.setPos(self.curvePoints[self.currentPole])
        kartPoint = self.localKart.getPos()
        direction = 0
        while True:
            currPoint = self.curvePoints[self.currentPole]
            nextPole = (self.currentPole + 1) % len(self.curvePoints)
            nextPoint = self.curvePoints[nextPole]
            segment = nextPoint - currPoint
            segment.setZ(0)
            segLength2 = segment.lengthSquared()
            kartVector = kartPoint - currPoint
            kartVector.setZ(0)
            project = segment * (segment.dot(kartVector) / segLength2)
            projLength2 = project.lengthSquared()
            if project.dot(segment) < 0:
                if direction == 1:
                    break
                prevPole = (self.currentPole - 1) % len(self.curvePoints)
                self.currentPole = prevPole
                direction = -1
            elif projLength2 > segLength2:
                if direction == -1:
                    break
                self.currentPole = nextPole
                direction = 1
            else:
                break

        if self.dummyNode:
            self.dummyNode.setPos(kartPoint[0], kartPoint[1], 0)
            self.dummyNode.setHpr(self.localKart.getH(), 0, 0)
        t = projLength2 / segLength2
        if self.debugIt:
            self.notify.debug('self.debugIt = %d' % self.debugIt)
            import pdb
            pdb.set_trace()
        if nextPole < self.currentPole:
            newT = self.curveTs[self.currentPole] * (1 - t) + self.curve.getMaxT() * t
        else:
            newT = self.curveTs[self.currentPole] * (1 - t) + self.curveTs[nextPole] * t
        kartDirection = self.localKart.forward.getPos(render) - self.localKart.getPos(render)
        kartDirection.normalize()
        project.normalize()
        globalDirection = kartDirection.dot(project)
        if globalDirection < 0:
            self.wrongWay = True
        elif globalDirection > 0.1:
            self.wrongWay = False
        newLapT = (newT - self.startT) / self.curve.getMaxT() % 1.0
        if newLapT - self.currLapT < -0.5:
            self.laps += 1
            self.changeMusicTempo(1 + self.laps * 0.5)
            self.notify.debug('crossed the start line: %s, %s, %s, %s' % (self.laps,
             self.startT,
             self.currT,
             newT))
        elif newLapT - self.currLapT > 0.5:
            self.laps -= 1
            self.changeMusicTempo(1 + self.laps * 0.5)
            self.notify.debug('crossed the start line - wrong way: %s, %s, %s, %s' % (self.laps,
             self.startT,
             self.currT,
             newT))
        self.currT = newT
        self.currLapT = newLapT
        if self.isUrbanTrack:
            self.showBuildings(self.currT)
        now = globalClock.getFrameTime()
        timestamp = globalClockDelta.localToNetworkTime(now)
        if self.laps == self.lapCount:
            self.sendUpdate('heresMyT', [localAvatar.doId,
             self.laps,
             self.currLapT,
             timestamp])
            self.fsm.request('finished')
        if self.laps > self.maxLap:
            self.maxLap = self.laps
            self.sendUpdate('heresMyT', [localAvatar.doId,
             self.laps,
             self.currLapT,
             timestamp])
        if now - self.lastTimeUpdate > 0.5:
            self.lastTimeUpdate = now
            self.sendUpdate('heresMyT', [localAvatar.doId,
             self.laps,
             self.currLapT,
             timestamp])
        self.gui.updateRacerInfo(localAvatar.doId, curvetime=self.currLapT + self.laps)
        self.gui.update(now)
        return Task.cont

    def enterFinished(self):
        taskMgr.remove('raceWatcher')
        self.fadeOutMusic()
        self.localKart.interruptTurbo()
        self.localKart.disableControls()
        taskName = 'parkIt'
        taskMgr.doMethodLater(2, self.stopDriving, taskName, extraArgs=[])
        self.miscTaskNames.append(taskName)
        self.finished = True
        camera.reparentTo(render)
        camera.setPos(self.localKart.getPos(render) + Vec3(0, 0, 10))
        camera.setH(self.localKart.getH(render) + 180)
        self.gui.disableRaceMode()
        self.gui.enableResultMode()
        localAvatar.reparentTo(hidden)
        self.localKart.reparentTo(hidden)

    def exitFinished(self):
        pass

    def stopDriving(self):
        kart = base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        cpos = camera.getPos()
        chpr = camera.getHpr()
        localAvatar.reparentTo(hidden)
        self.localKart.reparentTo(hidden)
        self.localKart.stopSmooth()
        self.localKart.stopPosHprBroadcast()
        camera.setPos(cpos)
        camera.setHpr(chpr)
        return

    def enterLeave(self):
        kart = base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        taskMgr.remove('raceWatcher')
        self.gui.disable()
        if self.localKart:
            self.localKart.disableControls()
        base.transitions.irisOut()
        if self.raceType == RaceGlobals.Circuit and not len(self.circuitLoop) == 0:
            self.sendUpdate('racerLeft', [localAvatar.doId])
        else:
            taskMgr.doMethodLater(1, self.goToSpeedway, 'leaveRace', extraArgs=[[localAvatar.doId], RaceGlobals.Exit_UserReq])
        if self.victory:
            self.victory.stop()
        self.bananaSound.stop()
        self.anvilFall.stop()
        return

    def exitLeave(self):
        pass

    def getCountdownColor(self, countdownTimeInt):
        clockNodeColors = [Vec4(0, 1, 0, 1),
         Vec4(1, 1, 0, 1),
         Vec4(1, 0.5, 0, 1),
         Vec4(1, 0, 0, 1)]
        i = max(min(countdownTimeInt, len(clockNodeColors) - 1), 0)
        return clockNodeColors[i]

    def startCountdownClock(self, countdownTime, ts):
        self.clockNode = TextNode('k')
        self.clockNode.setFont(ToontownGlobals.getSignFont())
        self.clockNode.setAlign(TextNode.ACenter)
        countdownInt = int(countdownTime)
        self.clockNode.setTextColor(self.getCountdownColor(countdownInt))
        self.clockNode.setText(str(countdownInt))
        self.clock = render2d.attachNewNode(self.clockNode)
        rs = TTLocalizer.DRrollScale
        self.clock.setPosHprScale(0, 0, 0, 0, 0, 0, rs, rs, rs)
        self.clock.hide()
        if ts < countdownTime:
            self.countdown(countdownTime - ts)

    def timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        timeStr = str(countdownTime + 1)
        if self.clock.isHidden():
            if task.duration - task.time <= task.maxCount:
                self.clock.show()
        if self.clockNode.getText() != timeStr:
            self.startBoopSfx.play()
            self.clockNode.setText(timeStr)
            self.clockNode.setTextColor(self.getCountdownColor(countdownTime + 1))
        if task.time >= task.duration:
            self.startBoop2Sfx.play()
            self.clockNode.setText(TTLocalizer.KartRace_Go)
            self.clockNode.setTextColor(self.getCountdownColor(-1))
            taskMgr.doMethodLater(1, self.endGoSign, 'removeGoSign')
            return Task.done
        else:
            return Task.cont

    def endGoSign(self, t):
        self.clock.remove()

    def countdown(self, duration):
        countdownTask = Task(self.timerTask)
        countdownTask.duration = duration
        countdownTask.maxCount = RaceGlobals.RaceCountdown
        taskMgr.remove(self.uniqueName('countdownTimerTask'))
        return taskMgr.add(countdownTask, self.uniqueName('countdownTimerTask'))

    def initGags(self):
        self.banana = globalPropPool.getProp('banana')
        self.banana.setScale(2)
        self.pie = globalPropPool.getProp('creampie')
        self.pie.setScale(1)

    def makeCheckPoint(self, trigger, location, event):
        cs = CollisionSphere(0, 0, 0, 140)
        cs.setTangible(0)
        triggerEvent = 'imIn-' + trigger
        cn = CollisionNode(trigger)
        cn.addSolid(cs)
        cn.setIntoCollideMask(BitMask32(32768))
        cn.setFromCollideMask(BitMask32(32768))
        cnp = NodePath(cn)
        cnp.reparentTo(self.geom)
        cnp.setPos(location)
        self.accept(triggerEvent, event)

    def loadUrbanTrack--- This code section failed: ---

0	LOAD_GLOBAL       'DNAStorage'
3	CALL_FUNCTION_0   None
6	LOAD_FAST         'self'
9	STORE_ATTR        'dnaStore'

12	LOAD_GLOBAL       'loader'
15	LOAD_ATTR         'loadDNAFile'
18	LOAD_FAST         'self'
21	LOAD_ATTR         'dnaStore'
24	LOAD_CONST        'phase_4/dna/storage.dna'
27	CALL_FUNCTION_2   None
30	POP_TOP           None

31	LOAD_GLOBAL       'loader'
34	LOAD_ATTR         'loadDNAFile'
37	LOAD_FAST         'self'
40	LOAD_ATTR         'dnaStore'
43	LOAD_CONST        'phase_5/dna/storage_town.dna'
46	CALL_FUNCTION_2   None
49	POP_TOP           None

50	LOAD_GLOBAL       'loader'
53	LOAD_ATTR         'loadDNAFile'
56	LOAD_FAST         'self'
59	LOAD_ATTR         'dnaStore'
62	LOAD_CONST        'phase_4/dna/storage_TT.dna'
65	CALL_FUNCTION_2   None
68	POP_TOP           None

69	LOAD_GLOBAL       'loader'
72	LOAD_ATTR         'loadDNAFile'
75	LOAD_FAST         'self'
78	LOAD_ATTR         'dnaStore'
81	LOAD_CONST        'phase_5/dna/storage_TT_town.dna'
84	CALL_FUNCTION_2   None
87	POP_TOP           None

88	LOAD_GLOBAL       'loader'
91	LOAD_ATTR         'loadDNAFile'
94	LOAD_FAST         'self'
97	LOAD_ATTR         'dnaStore'
100	LOAD_CONST        'phase_8/dna/storage_BR.dna'
103	CALL_FUNCTION_2   None
106	POP_TOP           None

107	LOAD_GLOBAL       'loader'
110	LOAD_ATTR         'loadDNAFile'
113	LOAD_FAST         'self'
116	LOAD_ATTR         'dnaStore'
119	LOAD_CONST        'phase_8/dna/storage_BR_town.dna'
122	CALL_FUNCTION_2   None
125	POP_TOP           None

126	LOAD_CONST        'phase_6/dna/urban_track_town.dna'
129	STORE_FAST        'dnaFile'

132	LOAD_FAST         'self'
135	LOAD_ATTR         'trackId'
138	LOAD_GLOBAL       'RaceGlobals'
141	LOAD_ATTR         'RT_Urban_2'
144	LOAD_GLOBAL       'RaceGlobals'
147	LOAD_ATTR         'RT_Urban_2_rev'
150	BUILD_TUPLE_2     None
153	COMPARE_OP        'in'
156	JUMP_IF_FALSE     '168'

159	LOAD_CONST        'phase_6/dna/urban_track_town_B.dna'
162	STORE_FAST        'dnaFile'
165	JUMP_FORWARD      '168'
168_0	COME_FROM         '165'

168	LOAD_GLOBAL       'loader'
171	LOAD_ATTR         'loadDNAFile'
174	LOAD_FAST         'self'
177	LOAD_ATTR         'dnaStore'
180	LOAD_FAST         'dnaFile'
183	CALL_FUNCTION_2   None
186	STORE_FAST        'node'

189	LOAD_FAST         'self'
192	LOAD_ATTR         'geom'
195	LOAD_ATTR         'attachNewNode'
198	LOAD_FAST         'node'
201	CALL_FUNCTION_1   None
204	LOAD_FAST         'self'
207	STORE_ATTR        'townGeom'

210	LOAD_FAST         'self'
213	LOAD_ATTR         'townGeom'
216	LOAD_ATTR         'findAllMatches'
219	LOAD_CONST        '**/+CollisionNode'
222	CALL_FUNCTION_1   None
225	LOAD_ATTR         'stash'
228	CALL_FUNCTION_0   None
231	POP_TOP           None

232	BUILD_MAP         None
235	LOAD_FAST         'self'
238	STORE_ATTR        'buildingGroups'

241	BUILD_MAP         None
244	LOAD_FAST         'self'
247	STORE_ATTR        'currBldgInd'

250	BUILD_MAP         None
253	LOAD_FAST         'self'
256	STORE_ATTR        'currBldgGroups'

259	LOAD_FAST         'self'
262	LOAD_ATTR         'geom'
265	LOAD_ATTR         'find'
268	LOAD_CONST        '**/polySurface8'
271	CALL_FUNCTION_1   None
274	STORE_FAST        'bgGeom'

277	LOAD_FAST         'self'
280	LOAD_ATTR         'dummyNode'
283	JUMP_IF_FALSE     '305'

286	LOAD_FAST         'bgGeom'
289	LOAD_ATTR         'reparentTo'
292	LOAD_FAST         'self'
295	LOAD_ATTR         'dummyNode'
298	CALL_FUNCTION_1   None
301	POP_TOP           None
302	JUMP_FORWARD      '318'

305	LOAD_FAST         'bgGeom'
308	LOAD_ATTR         'reparentTo'
311	LOAD_GLOBAL       'localAvatar'
314	CALL_FUNCTION_1   None
317	POP_TOP           None
318_0	COME_FROM         '302'

318	LOAD_FAST         'bgGeom'
321	LOAD_ATTR         'setScale'
324	LOAD_CONST        0.1
327	CALL_FUNCTION_1   None
330	POP_TOP           None

331	LOAD_GLOBAL       'CompassEffect'
334	LOAD_ATTR         'make'
337	LOAD_GLOBAL       'NodePath'
340	CALL_FUNCTION_0   None
343	LOAD_GLOBAL       'CompassEffect'
346	LOAD_ATTR         'PRot'
349	CALL_FUNCTION_2   None
352	STORE_FAST        'ce'

355	LOAD_FAST         'bgGeom'
358	LOAD_ATTR         'node'
361	CALL_FUNCTION_0   None
364	LOAD_ATTR         'setEffect'
367	LOAD_FAST         'ce'
370	CALL_FUNCTION_1   None
373	POP_TOP           None

374	LOAD_FAST         'bgGeom'
377	LOAD_ATTR         'setDepthTest'
380	LOAD_CONST        0
383	CALL_FUNCTION_1   None
386	POP_TOP           None

387	LOAD_FAST         'bgGeom'
390	LOAD_ATTR         'setDepthWrite'
393	LOAD_CONST        0
396	CALL_FUNCTION_1   None
399	POP_TOP           None

400	LOAD_FAST         'bgGeom'
403	LOAD_ATTR         'setBin'
406	LOAD_CONST        'background'
409	LOAD_CONST        102
412	CALL_FUNCTION_2   None
415	POP_TOP           None

416	LOAD_FAST         'bgGeom'
419	LOAD_ATTR         'setZ'
422	LOAD_CONST        -1
425	CALL_FUNCTION_1   None
428	POP_TOP           None

429	LOAD_FAST         'bgGeom'
432	LOAD_FAST         'self'
435	STORE_ATTR        'bgGeom'

438	LOAD_FAST         'self'
441	LOAD_ATTR         'geom'
444	LOAD_ATTR         'findAllMatches'
447	LOAD_CONST        '**/+ModelNode'
450	CALL_FUNCTION_1   None
453	STORE_FAST        'l'

456	SETUP_LOOP        '492'
459	LOAD_FAST         'l'
462	GET_ITER          None
463	FOR_ITER          '491'
466	STORE_FAST        'n'

469	LOAD_FAST         'n'
472	LOAD_ATTR         'node'
475	CALL_FUNCTION_0   None
478	LOAD_ATTR         'setPreserveTransform'
481	LOAD_CONST        0
484	CALL_FUNCTION_1   None
487	POP_TOP           None
488	JUMP_BACK         '463'
491	POP_BLOCK         None
492_0	COME_FROM         '456'

492	LOAD_FAST         'self'
495	LOAD_ATTR         'geom'
498	LOAD_ATTR         'flattenLight'
501	CALL_FUNCTION_0   None
504	POP_TOP           None

505	LOAD_CONST        0
508	STORE_FAST        'maxNum'

511	SETUP_LOOP        '817'
514	LOAD_CONST        'inner'
517	LOAD_CONST        'outer'
520	BUILD_LIST_2      None
523	GET_ITER          None
524	FOR_ITER          '816'
527	STORE_FAST        'side'

530	BUILD_LIST_0      None
533	LOAD_FAST         'self'
536	LOAD_ATTR         'buildingGroups'
539	LOAD_FAST         'side'
542	STORE_SUBSCR      None

543	LOAD_CONST        None
546	LOAD_FAST         'self'
549	LOAD_ATTR         'currBldgInd'
552	LOAD_FAST         'side'
555	STORE_SUBSCR      None

556	LOAD_CONST        None
559	LOAD_FAST         'self'
562	LOAD_ATTR         'currBldgGroups'
565	LOAD_FAST         'side'
568	STORE_SUBSCR      None

569	LOAD_CONST        0
572	STORE_FAST        'i'

575	SETUP_LOOP        '792'

578	LOAD_FAST         'self'
581	LOAD_ATTR         'townGeom'
584	LOAD_ATTR         'find'
587	LOAD_CONST        '**/Buildings_'
590	LOAD_FAST         'side'
593	BINARY_ADD        None
594	LOAD_CONST        '-'
597	BINARY_ADD        None
598	LOAD_GLOBAL       'str'
601	LOAD_FAST         'i'
604	CALL_FUNCTION_1   None
607	BINARY_ADD        None
608	CALL_FUNCTION_1   None
611	STORE_FAST        'bldgGroup'

614	LOAD_FAST         'bldgGroup'
617	LOAD_ATTR         'isEmpty'
620	CALL_FUNCTION_0   None
623	JUMP_IF_FALSE     '630'

626	BREAK_LOOP        None
627	JUMP_FORWARD      '630'
630_0	COME_FROM         '627'

630	LOAD_FAST         'bldgGroup'
633	LOAD_ATTR         'findAllMatches'
636	LOAD_CONST        '**/+ModelNode'
639	CALL_FUNCTION_1   None
642	STORE_FAST        'l'

645	SETUP_LOOP        '718'
648	LOAD_FAST         'l'
651	GET_ITER          None
652	FOR_ITER          '717'
655	STORE_FAST        'n'

658	LOAD_FAST         'n'
661	LOAD_ATTR         'getParent'
664	CALL_FUNCTION_0   None
667	LOAD_ATTR         'attachNewNode'
670	LOAD_FAST         'n'
673	LOAD_ATTR         'getName'
676	CALL_FUNCTION_0   None
679	CALL_FUNCTION_1   None
682	STORE_FAST        'n2'

685	LOAD_FAST         'n'
688	LOAD_ATTR         'getChildren'
691	CALL_FUNCTION_0   None
694	LOAD_ATTR         'reparentTo'
697	LOAD_FAST         'n2'
700	CALL_FUNCTION_1   None
703	POP_TOP           None

704	LOAD_FAST         'n'
707	LOAD_ATTR         'removeNode'
710	CALL_FUNCTION_0   None
713	POP_TOP           None
714	JUMP_BACK         '652'
717	POP_BLOCK         None
718_0	COME_FROM         '645'

718	LOAD_FAST         'bldgGroup'
721	LOAD_ATTR         'flattenStrong'
724	CALL_FUNCTION_0   None
727	POP_TOP           None

728	LOAD_FAST         'bldgGroup'
731	LOAD_ATTR         'getNode'
734	LOAD_CONST        0
737	CALL_FUNCTION_1   None
740	LOAD_ATTR         'getBounds'
743	CALL_FUNCTION_0   None
746	LOAD_ATTR         'isEmpty'
749	CALL_FUNCTION_0   None
752	JUMP_IF_TRUE      '778'

755	LOAD_FAST         'self'
758	LOAD_ATTR         'buildingGroups'
761	LOAD_FAST         'side'
764	BINARY_SUBSCR     None
765	LOAD_ATTR         'append'
768	LOAD_FAST         'bldgGroup'
771	CALL_FUNCTION_1   None
774	POP_TOP           None
775	JUMP_FORWARD      '778'
778_0	COME_FROM         '775'

778	LOAD_FAST         'i'
781	LOAD_CONST        1
784	INPLACE_ADD       None
785	STORE_FAST        'i'
788	JUMP_BACK         '578'
791	POP_BLOCK         None
792_0	COME_FROM         '575'

792	LOAD_FAST         'i'
795	LOAD_FAST         'maxNum'
798	COMPARE_OP        '>'
801	JUMP_IF_FALSE     '813'

804	LOAD_FAST         'i'
807	STORE_FAST        'maxNum'
810	JUMP_BACK         '524'
813	JUMP_BACK         '524'
816	POP_BLOCK         None
817_0	COME_FROM         '511'

817	SETUP_LOOP        '1089'
820	LOAD_CONST        'innersidest'
823	LOAD_CONST        'outersidest'
826	BUILD_LIST_2      None
829	GET_ITER          None
830	FOR_ITER          '1088'
833	STORE_FAST        'side'

836	BUILD_LIST_0      None
839	LOAD_FAST         'self'
842	LOAD_ATTR         'buildingGroups'
845	LOAD_FAST         'side'
848	STORE_SUBSCR      None

849	LOAD_CONST        None
852	LOAD_FAST         'self'
855	LOAD_ATTR         'currBldgInd'
858	LOAD_FAST         'side'
861	STORE_SUBSCR      None

862	LOAD_CONST        None
865	LOAD_FAST         'self'
868	LOAD_ATTR         'currBldgGroups'
871	LOAD_FAST         'side'
874	STORE_SUBSCR      None

875	SETUP_LOOP        '1085'
878	LOAD_GLOBAL       'range'
881	LOAD_FAST         'maxNum'
884	CALL_FUNCTION_1   None
887	GET_ITER          None
888	FOR_ITER          '1084'
891	STORE_FAST        'i'

894	SETUP_LOOP        '1081'
897	LOAD_CONST        ('innerbarricade', 'outerbarricade')
900	GET_ITER          None
901	FOR_ITER          '1080'
904	STORE_FAST        'barricade'

907	LOAD_FAST         'self'
910	LOAD_ATTR         'townGeom'
913	LOAD_ATTR         'find'
916	LOAD_CONST        '**/Buildings_'
919	LOAD_FAST         'side'
922	BINARY_ADD        None
923	LOAD_CONST        '-'
926	BINARY_ADD        None
927	LOAD_FAST         'barricade'
930	BINARY_ADD        None
931	LOAD_CONST        '_'
934	BINARY_ADD        None
935	LOAD_GLOBAL       'str'
938	LOAD_FAST         'i'
941	CALL_FUNCTION_1   None
944	BINARY_ADD        None
945	CALL_FUNCTION_1   None
948	STORE_FAST        'bldgGroup'

951	LOAD_FAST         'bldgGroup'
954	LOAD_ATTR         'isEmpty'
957	CALL_FUNCTION_0   None
960	JUMP_IF_FALSE     '969'

963	CONTINUE          '901'
966	JUMP_FORWARD      '969'
969_0	COME_FROM         '966'

969	LOAD_FAST         'bldgGroup'
972	LOAD_ATTR         'findAllMatches'
975	LOAD_CONST        '**/+ModelNode'
978	CALL_FUNCTION_1   None
981	STORE_FAST        'l'

984	SETUP_LOOP        '1057'
987	LOAD_FAST         'l'
990	GET_ITER          None
991	FOR_ITER          '1056'
994	STORE_FAST        'n'

997	LOAD_FAST         'n'
1000	LOAD_ATTR         'getParent'
1003	CALL_FUNCTION_0   None
1006	LOAD_ATTR         'attachNewNode'
1009	LOAD_FAST         'n'
1012	LOAD_ATTR         'getName'
1015	CALL_FUNCTION_0   None
1018	CALL_FUNCTION_1   None
1021	STORE_FAST        'n2'

1024	LOAD_FAST         'n'
1027	LOAD_ATTR         'getChildren'
1030	CALL_FUNCTION_0   None
1033	LOAD_ATTR         'reparentTo'
1036	LOAD_FAST         'n2'
1039	CALL_FUNCTION_1   None
1042	POP_TOP           None

1043	LOAD_FAST         'n'
1046	LOAD_ATTR         'removeNode'
1049	CALL_FUNCTION_0   None
1052	POP_TOP           None
1053	JUMP_BACK         '991'
1056	POP_BLOCK         None
1057_0	COME_FROM         '984'

1057	LOAD_FAST         'self'
1060	LOAD_ATTR         'buildingGroups'
1063	LOAD_FAST         'side'
1066	BINARY_SUBSCR     None
1067	LOAD_ATTR         'append'
1070	LOAD_FAST         'bldgGroup'
1073	CALL_FUNCTION_1   None
1076	POP_TOP           None
1077	JUMP_BACK         '901'
1080	POP_BLOCK         None
1081_0	COME_FROM         '894'
1081	JUMP_BACK         '888'
1084	POP_BLOCK         None
1085_0	COME_FROM         '875'
1085	JUMP_BACK         '830'
1088	POP_BLOCK         None
1089_0	COME_FROM         '817'

1089	LOAD_FAST         'self'
1092	LOAD_ATTR         'townGeom'
1095	LOAD_ATTR         'findAllMatches'
1098	LOAD_CONST        '**/prop_tree_*'
1101	CALL_FUNCTION_1   None
1104	STORE_FAST        'treeNodes'

1107	SETUP_LOOP        '1134'
1110	LOAD_FAST         'treeNodes'
1113	GET_ITER          None
1114	FOR_ITER          '1133'
1117	STORE_FAST        'tree'

1120	LOAD_FAST         'tree'
1123	LOAD_ATTR         'flattenStrong'
1126	CALL_FUNCTION_0   None
1129	POP_TOP           None
1130	JUMP_BACK         '1114'
1133	POP_BLOCK         None
1134_0	COME_FROM         '1107'

1134	LOAD_FAST         'self'
1137	LOAD_ATTR         'townGeom'
1140	LOAD_ATTR         'findAllMatches'
1143	LOAD_CONST        '**/prop_snow_tree_*'
1146	CALL_FUNCTION_1   None
1149	STORE_FAST        'snowTreeNodes'

1152	SETUP_LOOP        '1179'
1155	LOAD_FAST         'snowTreeNodes'
1158	GET_ITER          None
1159	FOR_ITER          '1178'
1162	STORE_FAST        'snowTree'

1165	LOAD_FAST         'snowTree'
1168	LOAD_ATTR         'flattenStrong'
1171	CALL_FUNCTION_0   None
1174	POP_TOP           None
1175	JUMP_BACK         '1159'
1178	POP_BLOCK         None
1179_0	COME_FROM         '1152'

1179	SETUP_LOOP        '1242'
1182	LOAD_CONST        'inner'
1185	LOAD_CONST        'outer'
1188	LOAD_CONST        'innersidest'
1191	LOAD_CONST        'outersidest'
1194	BUILD_LIST_4      None
1197	GET_ITER          None
1198	FOR_ITER          '1241'
1201	STORE_FAST        'side'

1204	SETUP_LOOP        '1238'
1207	LOAD_FAST         'self'
1210	LOAD_ATTR         'buildingGroups'
1213	LOAD_FAST         'side'
1216	BINARY_SUBSCR     None
1217	GET_ITER          None
1218	FOR_ITER          '1237'
1221	STORE_FAST        'grp'

1224	LOAD_FAST         'grp'
1227	LOAD_ATTR         'stash'
1230	CALL_FUNCTION_0   None
1233	POP_TOP           None
1234	JUMP_BACK         '1218'
1237	POP_BLOCK         None
1238_0	COME_FROM         '1204'
1238	JUMP_BACK         '1198'
1241	POP_BLOCK         None
1242_0	COME_FROM         '1179'

1242	LOAD_FAST         'self'
1245	LOAD_ATTR         'showBuildings'
1248	LOAD_CONST        0
1251	CALL_FUNCTION_1   None
1254	POP_TOP           None
1255	LOAD_CONST        None
1258	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 791

    def unloadUrbanTrack(self):
        del self.buildingGroups
        self.townGeom.removeNode()

    def loadFog(self):
        self.hasFog = True
        if self.isUrbanTrack:
            base.camLens.setFar(650)
        else:
            base.camLens.setFar(650)
        self.dummyNode = render.attachNewNode('dummyNode')
        if base.wantFog:
            self.fog = Fog('TrackFog')
            self.fog.setColor(Vec4(0.6, 0.7, 0.8, 1.0))
            if self.isUrbanTrack:
                self.fog.setLinearRange(200.0, 650.0)
            else:
                self.fog.setLinearRange(200.0, 800.0)
            render.setFog(self.fog)
        self.sky.setScale(1.725)
        self.sky.reparentTo(self.dummyNode)

    def showBuildings(self, t, forceRecompute = False):
        firstTimeCalled = 0
        if self.curve:
            t = t / self.curve.getMaxT()
        else:
            firstTimeCalled = 1
        if self.reversed:
            t = 1.0 - t
        numGroupsShown = 5
        for side in ['inner', 'outer']:
            numBldgGroups = len(self.buildingGroups[side])
            bldgInd = int(t * numBldgGroups)
            bldgInd = bldgInd % numBldgGroups
            if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
                oldBldgInd = int(self.oldT * numBldgGroups)
                newBldgInd = int(t * numBldgGroups)
                kartPoint = self.startPos
                kart = base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
                if kart:
                    kartPoint = self.localKart.getPos()
                if not self.currBldgInd[side]:
                    self.currBldgInd[side] = 0
                curInd = self.currBldgInd[side]
                myCurGroup = self.buildingGroups[side][curInd]
                prevGrp = (curInd - 1) % numBldgGroups
                myPrevGroup = self.buildingGroups[side][prevGrp]
                nextGrp = (curInd + 1) % numBldgGroups
                myNextGroup = self.buildingGroups[side][nextGrp]
                curVector = myCurGroup.getNode(0).getBounds().getCenter() - kartPoint
                curDistance = curVector.lengthSquared()
                prevVector = myPrevGroup.getNode(0).getBounds().getCenter() - kartPoint
                prevDistance = prevVector.lengthSquared()
                nextVector = myNextGroup.getNode(0).getBounds().getCenter() - kartPoint
                nextDistance = nextVector.lengthSquared()
                if curDistance <= prevDistance and curDistance <= nextDistance:
                    bldgInd = self.currBldgInd[side]
                elif prevDistance <= curDistance and prevDistance <= nextDistance:
                    bldgInd = prevGrp
                elif nextDistance <= curDistance and nextDistance <= prevDistance:
                    bldgInd = nextGrp
                else:
                    self.notify.warning('unhandled case!!!!')
                    bldgInd = self.currBldgInd[side]
            if bldgInd != self.currBldgInd[side]:
                currBldgGroups = self.currBldgGroups[side]
                if currBldgGroups:
                    for i in currBldgGroups:
                        self.buildingGroups[side][i].stash()

                prevGrp2 = (bldgInd - 2) % numBldgGroups
                prevGrp = (bldgInd - 1) % numBldgGroups
                currGrp = bldgInd % numBldgGroups
                nextGrp = (bldgInd + 1) % numBldgGroups
                nextGrp2 = (bldgInd + 2) % numBldgGroups
                self.currBldgGroups[side] = [prevGrp2,
                 prevGrp,
                 currGrp,
                 nextGrp,
                 nextGrp2]
                for i in self.currBldgGroups[side]:
                    self.buildingGroups[side][i].unstash()

                self.currBldgInd[side] = bldgInd

        if self.currBldgGroups['inner'] != self.currBldgGroups['outer']:
            pass
        if t != self.oldT:
            self.oldT = t
        if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
            if self.reversed:
                t = 1.0 - t
            for side in ['innersidest', 'outersidest']:
                segmentInd = int(t * self.barricadeSegments)
                seglmentInd = segmentInd % self.barricadeSegments
                if segmentInd != self.currBldgInd[side] or forceRecompute:
                    currBldgGroups = self.currBldgGroups[side]
                    if currBldgGroups:
                        for i in currBldgGroups:
                            self.buildingGroups[side][i].stash()

                    self.currBldgGroups[side] = []
                    if side == 'innersidest':
                        dict = self.innerBarricadeDict
                    elif side == 'outersidest':
                        dict = self.outerBarricadeDict
                    if dict.has_key(segmentInd):
                        self.currBldgGroups[side] = dict[segmentInd]
                    for i in self.currBldgGroups[side]:
                        self.buildingGroups[side][i].unstash()

                    self.currBldgInd[side] = segmentInd

        return

    def setupGeom(self):
        trackFilepath = RaceGlobals.TrackDict[self.trackId][0]
        self.geom = loader.loadModel(trackFilepath)
        for i in range(10):
            base.loader.tick()

        self.geom.reparentTo(render)
        if self.reversed:
            lapStartPos = self.geom.find('**/lap_start_rev').getPos()
        else:
            lapStartPos = self.geom.find('**/lap_start').getPos()
        self.startPos = lapStartPos
        lapMidPos = self.geom.find('**/lap_middle').getPos()
        for i in range(5):
            base.loader.tick()

        self.startingPos = []
        posLocators = self.geom.findAllMatches('**/start_pos*')
        for i in range(posLocators.getNumPaths()):
            base.loader.tick()
            self.startingPos.append([posLocators[i].getPos(), posLocators[i].getHpr()])

        self.notify.debug('self.startingPos: %s' % self.startingPos)
        self.wrongWay = False
        self.laps = 0
        if self.isUrbanTrack:
            self.loadUrbanTrack()
        self.genArrows()
        if self.reversed:
            self.curve = self.geom.find('**/curve_reverse').node()
        else:
            self.curve = self.geom.find('**/curve_forward').node()
        for i in range(4000):
            self.curvePoints.append(Point3(0, 0, 0))
            self.curve.getPoint(i / 4000.0 * (self.curve.getMaxT() - 1e-11), self.curvePoints[-1])
            self.curveTs.append(i / 4000.0 * (self.curve.getMaxT() - 1e-11))

        if self.trackId in (RaceGlobals.RT_Urban_2, RaceGlobals.RT_Urban_2_rev):
            self.precomputeSideStreets()
        for i in range(10):
            base.loader.tick()

        self.startT = self.getNearestT(lapStartPos)
        self.midT = self.getNearestT(lapMidPos)
        self.gags = []
        gagList = RaceGlobals.TrackDict[self.trackId][4]
        for i in range(len(gagList)):
            self.notify.debug('generating gag: %s' % i)
            self.gags.append(RaceGag(self, i, Vec3(*gagList[i]) + Vec3(0, 0, 3)))

        for i in range(5):
            base.loader.tick()

    def precomputeSideStreets(self):
        farDist = base.camLens.getFar() + 300
        farDistSquared = farDist * farDist
        for i in range(self.barricadeSegments):
            testPoint = Point3(0, 0, 0)
            self.curve.getPoint(i / self.barricadeSegments * (self.curve.getMaxT() - 1e-11), testPoint)
            for side in ('innersidest', 'outersidest'):
                for bldgGroupIndex in range(len(self.buildingGroups[side])):
                    bldgGroup = self.buildingGroups[side][bldgGroupIndex]
                    if not bldgGroup.getNode(0).getBounds().isEmpty():
                        bldgPoint = bldgGroup.getNode(0).getBounds().getCenter()
                        vector = testPoint - bldgPoint
                        if vector.lengthSquared() < farDistSquared:
                            if side == 'innersidest':
                                dict = self.innerBarricadeDict
                            elif side == 'outersidest':
                                dict = self.outerBarricadeDict
                            else:
                                self.notify.error('unhandled side')
                            if dict.has_key(i):
                                if bldgGroupIndex not in dict[i]:
                                    dict[i].append(bldgGroupIndex)
                            else:
                                dict[i] = [bldgGroupIndex]
                    for childIndex in (0,):
                        if childIndex >= bldgGroup.getNumChildren():
                            continue
                        childNodePath = bldgGroup.getChild(childIndex)
                        bldgPoint = childNodePath.node().getBounds().getCenter()
                        vector = testPoint - bldgPoint
                        if vector.lengthSquared() < farDistSquared:
                            if side == 'innersidest':
                                dict = self.innerBarricadeDict
                            elif side == 'outersidest':
                                dict = self.outerBarricadeDict
                            else:
                                self.notify.error('unhandled side')
                            if dict.has_key(i):
                                if bldgGroupIndex not in dict[i]:
                                    dict[i].append(bldgGroupIndex)
                            else:
                                dict[i] = [bldgGroupIndex]

        for side in ('innersidest', 'outersidest'):
            for bldgGroup in self.buildingGroups[side]:
                bldgGroup.flattenStrong()

        if self.isUrbanTrack:
            self.showBuildings(0, forceRecompute=True)

    def findSegmentStart(self):
        kart = base.cr.doId2do.get(self.kartMap.get(localAvatar.doId, None), None)
        minLength2 = 1000000
        minIndex = -1
        currPoint = Point3(0, 0, 0)
        kartPoint = self.localKart.getPos()
        for i in range(len(self.curvePoints)):
            currPoint = self.curvePoints[i]
            currLength2 = (kartPoint - currPoint).lengthSquared()
            if currLength2 < minLength2:
                minLength2 = currLength2
                minIndex = i

        currPoint = self.curvePoints[minIndex]
        if minIndex + 1 == len(self.curvePoints):
            nextPoint = self.curvePoints[0]
        else:
            nextPoint = self.curvePoints[minIndex + 1]
        if minIndex - 1 < 0:
            prevIndex = len(self.curvePoints) - 1
        else:
            prevIndex = minIndex - 1
        forwardSegment = nextPoint - currPoint
        if (kartPoint - currPoint).dot(forwardSegment) > 0:
            return minIndex
        else:
            return prevIndex
        return

    def getNearestT(self, pos):
        minLength2 = 1000000
        minIndex = -1
        currPoint = Point3(0, 0, 0)
        for i in range(len(self.curvePoints)):
            currPoint = self.curvePoints[i]
            currLength2 = (pos - currPoint).lengthSquared()
            if currLength2 < minLength2:
                minLength2 = currLength2
                minIndex = i

        currPoint = self.curvePoints[minIndex]
        if minIndex + 1 == len(self.curvePoints):
            nextPoint = self.curvePoints[0]
        else:
            nextPoint = self.curvePoints[minIndex + 1]
        if minIndex - 1 < 0:
            prevIndex = len(self.curvePoints) - 1
        else:
            prevIndex = minIndex - 1
        forwardSegment = nextPoint - currPoint
        if (pos - currPoint).dot(forwardSegment) > 0:
            pole = minIndex
        else:
            pole = prevIndex
        currPoint = self.curvePoints[pole]
        nextPole = (pole + 1) % len(self.curvePoints)
        nextPoint = self.curvePoints[nextPole]
        segment = nextPoint - currPoint
        segment.setZ(0)
        segLength2 = segment.lengthSquared()
        posVector = pos - currPoint
        posVector.setZ(0)
        project = segment * (segment.dot(posVector) / segLength2)
        percent = project.lengthSquared() / segLength2
        if nextPole < pole:
            t = self.curveTs[pole] * (1 - percent) + self.curve.getMaxT() * percent
        else:
            t = self.curveTs[pole] * (1 - percent) + self.curveTs[nextPole] * percent
        return t

    def hasGag(self, slot, type, index):
        if self.gags[slot].isActive():
            self.gags[slot].disableGag()

    def leaveRace(self):
        self.fsm.request('leave')

    def racerLeft(self, avId):
        if avId != localAvatar.doId:
            self.gui.racerLeft(avId, unexpected=False)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        if self.hasFog:
            SkyUtil.startCloudSky(self, parent=self.dummyNode, effects=CompassEffect.PRot)
        else:
            SkyUtil.startCloudSky(self, parent=render)

    def stopSky(self):
        taskMgr.remove('skyTrack')

    def pickupGag(self, slot, index):
        self.canShoot = False
        standing = self.gui.racerDict[localAvatar.doId].place - 1
        self.currGag = RaceGlobals.GagFreq[standing][index]
        cycleTime = 2
        self.gui.waitingOnGag(cycleTime)
        taskMgr.doMethodLater(cycleTime, self.enableShoot, 'enableShoot')
        self.sendUpdate('hasGag', [slot, self.currGag, index])

    def shootGag(self):
        if self.canShoot:
            if self.currGag == 1:
                self.bananaSound.play()
                self.shootBanana()
            elif self.currGag == 2:
                self.d_requestThrow(0, 0, 0)
                self.localKart.startTurbo()
            elif self.currGag == 3:
                self.d_requestThrow(0, 0, 0)
            elif self.currGag == 4:
                self.bananaSound.play()
                self.shootPie()
            self.currGag = 0
            self.gui.updateGag(0)

    def enableShoot(self, t):
        self.canShoot = True
        if self.gui:
            self.gui.updateGag(self.currGag)

    def shootBanana(self):
        pos = self.localKart.getPos(render)
        banana = self.banana.copyTo(self.geom)
        banana.setPos(pos)
        self.thrownGags.append(banana)
        self.d_requestThrow(pos[0], pos[1], pos[2])

    def shootPie(self):
        pos = self.localKart.getPos(render)
        self.d_requestThrow(pos[0], pos[1], pos[2])

    def genArrows(self):
        base.arrows = []
        arrowId = 0
        for boost in RaceGlobals.TrackDict[self.trackId][5]:
            self.genArrow(boost[0], boost[1], arrowId)
            arrowId += 1

    def genArrow(self, pos, hpr, id):
        factory = CardMaker('factory')
        factory.setFrame(-0.5, 0.5, -0.5, 0.5)
        arrowNode = factory.generate()
        arrowRoot = NodePath('root')
        baseArrow = NodePath(arrowNode)
        baseArrow.setTransparency(1)
        baseArrow.setTexture(self.boostArrowTexture)
        baseArrow.reparentTo(arrowRoot)
        arrow2 = baseArrow.copyTo(baseArrow)
        arrow2.setPos(0, 0, 1)
        arrow3 = arrow2.copyTo(arrow2)
        arrowRoot.setPos(*pos)
        arrowRoot.setHpr(*hpr)
        baseArrow.setHpr(0, -90, 0)
        baseArrow.setScale(24)
        arrowRoot.reparentTo(self.geom)
        trigger = 'boostArrow' + str(id)
        cs =
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\racing\DistributedRace.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'DNAStorage'
3	CALL_FUNCTION_0   None
6	LOAD_FAST         'self'
9	STORE_ATTR        'dnaStore'

12	LOAD_GLOBAL       'loader'
15	LOAD_ATTR         'loadDNAFile'
18	LOAD_FAST         'self'
21	LOAD_ATTR         'dnaStore'
24	LOAD_CONST        'phase_4/dna/storage.dna'
27	CALL_FUNCTION_2   None
30	POP_TOP           None

31	LOAD_GLOBAL       'loader'
34	LOAD_ATTR         'loadDNAFile'
37	LOAD_FAST         'self'
40	LOAD_ATTR         'dnaStore'
43	LOAD_CONST        'phase_5/dna/storage_town.dna'
46	CALL_FUNCTION_2   None
49	POP_TOP           None

50	LOAD_GLOBAL       'loader'
53	LOAD_ATTR         'loadDNAFile'
56	LOAD_FAST         'self'
59	LOAD_ATTR         'dnaStore'
62	LOAD_CONST        'phase_4/dna/storage_TT.dna'
65	CALL_FUNCTION_2   None
68	POP_TOP           None

69	LOAD_GLOBAL       'loader'
72	LOAD_ATTR         'loadDNAFile'
75	LOAD_FAST         'self'
78	LOAD_ATTR         'dnaStore'
81	LOAD_CONST        'phase_5/dna/storage_TT_town.dna'
84	CALL_FUNCTION_2   None
87	POP_TOP           None

88	LOAD_GLOBAL       'loader'
91	LOAD_ATTR         'loadDNAFile'
94	LOAD_FAST         'self'
97	LOAD_ATTR         'dnaStore'
100	LOAD_CONST        'phase_8/dna/storage_BR.dna'
103	CALL_FUNCTION_2   None
106	POP_TOP           None

107	LOAD_GLOBAL       'loader'
110	LOAD_ATTR         'loadDNAFile'
113	LOAD_FAST         'self'
116	LOAD_ATTR         'dnaStore'
119	LOAD_CONST        'phase_8/dna/storage_BR_town.dna'
122	CALL_FUNCTION_2   None
125	POP_TOP           None

126	LOAD_CONST        'phase_6/dna/urban_track_town.dna'
129	STORE_FAST        'dnaFile'

132	LOAD_FAST         'self'
135	LOAD_ATTR         'trackId'
138	LOAD_GLOBAL       'RaceGlobals'
141	LOAD_ATTR         'RT_Urban_2'
144	LOAD_GLOBAL       'RaceGlobals'
147	LOAD_ATTR         'RT_Urban_2_rev'
150	BUILD_TUPLE_2     None
153	COMPARE_OP        'in'
156	JUMP_IF_FALSE     '168'

159	LOAD_CONST        'phase_6/dna/urban_track_town_B.dna'
162	STORE_FAST        'dnaFile'
165	JUMP_FORWARD      '168'
168_0	COME_FROM         '165'

168	LOAD_GLOBAL       'loader'
171	LOAD_ATTR         'loadDNAFile'
174	LOAD_FAST         'self'
177	LOAD_ATTR         'dnaStore'
180	LOAD_FAST         'dnaFile'
183	CALL_FUNCTION_2   None
186	STORE_FAST        'node'

189	LOAD_FAST         'self'
192	LOAD_ATTR         'geom'
195	LOAD_ATTR         'attachNewNode'
198	LOAD_FAST         'node'
201	CALL_FUNCTION_1   None
204	LOAD_FAST         'self'
207	STORE_ATTR        'townGeom'

210	LOAD_FAST         'self'
213	LOAD_ATTR         'townGeom'
216	LOAD_ATTR         'findAllMatches'
219	LOAD_CONST        '**/+CollisionNode'
222	CALL_FUNCTION_1   None
225	LOAD_ATTR         'stash'
228	CALL_FUNCTION_0   None
231	POP_TOP           None

232	BUILD_MAP         None
235	LOAD_FAST         'self'
238	STORE_ATTR        'buildingGroups'

241	BUILD_MAP         None
244	LOAD_FAST         'self'
247	STORE_ATTR        'currBldgInd'

250	BUILD_MAP         None
253	LOAD_FAST         'self'
256	STORE_ATTR        'currBldgGroups'

259	LOAD_FAST         'self'
262	LOAD_ATTR         'geom'
265	LOAD_ATTR         'find'
268	LOAD_CONST        '**/polySurface8'
271	CALL_FUNCTION_1   None
274	STORE_FAST        'bgGeom'

277	LOAD_FAST         'self'
280	LOAD_ATTR         'dummyNode'
283	JUMP_IF_FALSE     '305'

286	LOAD_FAST         'bgGeom'
289	LOAD_ATTR         'reparentTo'
292	LOAD_FAST         'self'
295	LOAD_ATTR         'dummyNode'
298	CALL_FUNCTION_1   None
301	POP_TOP           None
302	JUMP_FORWARD      '318'

305	LOAD_FAST         'bgGeom'
308	LOAD_ATTR         'reparentTo'
311	LOAD_GLOBAL       'localAvatar'
314	CALL_FUNCTION_1   None
317	POP_TOP           None
318_0	COME_FROM         '302'

318	LOAD_FAST         'bgGeom'
321	LOAD_ATTR         'setScale'
324	LOAD_CONST        0.1
327	CALL_FUNCTION_1   None
330	POP_TOP           None

331	LOAD_GLOBAL       'CompassEffect'
334	LOAD_ATTR         'make'
337	LOAD_GLOBAL       'NodePath'
340	CALL_FUNCTION_0   None
343	LOAD_GLOBAL       'CompassEffect'
346	LOAD_ATTR         'PRot'
349	CALL_FUNCTION_2   None
352	STORE_FAST        'ce'

355	LOAD_FAST         'bgGeom'
358	LOAD_ATTR         'node'
361	CALL_FUNCTION_0   None
364	LOAD_ATTR         'setEffect'
367	LOAD_FAST         'ce'
370	CALL_FUNCTION_1   None
373	POP_TOP           None

374	LOAD_FAST         'bgGeom'
377	LOAD_ATTR         'setDepthTest'
380	LOAD_CONST        0
383	CALL_FUNCTION_1   None
386	POP_TOP           None

387	LOAD_FAST         'bgGeom'
390	LOAD_ATTR         'setDepthWrite'
393	LOAD_CONST        0
396	CALL_FUNCTION_1   None
399	POP_TOP           None

400	LOAD_FAST         'bgGeom'
403	LOAD_ATTR         'setBin'
406	LOAD_CONST        'background'
409	LOAD_CONST        102
412	CALL_FUNCTION_2   None
415	POP_TOP           None

416	LOAD_FAST         'bgGeom'
419	LOAD_ATTR         'setZ'
422	LOAD_CONST        -1
425	CALL_FUNCTION_1   None
428	POP_TOP           None

429	LOAD_FAST         'bgGeom'
432	LOAD_FAST         'self'
435	STORE_ATTR        'bgGeom'

438	LOAD_FAST         'self'
441	LOAD_ATTR         'geom'
444	LOAD_ATTR         'findAllMatches'
447	LOAD_CONST        '**/+ModelNode'
450	CALL_FUNCTION_1   None
453	STORE_FAST        'l'

456	SETUP_LOOP        '492'
459	LOAD_FAST         'l'
462	GET_ITER          None
463	FOR_ITER          '491'
466	STORE_FAST        'n'

469	LOAD_FAST         'n'
472	LOAD_ATTR         'node'
475	CALL_FUNCTION_0   None
478	LOAD_ATTR         'setPreserveTransform'
481	LOAD_CONST        0
484	CALL_FUNCTION_1   None
487	POP_TOP           None
488	JUMP_BACK         '463'
491	POP_BLOCK         None
492_0	COME_FROM         '456'

492	LOAD_FAST         'self'
495	LOAD_ATTR         'geom'
498	LOAD_ATTR         'flattenLight'
501	CALL_FUNCTION_0   None
504	POP_TOP           None

505	LOAD_CONST        0
508	STORE_FAST        'maxNum'

511	SETUP_LOOP        '817'
514	LOAD_CONST        'inner'
517	LOAD_CONST        'outer'
520	BUILD_LIST_2      None
523	GET_ITER          None
524	FOR_ITER          '816'
527	STORE_FAST        'side'

530	BUILD_LIST_0      None
533	LOAD_FAST         'self'
536	LOAD_ATTR         'buildingGroups'
539	LOAD_FAST         'side'
542	STORE_SUBSCR      None

543	LOAD_CONST        None
546	LOAD_FAST         'self'
549	LOAD_ATTR         'currBldgInd'
552	LOAD_FAST         'side'
555	STORE_SUBSCR      None

556	LOAD_CONST        None
559	LOAD_FAST         'self'
562	LOAD_ATTR         'currBldgGroups'
565	LOAD_FAST         'side'
568	STORE_SUBSCR      None

569	LOAD_CONST        0
572	STORE_FAST        'i'

575	SETUP_LOOP        '792'

578	LOAD_FAST         'self'
581	LOAD_ATTR         'townGeom'
584	LOAD_ATTR         'find'
587	LOAD_CONST        '**/Buildings_'
590	LOAD_FAST         'side'
593	BINARY_ADD        None
594	LOAD_CONST        '-'
597	BINARY_ADD        None
598	LOAD_GLOBAL       'str'
601	LOAD_FAST         'i'
604	CALL_FUNCTION_1   None
607	BINARY_ADD        None
608	CALL_FUNCTION_1   None
611	STORE_FAST        'bldgGroup'

614	LOAD_FAST         'bldgGroup'
617	LOAD_ATTR         'isEmpty'
620	CALL_FUNCTION_0   None
623	JUMP_IF_FALSE     '630'

626	BREAK_LOOP        None
627	JUMP_FORWARD      '630'
630_0	COME_FROM         '627'

630	LOAD_FAST         'bldgGroup'
633	LOAD_ATTR         'findAllMatches'
636	LOAD_CONST        '**/+ModelNode'
639	CALL_FUNCTION_1   None
642	STORE_FAST        'l'

645	SETUP_LOOP        '718'
648	LOAD_FAST         'l'
651	GET_ITER          None
652	FOR_ITER          '717'
655	STORE_FAST        'n'

658	LOAD_FAST         'n'
661	LOAD_ATTR         'getParent'
664	CALL_FUNCTION_0   None
667	LOAD_ATTR         'attachNewNode'
670	LOAD_FAST         'n'
673	LOAD_ATTR         'getName'
676	CALL_FUNCTION_0   None
679	CALL_FUNCTION_1   None
682	STORE_FAST        'n2'

685	LOAD_FAST         'n'
688	LOAD_ATTR         'getChildren'
691	CALL_FUNCTION_0   None
694	LOAD_ATTR         'reparentTo'
697	LOAD_FAST         'n2'
700	CALL_FUNCTION_1   None
703	POP_TOP           None

704	LOAD_FAST         'n'
707	LOAD_ATTR         'removeNode'
710	CALL_FUNCTION_0   None
713	POP_TOP           None
714	JUMP_BACK         '652'
717	POP_BLOCK         None
718_0	COME_FROM         '645'

718	LOAD_FAST         'bldgGroup'
721	LOAD_ATTR         'flattenStrong'
724	CALL_FUNCTION_0   None
727	POP_TOP           None

728	LOAD_FAST         'bldgGroup'
731	LOAD_ATTR         'getNode'
734	LOAD_CONST        0
737	CALL_FUNCTION_1   None
740	LOAD_ATTR         'getBounds'
743	CALL_FUNCTION_0   None
746	LOAD_ATTR         'isEmpty'
749	CALL_FUNCTION_0   None
752	JUMP_IF_TRUE      '778'

755	LOAD_FAST         'self'
758	LOAD_ATTR         'buildingGroups'
761	LOAD_FAST         'side'
764	BINARY_SUBSCR     None
765	LOAD_ATTR         'append'
768	LOAD_FAST         'bldgGroup'
771	CALL_FUNCTION_1   None
774	POP_TOP           None
775	JUMP_FORWARD      '778'
778_0	COME_FROM         '775'

778	LOAD_FAST         'i'
781	LOAD_CONST        1
784	INPLACE_ADD       None
785	STORE_FAST        'i'
788	JUMP_BACK         '578'
791	POP_BLOCK         None
792_0	COME_FROM         '575'

792	LOAD_FAST         'i'
795	LOAD_FAST         'maxNum'
798	COMPARE_OP        '>'
801	JUMP_IF_FALSE     '813'

804	LOAD_FAST         'i'
807	STORE_FAST        'maxNum'
810	JUMP_BACK         '524'
813	JUMP_BACK         '524'
816	POP_BLOCK         None
817_0	COME_FROM         '511'

817	SETUP_LOOP        '1089'
820	LOAD_CONST        'innersidest'
823	LOAD_CONST        'outersidest'
826	BUILD_LIST_2      None
829	GET_ITER          None
830	FOR_ITER          '1088'
833	STORE_FAST        'side'

836	BUILD_LIST_0      None
839	LOAD_FAST         'self'
842	LOAD_ATTR         'buildingGroups'
845	LOAD_FAST         'side'
848	STORE_SUBSCR      None

849	LOAD_CONST        None
852	LOAD_FAST         'self'
855	LOAD_ATTR         'currBldgInd'
858	LOAD_FAST         'side'
861	STORE_SUBSCR      None

862	LOAD_CONST        None
865	LOAD_FAST         'self'
868	LOAD_ATTR         'currBldgGroups'
871	LOAD_FAST         'side'
874	STORE_SUBSCR      None

875	SETUP_LOOP        '1085'
878	LOAD_GLOBAL       'range'
881	LOAD_FAST         'maxNum'
884	CALL_FUNCTION_1   None
887	GET_ITER          None
888	FOR_ITER          '1084'
891	STORE_FAST        'i'

894	SETUP_LOOP        '1081'
897	LOAD_CONST        ('innerbarricade', 'outerbarricade')
900	GET_ITER          None
901	FOR_ITER          '1080'
904	STORE_FAST        'barricade'

907	LOAD_FAST         'self'
910	LOAD_ATTR         'townGeom'
913	LOAD_ATTR         'find'
916	LOAD_CONST        '**/Buildings_'
919	LOAD_FAST         'side'
922	BINARY_ADD        None
923	LOAD_CONST        '-'
926	BINARY_ADD        None
927	LOAD_FAST         'barricade'
930	BINARY_ADD        None
931	LOAD_CONST        '_'
934	BINARY_ADD        None
935	LOAD_GLOBAL       'str'
938	LOAD_FAST         'i'
941	CALL_FUNCTION_1   None
944	BINARY_ADD        None
945	CALL_FUNCTION_1   None
948	STORE_FAST        'bldgGroup'

951	LOAD_FAST         'bldgGroup'
954	LOAD_ATTR         'isEmpty'
957	CALL_FUNCTION_0   None
960	JUMP_IF_FALSE     '969'

963	CONTINUE          '901'
966	JUMP_FORWARD      '969'
969_0	COME_FROM         '966'

969	LOAD_FAST         'bldgGroup'
972	LOAD_ATTR         'findAllMatches'
975	LOAD_CONST        '**/+ModelNode'
978	CALL_FUNCTION_1   None
981	STORE_FAST        'l'

984	SETUP_LOOP        '1057'
987	LOAD_FAST         'l'
990	GET_ITER          None
991	FOR_ITER          '1056'
994	STORE_FAST        'n'

997	LOAD_FAST         'n'
1000	LOAD_ATTR         'getParent'
1003	CALL_FUNCTION_0   None
1006	LOAD_ATTR         'attachNewNode'
1009	LOAD_FAST         'n'
1012	LOAD_ATTR         'getName'
1015	CALL_FUNCTION_0   None
1018	CALL_FUNCTION_1   None
1021	STORE_FAST        'n2'

1024	LOAD_FAST         'n'
1027	LOAD_ATTR         'getChildren'
1030	CALL_FUNCTIO CollisionTube(Point3(0.6, -6, 0), Point3(0.6, 54, 0), 4.8)
        cs.setTangible(0)
        triggerEvent = 'imIn-' + trigger
        cn = CollisionNode(trigger)
        cn.addSolid(cs)
        cn.setIntoCollideMask(BitMask32(32768))
        cn.setFromCollideMask(BitMask32(32768))
        cnp = NodePath(cn)
        cnp.reparentTo(arrowRoot)
        self.accept(triggerEvent, self.hitBoostArrow)
        arrowVec = arrow2.getPos(self.geom) - baseArrow.getPos(self.geom)
        arrowVec.normalize()
        idStr = str(id)
        cnp.setTag('boostId', idStr)
        self.boostDir[idStr] = arrowVec
        base.arrows.append(arrowRoot)

    def hitBoostArrow(self, cevent):
        into = cevent.getIntoNodePath()
        idStr = into.getTag('boostId')
        arrowVec = self.boostDir.get(idStr)
        if arrowVec == None:
            print 'Unknown boost arrow %s' % idStr
            return
        fvec = self.localKart.forward.getPos(self.geom) - self.localKart.getPos(self.geom)
        fvec.normalize()
        dotP = arrowVec.dot(fvec)
        if dotP > 0.7:
            self.localKart.startTurbo()
        return

    def fadeOutMusic(self):
        if self.musicTrack:
            self.musicTrack.finish()
        curVol = self.raceMusic.getVolume()
        interval = LerpFunctionInterval(self.raceMusic.setVolume, fromData=curVol, toData=0, duration=3)
        self.musicTrack = Sequence(interval)
        self.musicTrack.start()

    def changeMusicTempo(self, newPR):
        if self.musicTrack:
            self.musicTrack.finish()
        curPR = self.raceMusic.getPlayRate()
        interval = LerpFunctionInterval(self.raceMusic.setPlayRate, fromData=curPR, toData=newPR, duration=3)
        self.musicTrack = Sequence(interval)
        self.musicTrack.start()

    def setRaceZone(self, zoneId, trackId):
        hoodId = self.cr.playGame.hood.hoodId
        base.loader.endBulkLoad('atRace')
        self.kartCleanup()
        self.doneBarrier('waitingForExit')
        self.sendUpdate('racerLeft', [localAvatar.doId])
        out = {'loader': 'racetrack',
         'where': 'racetrack',
         'hoodId': hoodId,
         'zoneId': zoneId,
         'trackId': trackId,
         'shardId': None,
         'reason': RaceGlobals.Exit_UserReq}
        base.cr.playGame.hood.loader.fsm.request('quietZone', [out])
        return
N_0   None
1033	LOAD_ATTR         'reparentTo'
1036	LOAD_FAST         'n2'
1039	CALL_FUNCTION_1   None
1042	POP_TOP           None

1043	LOAD_FAST         'n'
1046	LOAD_ATTR         'removeNode'
1049	CALL_FUNCTION_0   None
1052	POP_TOP           None
1053	JUMP_BACK         '991'
1056	POP_BLOCK         None
1057_0	COME_FROM         '984'

1057	LOAD_FAST         'self'
1060	LOAD_ATTR         'buildingGroups'
1063	LOAD_FAST         'side'
1066	BINARY_SUBSCR     None
1067	LOAD_ATTR         'append'
1070	LOAD_FAST         'bldgGroup'
1073	CALL_FUNCTION_1   None
1076	POP_TOP           None
1077	JUMP_BACK         '901'
1080	POP_BLOCK         None
1081_0	COME_FROM         '894'
1081	JUMP_BACK         '888'
1084	POP_BLOCK         None
1085_0	COME_FROM         '875'
1085	JUMP_BACK         '830'
1088	POP_BLOCK         None
1089_0	COME_FROM         '817'

1089	LOAD_FAST         'self'
1092	LOAD_ATTR         'townGeom'
1095	LOAD_ATTR         'findAllMatches'
1098	LOAD_CONST        '**/prop_tree_*'
1101	CALL_FUNCTION_1   None
1104	STORE_FAST        'treeNodes'

1107	SETUP_LOOP        '1134'
1110	LOAD_FAST         'treeNodes'
1113	GET_ITER          None
1114	FOR_ITER          '1133'
1117	STORE_FAST        'tree'

1120	LOAD_FAST         'tree'
1123	LOAD_ATTR         'flattenStrong'
1126	CALL_FUNCTION_0   None
1129	POP_TOP           None
1130	JUMP_BACK         '1114'
1133	POP_BLOCK         None
1134_0	COME_FROM         '1107'

1134	LOAD_FAST         'self'
1137	LOAD_ATTR         'townGeom'
1140	LOAD_ATTR         'findAllMatches'
1143	LOAD_CONST        '**/prop_snow_tree_*'
1146	CALL_FUNCTION_1   None
1149	STORE_FAST        'snowTreeNodes'

1152	SETUP_LOOP        '1179'
1155	LOAD_FAST         'snowTreeNodes'
1158	GET_ITER          None
1159	FOR_ITER          '1178'
1162	STORE_FAST        'snowTree'

1165	LOAD_FAST         'snowTree'
1168	LOAD_ATTR         'flattenStrong'
1171	CALL_FUNCTION_0   None
1174	POP_TOP           None
1175	JUMP_BACK         '1159'
1178	POP_BLOCK         None
1179_0	COME_FROM         '1152'

1179	SETUP_LOOP        '1242'
1182	LOAD_CONST        'inner'
1185	LOAD_CONST        'outer'
1188	LOAD_CONST        'innersidest'
1191	LOAD_CONST        'outersidest'
1194	BUILD_LIST_4      None
1197	GET_ITER          None
1198	FOR_ITER          '1241'
1201	STORE_FAST        'side'

1204	SETUP_LOOP        '1238'
1207	LOAD_FAST         'self'
1210	LOAD_ATTR         'buildingGroups'
1213	LOAD_FAST         'side'
1216	BINARY_SUBSCR     None
1217	GET_ITER          None
1218	FOR_ITER          '1237'
1221	STORE_FAST        'grp'

1224	LOAD_FAST         'grp'
1227	LOAD_ATTR         'stash'
1230	CALL_FUNCTION_0   None
1233	POP_TOP           None
1234	JUMP_BACK         '1218'
1237	POP_BLOCK         None
1238_0	COME_FROM         '1204'
1238	JUMP_BACK         '1198'
1241	POP_BLOCK         None
1242_0	COME_FROM         '1179'

1242	LOAD_FAST         'self'
1245	LOAD_ATTR         'showBuildings'
1248	LOAD_CONST        0
1251	CALL_FUNCTION_1   None
1254	POP_TOP           None
1255	LOAD_CONST        None
1258	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 791

