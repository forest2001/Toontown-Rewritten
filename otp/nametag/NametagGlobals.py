camera = None
def setCamera(cam):
    global camera
    camera = cam

arrowModel = None
def setArrowModel(am):
    global arrowModel
    arrowModel = am

nametagCardModel = None
nametagCardDimensions = None
def setNametagCard(model, dimensions):
    global nametagCardModel, nametagCardDimensions
    nametagCardModel = model
    nametagCardDimensions = dimensions

mouseWatcher = None
def setMouseWatcher(mw):
    global mouseWatcher
    mouseWatcher = mw

speechBalloon3d = None
def setSpeechBalloon3d(sb3d):
    global speechBalloon3d
    speechBalloon3d = sb3d

thoughtBalloon3d = None
def setThoughtBalloon3d(tb3d):
    global thoughtBalloon3d
    thoughtBalloon3d = tb3d

speechBalloon2d = None
def setSpeechBalloon2d(sb2d):
    global speechBalloon2d
    speechBalloon2d = sb2d

thoughtBalloon2d = None
def setThoughtBalloon2d(tb2d):
    global thoughtBalloon2d
    thoughtBalloon2d = tb2d

pageButtons = {}
def setPageButton(state, model):
    pageButtons[state] = model

quitButtons = {}
def setQuitButton(state, model):
    quitButtons[state] = model

rolloverSound = None
def setRolloverSound(ros):
    global rolloverSound
    rolloverSound = ros

clickSound = None
def setClickSound(cs):
    global clickSound
    clickSound = cs

toon = None
def setToon(t):
    global toon
    toon = t
