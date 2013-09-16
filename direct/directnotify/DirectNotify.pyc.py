# 2013.08.22 22:13:49 Pacific Daylight Time
# Embedded file name: direct.directnotify.DirectNotify
import Notifier
import Logger

class DirectNotify():
    __module__ = __name__

    def __init__(self):
        self.__categories = {}
        self.logger = Logger.Logger()
        self.streamWriter = None
        return

    def __str__(self):
        return 'DirectNotify categories: %s' % self.__categories

    def getCategories(self):
        return self.__categories.keys()

    def getCategory(self, categoryName):
        return self.__categories.get(categoryName, None)

    def newCategory(self, categoryName, logger = None):
        if categoryName not in self.__categories:
            self.__categories[categoryName] = Notifier.Notifier(categoryName, logger)
            self.setDconfigLevel(categoryName)
        return self.getCategory(categoryName)

    def setDconfigLevel(self, categoryName):
        try:
            config
        except:
            return 0

        dconfigParam = 'notify-level-' + categoryName
        level = config.GetString(dconfigParam, '')
        if not level:
            level = config.GetString('default-directnotify-level', 'info')
        if not level:
            level = 'error'
        category = self.getCategory(categoryName)
        if level == 'error':
            category.setWarning(0)
            category.setInfo(0)
            category.setDebug(0)
        elif level == 'warning':
            category.setWarning(1)
            category.setInfo(0)
            category.setDebug(0)
        elif level == 'info':
            category.setWarning(1)
            category.setInfo(1)
            category.setDebug(0)
        elif level == 'debug':
            category.setWarning(1)
            category.setInfo(1)
            category.setDebug(1)
        else:
            print 'DirectNotify: unknown notify level: ' + str(level) + ' for category: ' + str(categoryName)

    def setDconfigLevels(self):
        for categoryName in self.getCategories():
            self.setDconfigLevel(categoryName)

    def setVerbose(self):
        for categoryName in self.getCategories():
            category = self.getCategory(categoryName)
            category.setWarning(1)
            category.setInfo(1)
            category.setDebug(1)

    def popupControls(self, tl = None):
        from direct.tkpanels import NotifyPanel
        NotifyPanel.NotifyPanel(self, tl)

    def giveNotify(self, cls):
        cls.notify = self.newCategory(cls.__name__)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\directnotify\DirectNotify.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:49 Pacific Daylight Time
