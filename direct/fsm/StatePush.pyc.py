# 2013.08.22 22:14:12 Pacific Daylight Time
# Embedded file name: direct.fsm.StatePush
__all__ = ['StateVar',
 'FunctionCall',
 'EnterExit',
 'Pulse',
 'EventPulse',
 'EventArgument']
from direct.showbase.DirectObject import DirectObject
import types

class PushesStateChanges():
    __module__ = __name__

    def __init__(self, value):
        self._value = value
        self._subscribers = set()

    def destroy(self):
        if len(self._subscribers) != 0:
            raise '%s object still has subscribers in destroy(): %s' % (self.__class__.__name__, self._subscribers)
        del self._subscribers
        del self._value

    def getState(self):
        return self._value

    def pushCurrentState(self):
        self._handleStateChange()
        return self

    def _addSubscription(self, subscriber):
        self._subscribers.add(subscriber)
        subscriber._recvStatePush(self)

    def _removeSubscription(self, subscriber):
        self._subscribers.remove(subscriber)

    def _handlePotentialStateChange(self, value):
        oldValue = self._value
        self._value = value
        if oldValue != value:
            self._handleStateChange()

    def _handleStateChange(self):
        for subscriber in self._subscribers:
            subscriber._recvStatePush(self)


class ReceivesStateChanges():
    __module__ = __name__

    def __init__(self, source):
        self._source = None
        self._initSource = source
        return

    def _finishInit(self):
        self._subscribeTo(self._initSource)
        del self._initSource

    def destroy(self):
        self._unsubscribe()
        del self._source

    def _subscribeTo(self, source):
        self._unsubscribe()
        self._source = source
        if self._source:
            self._source._addSubscription(self)

    def _unsubscribe(self):
        if self._source:
            self._source._removeSubscription(self)
            self._source = None
        return

    def _recvStatePush(self, source):
        pass


class StateVar(PushesStateChanges):
    __module__ = __name__

    def set(self, value):
        PushesStateChanges._handlePotentialStateChange(self, value)

    def get(self):
        return PushesStateChanges.getState(self)


class StateChangeNode(PushesStateChanges, ReceivesStateChanges):
    __module__ = __name__

    def __init__(self, source):
        ReceivesStateChanges.__init__(self, source)
        PushesStateChanges.__init__(self, source.getState())
        ReceivesStateChanges._finishInit(self)

    def destroy(self):
        PushesStateChanges.destroy(self)
        ReceivesStateChanges.destroy(self)

    def _recvStatePush(self, source):
        self._handlePotentialStateChange(source._value)


class ReceivesMultipleStateChanges():
    __module__ = __name__

    def __init__(self):
        self._key2source = {}
        self._source2key = {}

    def destroy(self):
        keys = self._key2source.keys()
        for key in keys:
            self._unsubscribe(key)

        del self._key2source
        del self._source2key

    def _subscribeTo(self, source, key):
        self._unsubscribe(key)
        self._key2source[key] = source
        self._source2key[source] = key
        source._addSubscription(self)

    def _unsubscribe(self, key):
        if key in self._key2source:
            source = self._key2source[key]
            source._removeSubscription(self)
            del self._key2source[key]
            del self._source2key[source]

    def _recvStatePush(self, source):
        self._recvMultiStatePush(self._source2key[source], source)

    def _recvMultiStatePush(self, key, source):
        pass


class FunctionCall(ReceivesMultipleStateChanges, PushesStateChanges):
    __module__ = __name__

    def __init__(self, func, *args, **kArgs):
        self._initialized = False
        ReceivesMultipleStateChanges.__init__(self)
        PushesStateChanges.__init__(self, None)
        self._func = func
        self._args = args
        self._kArgs = kArgs
        self._bakedArgs = []
        self._bakedKargs = {}
        for i in xrange(len(self._args)):
            key = i
            arg = self._args[i]
            if isinstance(arg, PushesStateChanges):
                self._bakedArgs.append(arg.getState())
                self._subscribeTo(arg, key)
            else:
                self._bakedArgs.append(self._args[i])

        for key, arg in self._kArgs.iteritems():
            if isinstance(arg, PushesStateChanges):
                self._bakedKargs[key] = arg.getState()
                self._subscribeTo(arg, key)
            else:
                self._bakedKargs[key] = arg

        self._initialized = True
        return

    def destroy(self):
        ReceivesMultipleStateChanges.destroy(self)
        PushesStateChanges.destroy(self)
        del self._func
        del self._args
        del self._kArgs
        del self._bakedArgs
        del self._bakedKargs

    def getState(self):
        return (tuple(self._bakedArgs), dict(self._bakedKargs))

    def _recvMultiStatePush(self, key, source):
        if isinstance(key, types.StringType):
            self._bakedKargs[key] = source.getState()
        else:
            self._bakedArgs[key] = source.getState()
        self._handlePotentialStateChange(self.getState())

    def _handleStateChange(self):
        if self._initialized:
            self._func(*self._bakedArgs, **self._bakedKargs)
            PushesStateChanges._handleStateChange(self)


class EnterExit(StateChangeNode):
    __module__ = __name__

    def __init__(self, source, enterFunc, exitFunc):
        self._enterFunc = enterFunc
        self._exitFunc = exitFunc
        StateChangeNode.__init__(self, source)

    def destroy(self):
        StateChangeNode.destroy(self)
        del self._exitFunc
        del self._enterFunc

    def _handlePotentialStateChange(self, value):
        StateChangeNode._handlePotentialStateChange(self, bool(value))

    def _handleStateChange(self):
        if self._value:
            self._enterFunc()
        else:
            self._exitFunc()
        StateChangeNode._handleStateChange(self)


class Pulse(PushesStateChanges):
    __module__ = __name__

    def __init__(self):
        PushesStateChanges.__init__(self, False)

    def sendPulse(self):
        self._handlePotentialStateChange(True)
        self._handlePotentialStateChange(False)


class EventPulse(Pulse, DirectObject):
    __module__ = __name__

    def __init__(self, event):
        Pulse.__init__(self)
        self.accept(event, self.sendPulse)

    def destroy(self):
        self.ignoreAll()
        Pulse.destroy(self)


class EventArgument(PushesStateChanges, DirectObject):
    __module__ = __name__

    def __init__(self, event, index = 0):
        PushesStateChanges.__init__(self, None)
        self._index = index
        self.accept(event, self._handleEvent)
        return

    def destroy(self):
        self.ignoreAll()
        del self._index
        PushesStateChanges.destroy(self)

    def _handleEvent(self, *args):
        self._handlePotentialStateChange(args[self._index])


class AttrSetter(StateChangeNode):
    __module__ = __name__

    def __init__(self, source, object, attrName):
        self._object = object
        self._attrName = attrName
        StateChangeNode.__init__(self, source)
        self._handleStateChange()

    def _handleStateChange(self):
        setattr(self._object, self._attrName, self._value)
        StateChangeNode._handleStateChange(self)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\fsm\StatePush.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:12 Pacific Daylight Time
