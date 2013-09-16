# 2013.08.22 22:15:52 Pacific Daylight Time
# Embedded file name: pandac.libdirectModules
from extension_native_helpers import *
Dtool_PreloadDLL('libdirect')
from libdirect import *
from extension_native_helpers import *
try:
    Dtool_PreloadDLL('libp3direct')
    from libp3direct import *
except:
    Dtool_PreloadDLL('libdirect')
    from libdirect import *

from direct.directnotify.DirectNotifyGlobal import directNotify
notify = directNotify.newCategory('Interval')
Dtool_ObjectToDict(CInterval, 'notify', notify)
del notify

def setT(self, t):
    self.setT_Old(t)
    self.privPostEvent()


Dtool_ObjectToDict(CInterval, 'setT_Old', CInterval.setT)
Dtool_funcToMethod(setT, CInterval)
del setT

def play(self, t0 = 0.0, duration = None, scale = 1.0):
    self.notify.error('using deprecated CInterval.play() interface')
    if duration:
        self.start(t0, t0 + duration, scale)
    else:
        self.start(t0, -1, scale)


Dtool_funcToMethod(play, CInterval)
del play

def stop(self):
    self.notify.error('using deprecated CInterval.stop() interface')
    self.finish()


Dtool_funcToMethod(stop, CInterval)
del stop

def setFinalT(self):
    self.notify.error('using deprecated CInterval.setFinalT() interface')
    self.finish()


Dtool_funcToMethod(setFinalT, CInterval)
del setFinalT

def privPostEvent(self):
    t = self.getT()
    if hasattr(self, 'setTHooks'):
        for func in self.setTHooks:
            func(t)


Dtool_funcToMethod(privPostEvent, CInterval)
del privPostEvent

def popupControls(self, tl = None):
    from direct.showbase.TkGlobal import Toplevel, Frame, Button, LEFT, X, Pmw
    import math
    from direct.tkwidgets import EntryScale
    if tl == None:
        tl = Toplevel()
        tl.title('Interval Controls')
    outerFrame = Frame(tl)

    def entryScaleCommand(t, s = self):
        s.setT(t)
        s.pause()

    self.es = es = EntryScale.EntryScale(outerFrame, text=self.getName(), min=0, max=math.floor(self.getDuration() * 100) / 100, command=entryScaleCommand)
    es.set(self.getT(), fCommand=0)
    es.pack(expand=1, fill=X)
    bf = Frame(outerFrame)

    def toStart(s = self, es = es):
        s.setT(0.0)
        s.pause()

    def toEnd(s = self):
        s.setT(s.getDuration())
        s.pause()

    jumpToStart = Button(bf, text='<<', command=toStart)

    def doPlay(s = self, es = es):
        s.resume(es.get())

    stop = Button(bf, text='Stop', command=lambda s = self: s.pause())
    play = Button(bf, text='Play', command=doPlay)
    jumpToEnd = Button(bf, text='>>', command=toEnd)
    jumpToStart.pack(side=LEFT, expand=1, fill=X)
    play.pack(side=LEFT, expand=1, fill=X)
    stop.pack(side=LEFT, expand=1, fill=X)
    jumpToEnd.pack(side=LEFT, expand=1, fill=X)
    bf.pack(expand=1, fill=X)
    outerFrame.pack(expand=1, fill=X)

    def update(t, es = es):
        es.set(t, fCommand=0)

    if not hasattr(self, 'setTHooks'):
        self.setTHooks = []
    self.setTHooks.append(update)
    self.setWantsTCallback(1)

    def onDestroy(e, s = self, u = update):
        if u in s.setTHooks:
            s.setTHooks.remove(u)

    tl.bind('<Destroy>', onDestroy)
    return


Dtool_funcToMethod(popupControls, CInterval)
del popupControls
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pandac\libdirectModules.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:52 Pacific Daylight Time
