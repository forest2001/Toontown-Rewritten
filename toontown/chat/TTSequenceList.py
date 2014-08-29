from pandac.PandaModules import *
from otp.chat.SequenceList import SequenceList
from direct.directnotify import DirectNotifyGlobal

class TTSequenceList(SequenceList):

    def __init__(self):
        self.notify = DirectNotifyGlobal.directNotify.newCategory('TTSequenceList')
        sequenceListURL = config.GetString('blacklist-sequence-url', '')
        if sequenceListURL == '':
            self.notify.warning('No Sequence BL URL specified! Continuing with local sequence.')
            SequenceList.__init__(self, self.loadSquencesLocally())
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
        return fs.getData().split('\r\n')

    def loadSquencesLocally(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('tsequence.dat')
        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('/server'))
        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            self.notify.warning("Couldn't find blacklist sequence data file!")
            return
        data = vfs.readFile(filename, True)
        return data.split('\n')
