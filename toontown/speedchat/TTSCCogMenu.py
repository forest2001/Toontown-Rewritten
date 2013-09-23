from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal

class TTSCCogMenu(SCMenu):
    __module__ = __name__

    def __init__(self, indices):
        SCMenu.__init__(self)
        for index in indices:
            term = SCStaticTextTerminal(index)
            self.append(term)

    def destroy(self):
        SCMenu.destroy(self)
