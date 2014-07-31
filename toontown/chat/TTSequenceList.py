from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.showbase import AppRunnerGlobal
from otp.chat.SequenceList import SequenceList
from toontown.toonbase import TTLocalizer

class TTSequenceList(SequenceList, DistributedObject.DistributedObject):

    def __init__(self):
        SequenceList.__init__(self, self.downloadSequences(config.GetString('blacklist-sequence-url', '')))

    def downloadSequences(self, url):
        fs = Ramfile()
        http = HTTPClient.getGlobalPtr()
        self.ch = http.makeChannel(True)
        self.ch.getHeader(DocumentSpec(url))
        doc = self.ch.getDocumentSpec()
        self.ch.getDocument(doc)
        self.ch.downloadToRam(fs)
        return fs.getData()
