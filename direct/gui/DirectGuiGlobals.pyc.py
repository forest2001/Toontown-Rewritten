# 2013.08.22 22:14:16 Pacific Daylight Time
# Embedded file name: direct.gui.DirectGuiGlobals
__all__ = []
from pandac.PandaModules import *
defaultFont = None
defaultFontFunc = TextNode.getDefaultFont
defaultClickSound = None
defaultRolloverSound = None
defaultDialogGeom = None
drawOrder = 100
panel = None
INITOPT = ['initopt']
LMB = 0
MMB = 1
RMB = 2
NORMAL = 'normal'
DISABLED = 'disabled'
FLAT = PGFrameStyle.TFlat
RAISED = PGFrameStyle.TBevelOut
SUNKEN = PGFrameStyle.TBevelIn
GROOVE = PGFrameStyle.TGroove
RIDGE = PGFrameStyle.TRidge
TEXTUREBORDER = PGFrameStyle.TTextureBorder
FrameStyleDict = {'flat': FLAT,
 'raised': RAISED,
 'sunken': SUNKEN,
 'groove': GROOVE,
 'ridge': RIDGE,
 'texture_border': TEXTUREBORDER}
HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'
VERTICAL_INVERTED = 'vertical_inverted'
DIALOG_NO = 0
DIALOG_OK = DIALOG_YES = DIALOG_RETRY = 1
DIALOG_CANCEL = -1
DESTROY = 'destroy-'
PRINT = 'print-'
ENTER = PGButton.getEnterPrefix()
EXIT = PGButton.getExitPrefix()
WITHIN = PGButton.getWithinPrefix()
WITHOUT = PGButton.getWithoutPrefix()
B1CLICK = PGButton.getClickPrefix() + MouseButton.one().getName() + '-'
B2CLICK = PGButton.getClickPrefix() + MouseButton.two().getName() + '-'
B3CLICK = PGButton.getClickPrefix() + MouseButton.three().getName() + '-'
B1PRESS = PGButton.getPressPrefix() + MouseButton.one().getName() + '-'
B2PRESS = PGButton.getPressPrefix() + MouseButton.two().getName() + '-'
B3PRESS = PGButton.getPressPrefix() + MouseButton.three().getName() + '-'
B1RELEASE = PGButton.getReleasePrefix() + MouseButton.one().getName() + '-'
B2RELEASE = PGButton.getReleasePrefix() + MouseButton.two().getName() + '-'
B3RELEASE = PGButton.getReleasePrefix() + MouseButton.three().getName() + '-'
OVERFLOW = PGEntry.getOverflowPrefix()
ACCEPT = PGEntry.getAcceptPrefix() + KeyboardButton.enter().getName() + '-'
ACCEPTFAILED = PGEntry.getAcceptFailedPrefix() + KeyboardButton.enter().getName() + '-'
TYPE = PGEntry.getTypePrefix()
ERASE = PGEntry.getErasePrefix()
CURSORMOVE = PGEntry.getCursormovePrefix()
ADJUST = PGSliderBar.getAdjustPrefix()
IMAGE_SORT_INDEX = 10
GEOM_SORT_INDEX = 20
TEXT_SORT_INDEX = 30
BACKGROUND_SORT_INDEX = -100
MIDGROUND_SORT_INDEX = 0
FOREGROUND_SORT_INDEX = 100
_OPT_DEFAULT = 0
_OPT_VALUE = 1
_OPT_FUNCTION = 2
BUTTON_READY_STATE = PGButton.SReady
BUTTON_DEPRESSED_STATE = PGButton.SDepressed
BUTTON_ROLLOVER_STATE = PGButton.SRollover
BUTTON_INACTIVE_STATE = PGButton.SInactive

def getDefaultRolloverSound():
    global defaultRolloverSound
    if defaultRolloverSound == None:
        defaultRolloverSound = base.loadSfx('audio/sfx/GUI_rollover.wav')
    return defaultRolloverSound


def setDefaultRolloverSound(newSound):
    global defaultRolloverSound
    defaultRolloverSound = newSound


def getDefaultClickSound():
    global defaultClickSound
    if defaultClickSound == None:
        defaultClickSound = base.loadSfx('audio/sfx/GUI_click.wav')
    return defaultClickSound


def setDefaultClickSound(newSound):
    global defaultClickSound
    defaultClickSound = newSound


def getDefaultFont():
    global defaultFont
    global defaultFontFunc
    if defaultFont == None:
        defaultFont = defaultFontFunc()
    return defaultFont


def setDefaultFont(newFont):
    global defaultFont
    defaultFont = newFont


def setDefaultFontFunc(newFontFunc):
    global defaultFontFunc
    defaultFontFunc = newFontFunc


def getDefaultDialogGeom():
    global defaultDialogGeom
    if defaultDialogGeom == None:
        defaultDialogGeom = loader.loadModel('models/gui/dialog_box_gui', okMissing=True)
    return defaultDialogGeom


def setDefaultDialogGeom(newDialogGeom):
    global defaultDialogGeom
    defaultDialogGeom = newDialogGeom


def getDefaultDrawOrder():
    global drawOrder
    return drawOrder


def setDefaultDrawOrder(newDrawOrder):
    global drawOrder
    drawOrder = newDrawOrder


def getDefaultPanel():
    global panel
    return panel


def setDefaultPanel(newPanel):
    global panel
    panel = newPanel
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\gui\DirectGuiGlobals.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:16 Pacific Daylight Time
