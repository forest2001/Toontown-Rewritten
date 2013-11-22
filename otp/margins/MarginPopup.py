from pandac.PandaModules import *

class MarginPopup:
    def __init__(self):
        self.__manager = None
        self.__visible = False

        # The margin management system uses these:
        self._assignedCell = None
        self._lastCell = None

    def setVisible(self, visibility):
        visibility = bool(visibility)
        if self.__visible == visibility: return

        self.__visible = visibility

        if self.__manager is not None:
            if visibility:
                self.__manager.addVisiblePopup(self)
            else:
                self.__manager.removeVisiblePopup(self)

    def getPriority(self):
        return 0

    def manage(self, manager):
        self.unmanage(self.__manager)
        self.__manager = manager

        if self.__visible:
            manager.addVisiblePopup(self)

    def unmanage(self, manager):
        if self.__manager is not None:
            if self.__visible:
                self.__manager.removeVisiblePopup(self)
            self.__manager = None
