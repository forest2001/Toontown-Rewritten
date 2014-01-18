from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM
from toontown.estate.DistributedEstateAI import DistributedEstateAI
from toontown.estate.DistributedHouseAI import DistributedHouseAI
import functools

class LoadHouseFSM(FSM):
    def __init__(self, mgr, estate, houseIndex, toon, callback):
        FSM.__init__(self, 'LoadHouseFSM')
        self.mgr = mgr
        self.estate = estate
        self.houseIndex = houseIndex
        self.toon = toon
        self.callback = callback

        self.newHouse = False
        self.done = False

    def start(self):
        # We have a few different cases here:
        if self.toon is None:
            # Case #1: There isn't a Toon in that estate slot. Make a blank house.

            # Because this state completes so fast, we'll use taskMgr to delay
            # it until the next iteration. This solves re-entrancy problems.
            taskMgr.doMethodLater(0.0, self.demand,
                                  'makeBlankHouse-%s' % id(self),
                                  extraArgs=['MakeBlankHouse'])
            return

        self.houseId = self.toon.get('setHouseId', [0])[0]
        if self.houseId  == 0:
            # Case #2: There is a Toon, but no setHouseId. Gotta make one.
            self.demand('CreateHouse')
        else:
            # Case #3: Toon with a setHouseId. Load it.
            self.demand('LoadHouse')

    def enterMakeBlankHouse(self):
        self.house = DistributedHouseAI(self.mgr.air)
        self.house.setHousePos(self.houseIndex)
        self.house.setColor(self.houseIndex)
        self.house.generateWithRequired(self.estate.zoneId)
        self.estate.houses[self.houseIndex] = self.house
        self.demand('Off')

    def enterCreateHouse(self):
        fields = {
            'setHouseType' : [0],
            'setGardenPos' : [0],
            'setAtticItems' : [''],
            'setInteriorItems' : [''],
            'setAtticWallpaper' : [''],
            'setInteriorWallpaper' : [''],
            'setAtticWindows' : [''],
            'setInteriorWindows' : [''],
            'setDeletedItems' : [''],
            # For if we're creating a blank house. We still need an index, however.
            'setName' : [self.toon['setName'][0]],
            'setAvatarId' : [self.toon['ID']],
        }

        self.mgr.air.dbInterface.createObject(
            self.mgr.air.dbId,
            self.mgr.air.dclassesByName['DistributedHouseAI'],
            fields,
            self.__handleCreate)

    def __handleCreate(self, doId):
        if self.state != 'CreateHouse':
            return

        # Update the avatar's houseId:
        av = self.mgr.air.doId2do.get(self.toon['ID'])
        if av:
            av.b_setHouseId(doId)
        else:
            self.mgr.air.dbInterface.updateObject(
                self.mgr.air.dbId,
                self.toon['ID'],
                self.mgr.air.dclassesByName['DistributedToonAI'],
                {'setHouseId': [doId]})

        self.houseId = doId
        self.newHouse = True
        self.demand('LoadHouse')

    def enterLoadHouse(self):
        # Activate the house:
        self.mgr.air.sendActivate(self.houseId, self.mgr.air.districtId, self.estate.zoneId,
                                  self.mgr.air.dclassesByName['DistributedHouseAI'],
                                  {'setHousePos': [self.houseIndex],
                                   'setColor': [self.houseIndex]})

        # Now we wait for the estate to show up... We do this by hanging a messenger
        # hook which the DistributedEstateAI throws once it spawns.
        self.acceptOnce('generate-%d' % self.houseId, self.__gotHouse)

    def __gotHouse(self, house):
        self.house = house

        if self.newHouse:
            self.house.initializeInterior()
            pass

        self.estate.houses[self.houseIndex] = self.house

        self.demand('Off')

    def exitLoadHouse(self):
        self.ignore('generate-%d' % self.houseId)

    def enterOff(self):
        self.done = True
        self.callback(self.house)

