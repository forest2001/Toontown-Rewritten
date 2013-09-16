# 2013.08.22 22:25:11 Pacific Daylight Time
# Embedded file name: toontown.speedchat.TTSCToontaskMenu
from otp.speedchat.SCMenu import SCMenu
from TTSCToontaskTerminal import TTSCToontaskTerminal
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from toontown.quest import Quests

class TTSCToontaskMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('questsChanged', self.__tasksChanged)
        self.__tasksChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __tasksChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        phrases = []

        def addTerminal(terminal, self = self, phrases = phrases):
            displayText = terminal.getDisplayText()
            if displayText not in phrases:
                self.append(terminal)
                phrases.append(displayText)

        for task in lt.quests:
            taskId, fromNpcId, toNpcId, rewardId, toonProgress = task
            q = Quests.getQuest(taskId)
            if q is None:
                continue
            msgs = q.getSCStrings(toNpcId, toonProgress)
            if type(msgs) != type([]):
                msgs = [msgs]
            for i in xrange(len(msgs)):
                addTerminal(TTSCToontaskTerminal(msgs[i], taskId, toNpcId, toonProgress, i))

        needToontask = 1
        if hasattr(lt, 'questCarryLimit'):
            needToontask = len(lt.quests) != lt.questCarryLimit
        if needToontask:
            addTerminal(SCStaticTextTerminal(1299))
        return
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\speedchat\TTSCToontaskMenu.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:25:11 Pacific Daylight Time
