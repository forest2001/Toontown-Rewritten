# 2013.08.22 22:22:54 Pacific Daylight Time
# Embedded file name: toontown.minigame.PhotoGameBase
import PhotoGameGlobals
import random

class PhotoGameBase():
    __module__ = __name__

    def __init__(self):
        pass

    def load(self):
        self.data = PhotoGameGlobals.AREA_DATA[self.getSafezoneId()]

    def generateAssignmentTemplates(self, numAssignments):
        self.data = PhotoGameGlobals.AREA_DATA[self.getSafezoneId()]
        random.seed(self.doId)
        assignmentTemplates = []
        numPathes = len(self.data['PATHS'])
        if numPathes == 0:
            return assignmentTemplates
        while len(assignmentTemplates) < numAssignments:
            subjectIndex = random.choice(range(numPathes))
            pose = (None, None)
            while pose[0] == None:
                animSetIndex = self.data['PATHANIMREL'][subjectIndex]
                pose = random.choice(self.data['ANIMATIONS'][animSetIndex] + self.data['MOVEMODES'][animSetIndex])

            newTemplate = (subjectIndex, pose[0])
            if newTemplate not in assignmentTemplates:
                assignmentTemplates.append((subjectIndex, pose[0]))

        self.notify.debug('assignment templates')
        self.notify.debug(str(assignmentTemplates))
        for template in assignmentTemplates:
            self.notify.debug(str(template))

        return assignmentTemplates
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\minigame\PhotoGameBase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:22:54 Pacific Daylight Time
