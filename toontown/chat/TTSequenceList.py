from pandac.PandaModules import *
from otp.chat.SequenceList import SequenceList

class TTSequenceList(SequenceList):

    def __init__(self):
        sequenceListURL = config.GetString('blacklist-sequence-url', '')
        if sequenceListURL == '':
            self.notify.warning('No Sequence BL URL specified! Continuing with no blacklist.')
            SequenceList.__init__(self, '')
        else:
            SequenceList.__init__(self, self.downloadSequences(sequenceListURL))

    def downloadSequences(self, url):
        fs = Ramfile()
        http = HTTPClient.getGlobalPtr()
        self.ch = http.makeChannel(True)
        self.ch.getHeader(DocumentSpec(url))
        doc = self.ch.getDocumentSpec()
        self.ch.getDocument(doc)
        self.ch.downloadToRam(fs)
        return fs.getData()
