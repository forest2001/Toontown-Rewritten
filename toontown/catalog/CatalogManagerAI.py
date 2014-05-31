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
        monthlyCatalog = self.catalogGenerator.generateMonthlyCatalog(av, time.time() / 60)
        newWeek = (av.catalogScheduleCurrentWeek + 1) % ToontownGlobals.CatalogNumWeeks
        weeklyCatalog = self.catalogGenerator.generateWeeklyCatalog(av, newWeek, monthlyCatalog)
        backCatalog = self.catalogGenerator.generateBackCatalog(av, newWeek, av.catalogScheduleCurrentWeek, monthlyCatalog)
        av.b_setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)
        av.b_setCatalogSchedule(newWeek, int((time.time() + 604800)/60))
        av.b_setCatalogNotify(ToontownGlobals.NewItems, av.mailboxNotify)
    
    def isItemReleased(self, accessory):
        return 1

