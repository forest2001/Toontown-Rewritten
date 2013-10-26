from Nametag import *
from otp.margins.MarginPopup import *
from pandac.PandaModules import *

class Nametag2d(Nametag, MarginPopup):
    def __init__(self):
        Nametag.__init__(self)
        MarginPopup.__init__(self)
