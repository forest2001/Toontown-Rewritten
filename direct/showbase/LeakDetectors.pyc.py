# 2013.08.22 22:14:36 Pacific Daylight Time
# Embedded file name: direct.showbase.LeakDetectors
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Job import Job
import __builtin__, gc

class LeakDetector():
    __module__ = __name__

    def __init__(self):
        if not hasattr(__builtin__, 'leakDetectors'):
            __builtin__.leakDetectors = {}
        self._leakDetectorsKey = self.getLeakDetectorKey()
        if __dev__:
            pass
        leakDetectors[self._leakDetectorsKey] = self

    def destroy(self):
        del leakDetectors[self._leakDetectorsKey]

    def getLeakDetectorKey(self):
        return '%s-%s' % (self.__class__.__name__, id(self))


class ObjectTypeLeakDetector(LeakDetector):
    __module__ = __name__

    def __init__(self, otld, objType, generation):
        self._otld = otld
        self._objType = objType
        self._generation = generation
        LeakDetector.__init__(self)

    def destroy(self):
        self._otld = None
        LeakDetector.destroy(self)
        return

    def getLeakDetectorKey(self):
        return '%s-%s' % (self._objType, self.__class__.__name__)

    def __len__(self):
        num = self._otld._getNumObjsOfType(self._objType, self._generation)
        self._generation = self._otld._getGeneration()
        return num


class ObjectTypesLeakDetector(LeakDetector):
    __module__ = __name__

    def __init__(self):
        LeakDetector.__init__(self)
        self._type2ld = {}
        self._type2count = {}
        self._generation = 0
        self._thisLdGen = 0

    def destroy(self):
        for ld in self._type2ld.itervalues():
            ld.destroy()

        LeakDetector.destroy(self)

    def _recalc(self):
        objs = gc.get_objects()
        self._type2count = {}
        for obj in objs:
            objType = safeTypeName(obj)
            if objType not in self._type2ld:
                self._type2ld[objType] = ObjectTypeLeakDetector(self, objType, self._generation)
            self._type2count.setdefault(objType, 0)
            self._type2count[objType] += 1

        self._generation += 1

    def _getGeneration(self):
        return self._generation

    def _getNumObjsOfType(self, objType, otherGen):
        if self._generation == otherGen:
            self._recalc()
        return self._type2count.get(objType, 0)

    def __len__(self):
        if self._generation == self._thisLdGen:
            self._recalc()
        self._thisLdGen = self._generation
        return len(self._type2count)


class GarbageLeakDetector(LeakDetector):
    __module__ = __name__

    def __len__(self):
        oldFlags = gc.get_debug()
        gc.set_debug(0)
        gc.collect()
        numGarbage = len(gc.garbage)
        del gc.garbage[:]
        gc.set_debug(oldFlags)
        return numGarbage


class SceneGraphLeakDetector(LeakDetector):
    __module__ = __name__

    def __init__(self, render):
        LeakDetector.__init__(self)
        self._render = render
        if config.GetBool('leak-scene-graph', 0):
            self._leakTaskName = 'leakNodes-%s' % serialNum()
            self._leakNode()

    def destroy(self):
        if hasattr(self, '_leakTaskName'):
            taskMgr.remove(self._leakTaskName)
        del self._render
        LeakDetector.destroy(self)

    def __len__(self):
        try:
            return self._render.countNumDescendants()
        except:
            return self._render.getNumDescendants()

    def __repr__(self):
        return 'SceneGraphLeakDetector(%s)' % self._render

    def _leakNode(self, task = None):
        self._render.attachNewNode('leakNode-%s' % serialNum())
        taskMgr.doMethodLater(10, self._leakNode, self._leakTaskName)


class CppMemoryUsage(LeakDetector):
    __module__ = __name__

    def __len__(self):
        haveMemoryUsage = True
        try:
            MemoryUsage
        except:
            haveMemoryUsage = False

        if haveMemoryUsage:
            return int(MemoryUsage.getCurrentCppSize())
        else:
            return 0


class TaskLeakDetectorBase():
    __module__ = __name__

    def _getTaskNamePattern(self, taskName):
        for i in xrange(10):
            taskName = taskName.replace('%s' % i, '')

        return taskName


class _TaskNamePatternLeakDetector(LeakDetector, TaskLeakDetectorBase):
    __module__ = __name__

    def __init__(self, taskNamePattern):
        self._taskNamePattern = taskNamePattern
        LeakDetector.__init__(self)

    def __len__(self):
        numTasks = 0
        for task in taskMgr.getTasks():
            if self._getTaskNamePattern(task.name) == self._taskNamePattern:
                numTasks += 1

        for task in taskMgr.getDoLaters():
            if self._getTaskNamePattern(task.name) == self._taskNamePattern:
                numTasks += 1

        return numTasks

    def getLeakDetectorKey(self):
        return '%s-%s' % (self._taskNamePattern, self.__class__.__name__)


