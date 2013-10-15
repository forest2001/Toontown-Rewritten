from pandac.PandaModules import *
# Dev stuff that should probably be removed before deployment:
from direct import distributed
distributed.__path__ = ['/home/cfsworks/Desktop/incremental/direct/src/distributed']

loadPrcFile('config/dev.prc')

class game:
    name = 'uberDog'
    process = 'server'
__builtins__.game = game

from otp.ai.AIBaseGlobal import *

from toontown.uberdog.ToontownUberRepository import ToontownUberRepository
simbase.air = ToontownUberRepository(400000000, 10000)
simbase.air.connect('127.0.0.1')

run()
