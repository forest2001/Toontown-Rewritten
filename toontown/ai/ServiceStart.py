from pandac.PandaModules import *

# Dev stuff that should probably be removed before deployment:
loadPrcFile('config/dev.prc')

class game:
    name = 'toontown'
    process = 'server'
__builtins__.game = game

from otp.ai.AIBaseGlobal import *

from toontown.ai.ToontownAIRepository import ToontownAIRepository
simbase.air = ToontownAIRepository(401000000, 10000, 'Devhaven')
simbase.air.connect('127.0.0.1')

run()
