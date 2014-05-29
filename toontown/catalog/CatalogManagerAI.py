from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from CatalogGenerator import CatalogGenerator
from toontown.toonbase import ToontownGlobals
import time

class CatalogManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.catalogGenerator = CatalogGenerator()

    def startCatalog(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            self.deliverCatalogFor(av)    
    
    def deliverCatalogFor(self, av):
        monthlyCatalog = self.catalogGenerator.generateMonthlyCatalog(av, av.catalogScheduleCurrentWeek)
        weeklyCatalog = self.catalogGenerator.generateWeeklyCatalog(av, av.catalogScheduleCurrentWeek, monthlyCatalog)
        backCatalog = self.catalogGenerator.generateBackCatalog(av, av.catalogScheduleCurrentWeek, av.catalogScheduleCurrentWeek - 1, monthlyCatalog)
        av.b_setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)
        av.b_setCatalogSchedule((av.catalogScheduleCurrentWeek + 1) % ToontownGlobals.CatalogNumWeeks, time.time() + 604800)
        av.b_setCatalogNotify(ToontownGlobals.NewItems, av.mailboxNotify)
    
    def isItemReleased(self, accessory):
        return 1