class TaskLeakDetector(LeakDetector, TaskLeakDetectorBase):
    __module__ = __name__

    def __init__(self):
        LeakDetector.__init__(self)
        self._taskName2collector = {}

    def destroy(self):
        for taskName, collector in self._taskName2collector.iteritems():
            collector.destroy()

        del self._taskName2collector
        LeakDetector.destroy(self)

    def _processTaskName(self, taskName):
        namePattern = self._getTaskNamePattern(taskName)
        if namePattern not in self._taskName2collector:
            self._taskName2collector[namePattern] = _TaskNamePatternLeakDetector(namePattern)

    def __len__(self):
        self._taskName2collector = {}
        for task in taskMgr.getTasks():
            self._processTaskName(task.name)

        for task in taskMgr.getDoLaters():
            self._processTaskName(task.name)

        return len(self._taskName2collector)


class MessageLeakDetectorBase():
    __module__ = __name__

    def _getMessageNamePattern(self, msgName):
        for i in xrange(10):
            msgName = msgName.replace('%s' % i, '')

        return msgName


class _MessageTypeLeakDetector(LeakDetector, MessageLeakDetectorBase):
    __module__ = __name__

    def __init__(self, msgNamePattern):
        self._msgNamePattern = msgNamePattern
        self._msgNames = set()
        LeakDetector.__init__(self)

    def addMsgName(self, msgName):
        self._msgNames.add(msgName)

    def __len__(self):
        toRemove = set()
        num = 0
        for msgName in self._msgNames:
            n = messenger._getNumListeners(msgName)
            if n == 0:
                toRemove.add(msgName)
            else:
                num += n

        self._msgNames.difference_update(toRemove)
        return num

    def getLeakDetectorKey(self):
        return '%s-%s' % (self._msgNamePattern, self.__class__.__name__)


class _MessageTypeLeakDetectorCreator(Job):
    __module__ = __name__

    def __init__(self, creator):
        Job.__init__(self, uniqueName(typeName(self)))
        self._creator = creator

    def destroy(self):
        self._creator = None
        Job.destroy(self)
        return

    def finished(self):
        Job.finished(self)

    def run--- This code section failed: ---

0	SETUP_LOOP        '111'
3	LOAD_GLOBAL       'messenger'
6	LOAD_ATTR         '_getEvents'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '110'
16	STORE_FAST        'msgName'

19	LOAD_CONST        None
22	YIELD_VALUE       None

23	LOAD_FAST         'self'
26	LOAD_ATTR         '_creator'
29	LOAD_ATTR         '_getMessageNamePattern'
32	LOAD_FAST         'msgName'
35	CALL_FUNCTION_1   None
38	STORE_FAST        'namePattern'

41	LOAD_FAST         'namePattern'
44	LOAD_FAST         'self'
47	LOAD_ATTR         '_creator'
50	LOAD_ATTR         '_msgName2detector'
53	COMPARE_OP        'not in'
56	JUMP_IF_FALSE     '84'

59	LOAD_GLOBAL       '_MessageTypeLeakDetector'
62	LOAD_FAST         'namePattern'
65	CALL_FUNCTION_1   None
68	LOAD_FAST         'self'
71	LOAD_ATTR         '_creator'
74	LOAD_ATTR         '_msgName2detector'
77	LOAD_FAST         'namePattern'
80	STORE_SUBSCR      None
81	JUMP_FORWARD      '84'
84_0	COME_FROM         '81'

84	LOAD_FAST         'self'
87	LOAD_ATTR         '_creator'
90	LOAD_ATTR         '_msgName2detector'
93	LOAD_FAST         'namePattern'
96	BINARY_SUBSCR     None
97	LOAD_ATTR         'addMsgName'
100	LOAD_FAST         'msgName'
103	CALL_FUNCTION_1   None
106	POP_TOP           None
107	JUMP_BACK         '13'
110	POP_BLOCK         None
111_0	COME_FROM         '0'

111	LOAD_GLOBAL       'Job'
114	LOAD_ATTR         'Done'
117	YIELD_VALUE       None
118	LOAD_CONST        None
121	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 38


class MessageTypesLeakDetector(LeakDetector, MessageLeakDetectorBase):
    __module__ = __name__

    def __init__(self):
        LeakDetector.__init__(self)
        self._msgName2detector = {}
        self._createJob = None
        if config.GetBool('leak-message-types', 0):
            self._leakers = []
            self._leakTaskName = uniqueName('leak-message-types')
            taskMgr.add(self._leak, self._leakTaskName)
        return

    def _leak(self, task):
        self._leakers.append(DirectObject())
        self._leakers[-1].accept('leak-msg', self._leak)
        return task.cont

    def destroy(self):
        if hasattr(self, '_leakTaskName'):
            taskMgr.remove(self._leakTaskName)
            for leaker in self._leakers:
                leaker.ignoreAll()

            self._leakers = None
        if self._createJob:
            self._createJob.destroy()
        self._createJob = None
        for msgName, detector in self._msgName2detector.iteritems():
            detector.destroy()

        del self._msgName2detector
        LeakDetector.destroy(self)
        return

    def __len__(self):
        if self._createJob:
            if self._createJob.isFinished():
                self._createJob.destroy()
                self._createJob = None
        self._createJob = _MessageTypeLeakDetectorCreator(self)
        jobMgr.add(self._createJob)
        return len(self._msgName2detector)


