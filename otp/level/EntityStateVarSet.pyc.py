# 2013.08.22 22:15:31 Pacific Daylight Time
# Embedded file name: otp.level.EntityStateVarSet
from direct.fsm.StatePush import StateVar
from direct.showbase.PythonUtil import getSetterName
from otp.level.Entity import Entity

class EntityStateVarSet(Entity):
    __module__ = __name__

    def __init__(self, entType):
        self._entType = entType
        self._attribNames = []
        for attrib in self._entType.attribs:
            name, defaultVal, type = attrib
            self._addAttrib(name, defaultVal, type)

    def initializeEntity(self, level, entId):
        stateVars = {}
        for attribName in self._attribNames:
            stateVars[attribName] = getattr(self, attribName)

        Entity.initializeEntity(self, level, entId)
        for attribName in self._attribNames:
            stateVars[attribName].set(getattr(self, attribName))

        for attribName in self._attribNames:
            setattr(self, attribName, stateVars[attribName])

    def _getAttributeNames(self):
        return self._attribNames[:]

    def _setter(self, name, value):
        getattr(self, name).set(value)

    def _addAttrib(self, name, defaultVal, type):
        setattr(self, name, StateVar(defaultVal))
        setattr(self, getSetterName(name), Functor(self._setter, name))
        self._attribNames.append(name)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\level\EntityStateVarSet.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:31 Pacific Daylight Time
