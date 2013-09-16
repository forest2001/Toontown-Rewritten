# 2013.08.22 22:14:05 Pacific Daylight Time
# Embedded file name: direct.distributed.DistributedObjectGlobalUD
from DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify
import sys

class DistributedObjectGlobalUD(DistributedObjectUD):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedObjectGlobalUD')
    doNotDeallocateChannel = 1
    isGlobalDistObj = 1

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.ExecNamespace = {'self': self}

    def announceGenerate(self):
        self.air.registerForChannel(self.doId)
        DistributedObjectUD.announceGenerate(self)

    def delete(self):
        self.air.unregisterForChannel(self.doId)
        DistributedObjectUD.delete(self)

    def execCommand(self, command, mwMgrId, avId, zoneId):
        text = str(self.__execMessage(command))[:config.GetInt('ai-debug-length', 300)]
        dclass = uber.air.dclassesByName.get('PiratesMagicWordManagerAI')
        dg = dclass.aiFormatUpdate('setMagicWordResponse', mwMgrId, (1 << 32) + avId, uber.air.ourChannel, [text])
        uber.air.send(dg)

    def __execMessage(self, message):
        if not self.ExecNamespace:
            exec 'from pandac.PandaModules import *' in globals(), self.ExecNamespace
        try:
            if not isClient():
                print 'EXECWARNING DistributedObjectGlobalUD eval: %s' % message
                printStack()
            return str(eval(message, globals(), self.ExecNamespace))
        except SyntaxError:
            try:
                if not isClient():
                    print 'EXECWARNING DistributedObjectGlobalUD: %s' % message
                    printStack()
                exec message in globals(), self.ExecNamespace
                return 'ok'
            except:
                exception = sys.exc_info()[0]
                extraInfo = sys.exc_info()[1]
                if extraInfo:
                    return str(extraInfo)
                else:
                    return str(exception)

        except:
            exception = sys.exc_info()[0]
            extraInfo = sys.exc_info()[1]
            if extraInfo:
                return str(extraInfo)
            else:
                return str(exception)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\distributed\DistributedObjectGlobalUD.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:05 Pacific Daylight Time