class LoadEstateFSM(FSM):
    def __init__(self, mgr, callback):
        FSM.__init__(self, 'LoadEstateFSM')
        self.mgr = mgr
        self.callback = callback

        self.estate = None

    def start(self, accountId, zoneId):
        self.accountId = accountId
        self.zoneId = zoneId
        self.demand('QueryAccount')

    def enterQueryAccount(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.accountId,
                                             self.__gotAccount)

    def __gotAccount(self, dclass, fields):
        if self.state != 'QueryAccount':
            return # We must have aborted or something...

        if dclass != self.mgr.air.dclassesByName['AccountAI']:
            self.mgr.notify.warning('Account %d has non-account dclass %d!' %
                                    (self.accountId, dclass))
            self.demand('Failure')
            return

        self.accountFields = fields

        self.estateId = fields.get('ESTATE_ID', 0)
        self.demand('QueryToons')

    def enterQueryToons(self):
        self.toonIds = self.accountFields.get('ACCOUNT_AV_SET', [0]*6)
        self.toons = {}

        for index, toonId in enumerate(self.toonIds):
            if toonId == 0:
                self.toons[index] = None
                continue
            self.mgr.air.dbInterface.queryObject(
                self.mgr.air.dbId, toonId,
                functools.partial(self.__gotToon, index=index))

    def __gotToon(self, dclass, fields, index):
        if self.state != 'QueryToons':
            return # We must have aborted or something...

        if dclass != self.mgr.air.dclassesByName['DistributedToonAI']:
            self.mgr.notify.warning('Account %d has avatar %d with non-Toon dclass %d!' %
                                    (self.accountId, self.toonIds[index], dclass))
            self.demand('Failure')
            return

        fields['ID'] = self.toonIds[index]
        self.toons[index] = fields
        if len(self.toons) == 6:
            self.__gotAllToons()

    def __gotAllToons(self):
        # Okay, we have all of our Toons, now we can proceed with estate!
        if self.estateId:
            # We already have an estate, load it!
            self.demand('LoadEstate')
        else:
            # We don't have one yet, make one!
            self.demand('CreateEstate')

    def enterCreateEstate(self):
        # We have to ask the DB server to construct a blank estate object...
        fields = {
            'setEstateType' : [0],
            'setDecorData' : [[]],
            'setLastEpochTimeStamp' : [0],
            'setRentalTimeStamp' : [0],
            'setRentalType' : [0],
            'setSlot0Items' : [[]],
            'setSlot1Items' : [[]],
            'setSlot2Items' : [[]],
            'setSlot3Items' : [[]],
            'setSlot4Items' : [[]],
            'setSlot5Items' : [[]],
        }

        self.mgr.air.dbInterface.createObject(
            self.mgr.air.dbId,
            self.mgr.air.dclassesByName['DistributedEstateAI'],
            fields,
            self.__handleEstateCreate)

    def __handleEstateCreate(self, estateId):
        if self.state != 'CreateEstate':
            return # We must have aborted or something...
        self.estateId = estateId
        self.demand('LoadEstate')

    def enterLoadEstate(self):
        # Activate the estate:
        self.mgr.air.sendActivate(self.estateId, self.mgr.air.districtId, self.zoneId)

        # Now we wait for the estate to show up... We do this by hanging a messenger
        # hook which the DistributedEstateAI throws once it spawns.
        self.acceptOnce('generate-%d' % self.estateId, self.__gotEstate)

    def __gotEstate(self, estate):
        self.estate = estate

        # Gotcha! Now we need to load houses:
        self.demand('LoadHouses')

    def exitLoadEstate(self):
        self.ignore('generate-%d' % self.estateId)

    def enterLoadHouses(self):
        self.houseFSMs = []

        for houseIndex in range(6):
            fsm = LoadHouseFSM(self.mgr, self.estate, houseIndex,
                               self.toons[houseIndex], self.__houseDone)
            self.houseFSMs.append(fsm)
            fsm.start()

    def __houseDone(self, house):
        if self.state != 'LoadHouses':
            # We aren't loading houses, so we probably got cancelled. Therefore,
            # the only sensible thing to do is simply destroy the house.
            house.requestDelete()
            return

        # A houseFSM just finished! Let's see if all of them are done:
        if all(houseFSM.done for houseFSM in self.houseFSMs):
            self.demand('Finished')

    def enterFinished(self):
        self.callback(True)

    def enterFailure(self):
        self.cancel()

        self.callback(False)

    def cancel(self):
        if self.estate:
            self.estate.destroy()
            self.estate = None

        self.demand('Off')

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        
    def getEstateZone(self):
        senderId = self.air.getAvatarIdFromSender()
        accId = self.air.getAccountIdFromSender()

        toon = self.air.doId2do.get(senderId)

        if not toon:
            self.air.writeServerEvent('suspicious', senderId, 'Sent getEstateZone() but not on district!')
            return

        estate = getattr(toon, 'estate', None)
        if estate:
            # They already have an estate loaded, so let's just return it:
            self.sendUpdateToAvatarId(senderId, 'setEstateZone', [senderId, estate.zoneId])
            return

        if getattr(toon, 'loadEstateFSM', None):
            # We already have a loading operation underway; ignore this second
            # request since the first operation will setEstateZone() when it
            # finishes anyway.
            return

        zoneId = self.air.allocateZone()

        def estateLoaded(success):
            if success:
                toon.estate = toon.loadEstateFSM.estate
                self.sendUpdateToAvatarId(senderId, 'setEstateZone', [senderId, zoneId])
            else:
                # Estate loading failed??!
                # I don't know what to do here... Panic! Panic!
                self.notify.warning('Failed to load estate for %d!' % senderId)
                self.air.writeServerEvent('suspicious', senderId, 'Requested to load estate but it failed!')
                toon.requestDelete()

                # And I guess we won't need our zoneId anymore...
                self.air.deallocateZone(zoneId)

            toon.loadEstateFSM = None

        self.acceptOnce(self.air.getAvatarExitEvent(toon.doId), self._unloadEstate, extraArgs=[toon])

        toon.loadEstateFSM = LoadEstateFSM(self, estateLoaded)
        toon.loadEstateFSM.start(accId, zoneId)

    def exitEstate(self):
        senderId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(senderId)

        if not toon:
            self.air.writeServerEvent('suspicious', senderId, 'Sent exitEstate() but not on district!')
            return

        self._unloadEstate(toon)

    def _unloadEstate(self, toon):
        if getattr(toon, 'estate', None):
            self.air.deallocateZone(toon.estate.zoneId)
            toon.estate.destroy()
            toon.estate = None

        if getattr(toon, 'loadEstateFSM', None):
            self.air.deallocateZone(toon.loadEstateFSM.zoneId)
            toon.loadEstateFSM.cancel()
            toon.loadEstateFSM = None

        self.ignore(self.air.getAvatarExitEvent(toon.doId))