class _MessageListenerTypeLeakDetector(LeakDetector):
    __module__ = __name__

    def __init__(self, typeName):
        self._typeName = typeName
        LeakDetector.__init__(self)

    def __len__(self):
        numObjs = 0
        for obj in messenger._getObjects():
            if typeName(obj) == self._typeName:
                numObjs += 1

        return numObjs

    def getLeakDetectorKey(self):
        return '%s-%s' % (self._typeName, self.__class__.__name__)


class _MessageListenerTypeLeakDetectorCreator(Job):
    __module__ = __name__

    def __init__(self, creator):
        Job.__init__(self, uniqueName(typeName(self)))
        self._creator = creator

    def destroy(self):
        self._creator = None
        Job.destroy(self)
        return

    def finished(self):
        Job.finished(self)

    def run--- This code section failed: ---

0	SETUP_LOOP        '82'
3	LOAD_GLOBAL       'messenger'
6	LOAD_ATTR         '_getObjects'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '81'
16	STORE_FAST        'obj'

19	LOAD_CONST        None
22	YIELD_VALUE       None

23	LOAD_GLOBAL       'typeName'
26	LOAD_FAST         'obj'
29	CALL_FUNCTION_1   None
32	STORE_FAST        'tName'

35	LOAD_FAST         'tName'
38	LOAD_FAST         'self'
41	LOAD_ATTR         '_creator'
44	LOAD_ATTR         '_typeName2detector'
47	COMPARE_OP        'not in'
50	JUMP_IF_FALSE     '78'

53	LOAD_GLOBAL       '_MessageListenerTypeLeakDetector'
56	LOAD_FAST         'tName'
59	CALL_FUNCTION_1   None
62	LOAD_FAST         'self'
65	LOAD_ATTR         '_creator'
68	LOAD_ATTR         '_typeName2detector'
71	LOAD_FAST         'tName'
74	STORE_SUBSCR      None
75	JUMP_BACK         '13'
78	JUMP_BACK         '13'
81	POP_BLOCK         None
82_0	COME_FROM         '0'

82	LOAD_GLOBAL       'Job'
85	LOAD_ATTR         'Done'
88	YIELD_VALUE       None
89	LOAD_CONST        None
92	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 32


class MessageListenerTypesLeakDetector(LeakDetector):
    __module__ = __name__

    def __init__(self):
        LeakDetector.__init__(self)
        self._typeName2detector = {}
        self._createJob = None
        if config.GetBool('leak-message-listeners', 0):
            self._leakers = []
            self._leakTaskName = uniqueName('leak-message-listeners')
            taskMgr.add(self._leak, self._leakTaskName)
        return

    def _leak(self, task):
        self._leakers.append(DirectObject())
        self._leakers[-1].accept(uniqueName('leak-msg-listeners'), self._leak)
        return task.cont

    def destroy(self):
        if hasattr(self, '_leakTaskName'):
            taskMgr.remove(self._leakTaskName)
            for leaker in self._leakers:
                leaker.ignoreAll()

            self._leakers = None
        if self._createJob:
            self._createJob.destroy()
        self._createJob = None
        for typeName, detector in self._typeName2detector.iteritems():
            detector.destroy()

        del self._typeName2detector
        LeakDetector.destroy(self)
        return

    def __len__(self):
        if self._createJob:
            if self._createJob.isFinished():
                self._createJob.destroy()
                self._createJob = None
        self._createJob = _MessageListenerTypeLeakDetectorCreator(self)
        jobMgr.add(self._createJob)
        return len(self._typeName2detector)# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:37 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\LeakDetectors.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '82'
3	LOAD_GLOBAL       'messenger'
6	LOAD_ATTR         '_getObjects'
9	CALL_FUNCTION_0   None
12	GET_ITER          None
13	FOR_ITER          '81'
16	STORE_FAST        'obj'

19	LOAD_CONST        None
22	YIELD_VALUE       None

23	LOAD_GLOBAL       'typeName'
26	LOAD_FAST         'obj'
29	CALL_FUNCTION_1   None
32	STORE_FAST        'tName'

35	LOAD_FAST         'tName'
38	LOAD_FAST         'self'
41	LOAD_ATTR         '_creator'
44	LOAD_ATTR         '_typeName2detector'
47	COMPARE_OP        'not in'
50	JUMP_IF_FALSE     '78'

53	LOAD_GLOBAL       '_MessageListenerTypeLeakDetector'
56	LOAD_FAST         'tName'
59	CALL_FUNCTION_1   None
62	LOAD_FAST         'self'
65	LOAD_ATTR         '_creator'
68	LOAD_ATTR         '_typeName2detector'
71	LOAD_FAST         'tName'
74	STORE_SUBSCR      None
75	JUMP_BACK         '13'
78	JUMP_BACK         '13'
81	POP_BLOCK         None
82_0	COME_FROM         '0'

82	LOAD_GLOBAL       'Job'
85	LOAD_ATTR         'Done'
88	YIELD_VALUE       None
89	LOAD_CONST        None
92	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 32

