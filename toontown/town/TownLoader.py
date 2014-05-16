from pandac.PandaModules import *
from toontown.battle.BattleProps import *
from toontown.battle.BattleSounds import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import cleanupDialog
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import TownBattle
from toontown.toon import Toon
from toontown.toon import NPCToons
from otp.nametag.NametagConstants import *
from toontown.toon.Toon import teleportDebug
from toontown.battle import BattleParticles
from direct.fsm import StateData
from toontown.building import ToonInterior
from toontown.hood import QuietZoneState
from toontown.hood import ZoneUtil
from random import randint

class TownLoader(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.hood = hood
        self.parentFSMState = parentFSMState
        self.fsm = ClassicFSM.ClassicFSM('TownLoader', [State.State('start', self.enterStart, self.exitStart, ['quietZone', 'street', 'toonInterior']),
         State.State('street', self.enterStreet, self.exitStreet, ['quietZone']),
         State.State('toonInterior', self.enterToonInterior, self.exitToonInterior, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['street', 'toonInterior']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')
        self.branchZone = None
        self.canonicalBranchZone = None
        self.placeDoneEvent = 'placeDone'
        self.townBattleDoneEvent = 'town-battle-done'
        return

    def loadBattleAnims(self):
        Toon.loadBattleAnims()

    def unloadBattleAnims(self):
        Toon.unloadBattleAnims()

    def load(self, zoneId):
        self.zoneId = zoneId
        self.parentFSMState.addChild(self.fsm)
        self.loadBattleAnims()
        self.branchZone = ZoneUtil.getBranchZone(zoneId)
        self.canonicalBranchZone = ZoneUtil.getCanonicalBranchZone(zoneId)
        self.music = base.loadMusic(self.musicFile)
        self.activityMusic = base.loadMusic(self.activityMusicFile)
        self.battleMusic = base.loadMusic('phase_3.5/audio/bgm/encntr_general_bg.ogg')
        self.townBattle = TownBattle.TownBattle(self.townBattleDoneEvent)
        self.townBattle.load()

        if base.config.GetBool('want-april-toons', 0):
            self.npc = NPCToons.createLocalNPC(91915)
            self.npc.reparentTo(base.localAvatar)
            self.npc.setZ(30)
            self.npc.hide()
            self.piano = loader.loadModel('phase_5/models/props/piano-mod')
            self.piano.setZ(250)
            self.piano.setHpr(0, 90, 0)
            self.piano.reparentTo(base.localAvatar)
            self.piano.setScale(0)
            self.pianoSfx = base.loadSfx('phase_5/audio/sfx/AA_drop_piano.ogg')
            self.dropSfx = base.loadSfx('phase_5/audio/sfx/cogbldg_drop.ogg')
            self.pianoDropSound = Sequence(
                Func(base.playSfx, self.dropSfx),
                Wait(6.7),
                Func(base.playSfx, self.pianoSfx),
                Func(base.localAvatar.b_setAnimState, 'Squish'),
                Wait(2.5),
                Func(self.pianoSfx.stop)
            )
            self.pianoDropSequence = Sequence(
                Wait(randint(10, 60)),
                Func(self.pianoDropSound.start),
                Parallel(self.piano.scaleInterval(1, (3, 3, 3)), self.piano.posInterval(7, (0, 0, 0))),
                self.piano.posInterval(0.1, (0, 0, 0.5)),
                self.piano.posInterval(0.1, (0, 0, 0)),
                Wait(0.4),
                Parallel(Func(self.npc.addActive), Func(self.npc.setChatAbsolute, 'Whoops! My bad!', CFSpeech|CFTimeout)),
                self.piano.scaleInterval(1, (0, 0, 0)),
                Wait(5),
                Func(self.npc.removeActive)
            )
            self.pianoDropSequence.loop()

    def unload(self):
        self.unloadBattleAnims()
        globalPropPool.unloadProps()
        globalBattleSoundCache.clear()
        BattleParticles.unloadParticles()
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        del self.fsm
        del self.streetClass
        self.landmarkBlocks.removeNode()
        del self.landmarkBlocks
        del self.hood
        del self.nodeDict
        del self.zoneDict
        del self.nodeToZone
        del self.fadeInDict
        del self.fadeOutDict
        del self.nodeList
        self.geom.removeNode()
        del self.geom
        self.townBattle.unload()
        self.townBattle.cleanup()
        del self.townBattle
        del self.battleMusic
        del self.music
        del self.activityMusic
        del self.holidayPropTransforms
        self.deleteAnimatedProps()
        cleanupDialog('globalDialog')
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        if base.config.GetBool('want-april-toons', 0):
            self.pianoDropSequence.finish()
            self.pianoDropSound.finish()
            del self.pianoDropSequence
            del self.pianoDropSound
            self.piano.removeNode()
            del self.pianoSfx
            del self.dropSfx
            del self.npc

    def enter(self, requestStatus):
        teleportDebug(requestStatus, 'TownLoader.enter(%s)' % requestStatus)
        self.fsm.enterInitialState()
        teleportDebug(requestStatus, 'setting state: %s' % requestStatus['where'])
        self.setState(requestStatus['where'], requestStatus)

    def exit(self):
        self.ignoreAll()

    def setState(self, stateName, requestStatus):
        self.fsm.request(stateName, [requestStatus])

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def enterStreet(self, requestStatus):
        teleportDebug(requestStatus, 'enterStreet(%s)' % requestStatus)
        self.acceptOnce(self.placeDoneEvent, self.streetDone)
        self.place = self.streetClass(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        base.cr.playGame.setPlace(self.place)
        self.place.enter(requestStatus)

    def exitStreet(self):
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def streetDone(self):
        self.requestStatus = self.place.doneStatus
        status = self.place.doneStatus
        if status['loader'] == 'townLoader' and ZoneUtil.getBranchZone(status['zoneId']) == self.branchZone and status['shardId'] == None:
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)
        return

    def enterToonInterior(self, requestStatus):
        self.acceptOnce(self.placeDoneEvent, self.handleToonInteriorDone)
        self.place = ToonInterior.ToonInterior(self, self.fsm.getStateNamed('toonInterior'), self.placeDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)

    def exitToonInterior(self):
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def handleToonInteriorDone(self):
        status = self.place.doneStatus
        if ZoneUtil.getBranchZone(status['zoneId']) == self.branchZone and status['shardId'] == None:
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)
        return

    def enterQuietZone(self, requestStatus):
        self.quietZoneDoneEvent = uniqueName('quietZoneDone')
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData = None
        return

    def handleQuietZoneDone(self):
        status = self.quietZoneStateData.getRequestStatus()
        self.fsm.request(status['where'], [status])

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass

    def createHood(self, dnaFile, loadStorage = 1):
        if loadStorage:
            loader.loadDNA('phase_5/dna/storage_town.xml').store(self.hood.dnaStore)
            self.notify.debug('done loading %s' % 'phase_5/dna/storage_town.xml')
            loader.loadDNA(self.townStorageDNAFile).store(self.hood.dnaStore)
            self.notify.debug('done loading %s' % self.townStorageDNAFile)
        sceneTree = loader.loadDNA(dnaFile)
        node = sceneTree.generate(self.hood.dnaStore)
        base.cr.playGame.dnaData = sceneTree.generateData()
        self.notify.debug('done loading %s' % dnaFile)
        if node.getNumParents() == 1:
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            self.geom = hidden.attachNewNode(node)
        self.makeDictionaries(sceneTree)
        self.reparentLandmarkBlockNodes()
        self.renameFloorPolys(self.nodeList)
        self.createAnimatedProps(self.nodeList)
        self.holidayPropTransforms = {}
        npl = self.geom.findAllMatches('**/=DNARoot=holiday_prop')
        for i in range(npl.getNumPaths()):
            np = npl.getPath(i)
            np.setTag('transformIndex', `i`)
            self.holidayPropTransforms[i] = np.getNetTransform()

        self.notify.info('skipping self.geom.flattenMedium')
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)
        self.geom.setName('town_top_level')

    def reparentLandmarkBlockNodes(self):
        bucket = self.landmarkBlocks = hidden.attachNewNode('landmarkBlocks')
        npc = self.geom.findAllMatches('**/sb*:*_landmark_*_DNARoot')
        for i in range(npc.getNumPaths()):
            nodePath = npc.getPath(i)
            nodePath.wrtReparentTo(bucket)

        npc = self.geom.findAllMatches('**/sb*:*animated_building*_DNARoot')
        for i in range(npc.getNumPaths()):
            nodePath = npc.getPath(i)
            nodePath.wrtReparentTo(bucket)

    def makeDictionaries(self, sceneTree):
        self.nodeDict = {}
        self.zoneDict = {}
        self.nodeToZone = {}
        self.nodeList = []
        self.fadeInDict = {}
        self.fadeOutDict = {}
        a1 = Vec4(1, 1, 1, 1)
        a0 = Vec4(1, 1, 1, 0)
        for visgroup in base.cr.playGame.dnaData.visgroups:
            groupName = base.cr.hoodMgr.extractGroupName(visgroup.name)
            zoneId = int(groupName)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            groupNode = self.geom.find('**/' + visgroup.name)
            if groupNode.isEmpty():
                self.notify.error('Could not find visgroup')
            else:
                if ':' in groupName:
                    groupName = '%s%s' % (zoneId, groupName[groupName.index(':'):])
                else:
                    groupName = '%s' % zoneId
                groupNode.setName(groupName)
            self.nodeDict[zoneId] = []
            self.nodeList.append(groupNode)
            self.zoneDict[zoneId] = groupNode
            self.nodeToZone[groupNode] = zoneId
            fadeDuration = 0.5
            self.fadeOutDict[groupNode] = Sequence(Func(groupNode.setTransparency, 1), LerpColorScaleInterval(groupNode, fadeDuration, a0, startColorScale=a1), Func(groupNode.clearColorScale), Func(groupNode.clearTransparency), Func(groupNode.stash), name='fadeZone-' + str(zoneId), autoPause=1)
            self.fadeInDict[groupNode] = Sequence(Func(groupNode.unstash), Func(groupNode.setTransparency, 1), LerpColorScaleInterval(groupNode, fadeDuration, a1, startColorScale=a0), Func(groupNode.clearColorScale), Func(groupNode.clearTransparency), name='fadeZone-' + str(zoneId), autoPause=1)

        for visgroup in base.cr.playGame.dnaData.visgroups:
            zoneId = int(base.cr.hoodMgr.extractGroupName(visgroup.name))
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            for visName in visgroup.vis:
                groupName = base.cr.hoodMgr.extractGroupName(visName)
                nextZoneId = int(groupName)
                nextZoneId = ZoneUtil.getTrueZoneId(nextZoneId, self.zoneId)
                visNode = self.zoneDict[nextZoneId]
                self.nodeDict[zoneId].append(visNode)

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

    def createAnimatedProps(self, nodeList):
        self.animPropDict = {}
        self.zoneIdToInteractivePropDict = {}
        for i in nodeList:
            animPropNodes = i.findAllMatches('**/animated_prop_*')
            numAnimPropNodes = animPropNodes.getNumPaths()
            for j in range(numAnimPropNodes):
                animPropNode = animPropNodes.getPath(j)
                if animPropNode.getName().startswith('animated_prop_generic'):
                    className = 'GenericAnimatedProp'
                elif animPropNode.getName().startswith('animated_prop_'):
                    name = animPropNode.getName()[len('animated_prop_'):]
                    splits = name.split('_')
                    className = splits[0]
                else:
                    className = animPropNode.getName()[14:-8]
                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])
                classObj = getattr(symbols[className], className)
                animPropObj = classObj(animPropNode)
                animPropList = self.animPropDict.setdefault(i, [])
                animPropList.append(animPropObj)

            interactivePropNodes = i.findAllMatches('**/interactive_prop_*')
            numInteractivePropNodes = interactivePropNodes.getNumPaths()
            for j in range(numInteractivePropNodes):
                interactivePropNode = interactivePropNodes.getPath(j)
                className = 'InteractiveAnimatedProp'
                if 'hydrant' in interactivePropNode.getName():
                    className = 'HydrantInteractiveProp'
                elif 'trashcan' in interactivePropNode.getName():
                    className = 'TrashcanInteractiveProp'
                elif 'mailbox' in interactivePropNode.getName():
                    className = 'MailboxInteractiveProp'
                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])
                classObj = getattr(symbols[className], className)
                interactivePropObj = classObj(interactivePropNode)
                animPropList = self.animPropDict.get(i)
                if animPropList is None:
                    animPropList = self.animPropDict.setdefault(i, [])
                animPropList.append(interactivePropObj)
                if interactivePropObj.getCellIndex() == 0:
                    zoneId = int(i.getName())
                    if zoneId not in self.zoneIdToInteractivePropDict:
                        self.zoneIdToInteractivePropDict[zoneId] = interactivePropObj
                    else:
                        self.notify.error('already have interactive prop %s in zone %s' % (self.zoneIdToInteractivePropDict, zoneId))

            animatedBuildingNodes = i.findAllMatches('**/*:animated_building_*;-h')
            for np in animatedBuildingNodes:
                if np.getName().startswith('sb'):
                    animatedBuildingNodes.removePath(np)

            numAnimatedBuildingNodes = animatedBuildingNodes.getNumPaths()
            for j in range(numAnimatedBuildingNodes):
                animatedBuildingNode = animatedBuildingNodes.getPath(j)
                className = 'GenericAnimatedBuilding'
                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])
                classObj = getattr(symbols[className], className)
                animatedBuildingObj = classObj(animatedBuildingNode)
                animPropList = self.animPropDict.get(i)
                if animPropList is None:
                    animPropList = self.animPropDict.setdefault(i, [])
                animPropList.append(animatedBuildingObj)

        return

    def deleteAnimatedProps(self):
        for zoneNode, animPropList in self.animPropDict.items():
            for animProp in animPropList:
                animProp.delete()

        del self.animPropDict

    def enterAnimatedProps(self, zoneNode):
        for animProp in self.animPropDict.get(zoneNode, ()):
            animProp.enter()

    def exitAnimatedProps(self, zoneNode):
        for animProp in self.animPropDict.get(zoneNode, ()):
            animProp.exit()

    def getInteractiveProp(self, zoneId):
        result = None
        if zoneId in self.zoneIdToInteractivePropDict:
            result = self.zoneIdToInteractivePropDict[zoneId]
        return result
