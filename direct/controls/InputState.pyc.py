# 2013.08.22 22:13:47 Pacific Daylight Time
# Embedded file name: direct.controls.InputState
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject

class InputStateToken():
    __module__ = __name__
    _SerialGen = SerialNumGen()
    Inval = 'invalidatedToken'

    def __init__(self, inputState):
        self._id = InputStateToken._SerialGen.next()
        self._hash = self._id
        self._inputState = inputState

    def release(self):
        pass

    def isValid(self):
        return self._id != InputStateToken.Inval

    def invalidate(self):
        self._id = InputStateToken.Inval

    def __hash__(self):
        return self._hash


class InputStateWatchToken(InputStateToken, DirectObject.DirectObject):
    __module__ = __name__

    def release(self):
        self._inputState._ignore(self)
        self.ignoreAll()


class InputStateForceToken(InputStateToken):
    __module__ = __name__

    def release(self):
        self._inputState._unforce(self)


class InputStateTokenGroup():
    __module__ = __name__

    def __init__(self):
        self._tokens = []

    def addToken(self, token):
        self._tokens.append(token)

    def release(self):
        for token in self._tokens:
            token.release()

        self._tokens = []


class InputState(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('InputState')
    WASD = 'WASD'
    QE = 'QE'
    ArrowKeys = 'ArrowKeys'
    Keyboard = 'Keyboard'
    Mouse = 'Mouse'

    def __init__(self):
        self._state = {}
        self._forcingOn = {}
        self._forcingOff = {}
        self._token2inputSource = {}
        self._token2forceInfo = {}
        self._watching = {}

    def delete(self):
        del self._watching
        del self._token2forceInfo
        del self._token2inputSource
        del self._forcingOff
        del self._forcingOn
        del self._state
        self.ignoreAll()

    def isSet(self, name, inputSource = None):
        if name in self._forcingOn:
            return True
        elif name in self._forcingOff:
            return False
        if inputSource:
            s = self._state.get(name)
            if s:
                return inputSource in s
            else:
                return False
        else:
            return name in self._state

    def getEventName(self, name):
        return 'InputState-%s' % (name,)

    def set(self, name, isActive, inputSource = None):
        if inputSource is None:
            inputSource = 'anonymous'
        if isActive:
            self._state.setdefault(name, set())
            self._state[name].add(inputSource)
        elif name in self._state:
            self._state[name].discard(inputSource)
            if len(self._state[name]) == 0:
                del self._state[name]
        messenger.send(self.getEventName(name), [self.isSet(name)])
        return

    def releaseInputs(self, name):
        del self._state[name]

    def watch(self, name, eventOn, eventOff, startState = False, inputSource = None):
        if inputSource is None:
            inputSource = "eventPair('%s','%s')" % (eventOn, eventOff)
        self.set(name, startState, inputSource)
        token = InputStateWatchToken(self)
        token.accept(eventOn, self.set, [name, True, inputSource])
        token.accept(eventOff, self.set, [name, False, inputSource])
        self._token2inputSource[token] = inputSource
        self._watching.setdefault(inputSource, {})
        self._watching[inputSource][token] = (name, eventOn, eventOff)
        return token

    def watchWithModifiers(self, name, event, startState = False, inputSource = None):
        patterns = ('%s', 'control-%s', 'shift-control-%s', 'alt-%s', 'control-alt-%s', 'shift-%s', 'shift-alt-%s')
        tGroup = InputStateTokenGroup()
        for pattern in patterns:
            tGroup.addToken(self.watch(name, pattern % event, '%s-up' % event, startState=startState, inputSource=inputSource))

        return tGroup

    def _ignore(self, token):
        inputSource = self._token2inputSource.pop(token)
        name, eventOn, eventOff = self._watching[inputSource].pop(token)
        token.invalidate()
        DirectObject.DirectObject.ignore(self, eventOn)
        DirectObject.DirectObject.ignore(self, eventOff)
        if len(self._watching[inputSource]) == 0:
            del self._watching[inputSource]

    def force(self, name, value, inputSource):
        token = InputStateForceToken(self)
        self._token2forceInfo[token] = (name, inputSource)
        if value:
            if name in self._forcingOff:
                self.notify.error("%s is trying to force '%s' to ON, but '%s' is already being forced OFF by %s" % (inputSource,
                 name,
                 name,
                 self._forcingOff[name]))
            self._forcingOn.setdefault(name, set())
            self._forcingOn[name].add(inputSource)
        else:
            if name in self._forcingOn:
                self.notify.error("%s is trying to force '%s' to OFF, but '%s' is already being forced ON by %s" % (inputSource,
                 name,
                 name,
                 self._forcingOn[name]))
            self._forcingOff.setdefault(name, set())
            self._forcingOff[name].add(inputSource)
        return token

    def _unforce(self, token):
        name, inputSource = self._token2forceInfo[token]
        token.invalidate()
        if name in self._forcingOn:
            self._forcingOn[name].discard(inputSource)
            if len(self._forcingOn[name]) == 0:
                del self._forcingOn[name]
        if name in self._forcingOff:
            self._forcingOff[name].discard(inputSource)
            if len(self._forcingOff[name]) == 0:
                del self._forcingOff[name]

    def debugPrint(self, message):
        return self.notify.debug('%s (%s) %s' % (id(self), len(self._state), message))
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\controls\InputState.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:48 Pacific Daylight Time
